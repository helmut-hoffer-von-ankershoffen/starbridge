import json
import platform
import subprocess
import sys
import time
from pathlib import Path

import psutil

from starbridge import __is_running_in_container__, __project_name__
from starbridge.mcp import MCPBaseService, MCPContext, mcp_tool
from starbridge.utils import Health, get_logger

logger = get_logger(__name__)


class Service(MCPBaseService):
    """Service class for Claude operations."""

    def __init__(self):
        super().__init__()

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> Health:
        """Check if Claude Desktop application is installed and is running."""
        if __is_running_in_container__:
            return Health(
                status=Health.Status.DOWN,
                reason="Checking health of Claude not supported in a container",
            )
        if not self.is_installed():
            return Health(status=Health.Status.DOWN, reason="not installed")
        if not self.is_running():
            return Health(status=Health.Status.DOWN, reason="not running")
        return Health(status=Health.Status.UP)

    @mcp_tool()
    def info(self, context: MCPContext | None = None):
        """Get info about Claude Desktop application. This includes if it is installed, running, config, and processes running next to Claude."""
        data = {
            "is_installed": self.is_installed(),
            "is_running": self.is_running(),
            "application_directory": None,
            "config_path": None,
            "log_path": None,
            "config": None,
            "pid": None,
            "processes": [],
        }
        if self.is_installed():
            data["application_directory"] = str(self.application_directory())
            if self.has_config():
                data["config_path"] = str(self.config_path())
                data["config"] = self.config_read()
                data["log_path"] = str(self.log_path())
        data["processes"] = []
        for proc in psutil.process_iter(attrs=["pid", "ppid", "name"]):
            try:
                cmdline = proc.cmdline()
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                cmdline = None
            data["processes"].append({
                "pid": proc.info["pid"],
                "ppid": proc.info["ppid"],
                "name": proc.info["name"],
                "cmdline": cmdline,
            })
            if proc.info["name"] == "Claude":
                data["pid"] = proc.info["pid"]
        return data

    @mcp_tool()
    def restart(self, context: MCPContext | None = None) -> str:
        """Restart Claude Desktop application. The agent should use this tool when asked to restart itself"""
        Service._restart()
        return "Claude Desktop application restarted"

    @staticmethod
    def application_directory() -> Path:
        """Get path of Claude config directory based on platform."""
        if __is_running_in_container__:
            return Path("/Claude/.config")
        match sys.platform:
            case "darwin":
                return Path(Path.home(), "Library", "Application Support", "Claude")
            case "win32":
                return Path(Path.home(), "AppData", "Roaming", "Claude")
            case "linux":
                return Path(Path.home(), ".config", "Claude")
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    @staticmethod
    def is_installed() -> bool:
        """Check if Claude Desktop application is installed."""
        return Service.application_directory().is_dir()

    @staticmethod
    def is_running() -> bool:
        """Check if Claude Desktop application is running."""
        if __is_running_in_container__:
            logger.warning(
                "Checking if Claude is running is not supported in container"
            )
            return False

        return any(
            proc.info["name"] == "Claude"
            for proc in psutil.process_iter(attrs=["name"])
        )

    @staticmethod
    def config_path() -> Path:
        """Get path of Claude config based on platform."""
        return Service.application_directory() / "claude_desktop_config.json"

    @staticmethod
    def has_config() -> bool:
        """Check if Claud has configuration."""
        return Service.config_path().is_file()

    @staticmethod
    def config_read() -> dict:
        """Read config from file."""
        config_path = Service.config_path()
        if config_path.is_file():
            with open(config_path, encoding="utf8") as file:
                return json.load(file)
        raise FileNotFoundError(f"No config file found at '{config_path}'")

    @staticmethod
    def config_write(config: dict) -> dict:
        """Write config to file."""
        config_path = Service.config_path()
        with open(config_path, "w", encoding="utf8") as file:
            json.dump(config, file, indent=2)
        return config

    @staticmethod
    def log_directory() -> Path:
        """Get path of Claude log directory based on platform."""
        match sys.platform:
            case "darwin":
                return Path(Path.home(), "Library", "Logs", "Claude")
            case "win32":
                return Path(Path.home(), "AppData", "Roaming", "Claude", "logs")
            case "linux":
                return Path(Path.home(), ".logs", "Claude")
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    @staticmethod
    def log_path(mcp_server_name: str | None = __project_name__) -> Path:
        """Get path of mcp ."""
        path = Service.log_directory()
        if mcp_server_name is None:
            return path / "mcp.log"
        return path / f"mcp-server-{mcp_server_name}.log"

    @staticmethod
    def install_mcp_server(
        mcp_server_config: dict, mcp_server_name=__project_name__, restart=True
    ) -> bool:
        """Install MCP server in Claude Desktop application."""
        if Service.is_installed() is False:
            raise RuntimeError(
                f"Claude Desktop application is not installed at '{Service.application_directory()}'"
            )
        try:
            config = Service.config_read()
        except FileNotFoundError:
            config = {"mcpServers": {}}

        if (
            mcp_server_name in config["mcpServers"]
            and config["mcpServers"][mcp_server_name] == mcp_server_config
        ):
            if restart:
                Service._restart()
            return False

        config["mcpServers"][mcp_server_name] = mcp_server_config
        Service.config_write(config)
        if restart:
            Service._restart()
        return True

    @staticmethod
    def uninstall_mcp_server(
        mcp_server_name: str = __project_name__, restart=True
    ) -> bool:
        """Uninstall MCP server from Claude Desktop application."""
        if Service.is_installed() is False:
            raise RuntimeError(
                f"Claude Desktop application is not installed at '{Service.application_directory()}'"
            )
        try:
            config = Service.config_read()
        except FileNotFoundError:
            config = {"mcpServers": {}}
        if mcp_server_name not in config["mcpServers"]:
            return False
        del config["mcpServers"][mcp_server_name]
        Service.config_write(config)
        if restart:
            Service._restart()
        return True

    @staticmethod
    def platform_supports_restart():
        """Check if platform supports restarting Claude."""
        return not __is_running_in_container__

    @staticmethod
    def _restart():
        """Restarts the Claude desktop application on macOS."""
        if Service.platform_supports_restart() is False:
            raise RuntimeError("Restarting Claude is not supported in container")

        # Find and terminate all Claude processes
        for proc in psutil.process_iter(attrs=["name"]):
            if proc.info["name"] == "Claude":
                proc.terminate()

        # Wait for processes to terminate
        time.sleep(2)

        match platform.system():
            case "Darwin":
                return subprocess.run(["open", "-a", "Claude"], shell=False, check=True)
            case "win23":
                return subprocess.run(["start", "Claude"], shell=True, check=True)
            case "Linux":
                return subprocess.run(["xdg-open", "Claude"], shell=False, check=True)

        raise RuntimeError(f"Starting Claude not supported on {platform.system()}")
