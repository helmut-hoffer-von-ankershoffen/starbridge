"""Service implementation for managing Claude Desktop application."""

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

    def __init__(self) -> None:
        """Initialize the Claude service."""
        super().__init__()

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> Health:  # noqa: ARG002
        """
        Check if Claude Desktop application is installed and is running.

        Args:
            context (MCPContext | None): Optional MCP context.

        Returns:
            Health: Health status of the Claude Desktop application.

        """
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
    def info(self, context: MCPContext | None = None):  # noqa: ARG002, ANN201
        """
        Get info about Claude Desktop application.

        This includes if it is installed, running, config, and processes running next to Claude.

        Args:
            context (MCPContext | None): Optional MCP context.

        Returns:
            dict: Information about the Claude Desktop application.

        """
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
    def restart(self, context: MCPContext | None = None) -> str:  # noqa: PLR6301, ARG002
        """
        Restart Claude Desktop application.

        The agent should use this tool when asked to restart itself.

        Args:
            context (MCPContext | None): Optional MCP context.

        Returns:
            str: Confirmation message.

        """
        Service._restart()
        return "Claude Desktop application restarted"

    @staticmethod
    def application_directory() -> Path:
        """
        Get path of Claude config directory based on platform.

        Returns:
            Path: Directory path.

        Raises:
            RuntimeError: If platform is not supported.

        """
        if __is_running_in_container__:
            return Path("/Claude/.config")
        match sys.platform:
            case "darwin":
                return Path(Path.home(), "Library", "Application Support", "Claude")
            case "win32":
                return Path(Path.home(), "AppData", "Roaming", "Claude")
            case "linux":
                return Path(Path.home(), ".config", "Claude")
        msg = f"Unsupported platform {sys.platform}"
        raise RuntimeError(msg)

    @staticmethod
    def is_installed() -> bool:
        """
        Check if Claude Desktop application is installed.

        Returns:
            bool: True if installed, False otherwise.

        """
        return Service.application_directory().is_dir()

    @staticmethod
    def is_running() -> bool:
        """
        Check if Claude Desktop application is running.

        Returns:
            bool: True if running, False otherwise.

        """
        if __is_running_in_container__:
            logger.warning(
                "Checking if Claude is running is not supported in container",
            )
            return False

        return any(proc.info["name"] == "Claude" for proc in psutil.process_iter(attrs=["name"]))

    @staticmethod
    def config_path() -> Path:
        """
        Get path of Claude config based on platform.

        Returns:
            Path: Config file path.

        """
        return Service.application_directory() / "claude_desktop_config.json"

    @staticmethod
    def has_config() -> bool:
        """
        Check if Claude has configuration.

        Returns:
            bool: True if config exists, False otherwise.

        """
        return Service.config_path().is_file()

    @staticmethod
    def config_read() -> dict:
        """
        Read config from file.

        Returns:
            dict: Configuration data.

        Raises:
            FileNotFoundError: If config file doesn't exist.

        """
        config_path = Service.config_path()
        if config_path.is_file():
            with config_path.open(encoding="utf8") as file:
                return json.load(file)
        msg = f"No config file found at '{config_path}'"
        raise FileNotFoundError(msg)

    @staticmethod
    def config_write(config: dict) -> dict:
        """
        Write config to file.

        Args:
            config (dict): Configuration data to write.

        Returns:
            dict: Written configuration data.

        """
        config_path = Service.config_path()
        with config_path.open("w", encoding="utf8") as file:
            json.dump(config, file, indent=2)
        return config

    @staticmethod
    def log_directory() -> Path:
        """
        Get path of Claude log directory based on platform.

        Returns:
            Path: Log directory path.

        Raises:
            RuntimeError: If platform is not supported.

        """
        match sys.platform:
            case "darwin":
                return Path(Path.home(), "Library", "Logs", "Claude")
            case "win32":
                return Path(Path.home(), "AppData", "Roaming", "Claude", "logs")
            case "linux":
                return Path(Path.home(), ".logs", "Claude")
        msg = f"Unsupported platform {sys.platform}"
        raise RuntimeError(msg)

    @staticmethod
    def log_path(mcp_server_name: str | None = __project_name__) -> Path:
        """
        Get path of MCP server log file.

        Args:
            mcp_server_name (str | None): Name of the MCP server. Defaults to project name.

        Returns:
            Path: Log file path.

        """
        path = Service.log_directory()
        if mcp_server_name is None:
            return path / "mcp.log"
        return path / f"mcp-server-{mcp_server_name}.log"

    @staticmethod
    def install_mcp_server(
        mcp_server_config: dict,
        mcp_server_name: str = __project_name__,
        restart: bool = True,
    ) -> bool:
        """
        Install MCP server in Claude Desktop application.

        Args:
            mcp_server_config (dict): Configuration for the MCP server.
            mcp_server_name (str): Name of the MCP server.
            restart (bool): Restart Claude Desktop application after installation.

        Returns:
            bool: True if installation successful.

        Raises:
            RuntimeError: If Claude is not installed.

        """
        if Service.is_installed() is False:
            msg = f"Claude Desktop application is not installed at '{Service.application_directory()}'"
            raise RuntimeError(
                msg,
            )
        try:
            config = Service.config_read()
        except FileNotFoundError:
            config = {"mcpServers": {}}

        if mcp_server_name in config["mcpServers"] and config["mcpServers"][mcp_server_name] == mcp_server_config:
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
        mcp_server_name: str = __project_name__,
        restart: bool = True,
    ) -> bool:
        """
        Uninstall MCP server from Claude Desktop application.

        Args:
            mcp_server_name (str): Name of the MCP server.
            restart (bool): Restart Claude Desktop application after uninstallation.

        Returns:
            bool: True if uninstallation successful.

        Raises:
            RuntimeError: If Claude is not installed.

        """
        if Service.is_installed() is False:
            msg = f"Claude Desktop application is not installed at '{Service.application_directory()}'"
            raise RuntimeError(
                msg,
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
    def platform_supports_restart() -> bool:
        """
        Check if platform supports restarting Claude.

        Returns:
            bool: True if restart is supported.

        """
        return not __is_running_in_container__

    @staticmethod
    def _restart() -> subprocess.CompletedProcess[bytes]:
        """
        Restarts the Claude desktop application on macOS.

        Returns:
            subprocess.CompletedProcess: The completed process.

        Raises:
            RuntimeError: If restart is not supported on the platform.

        """
        if Service.platform_supports_restart() is False:
            msg = "Restarting Claude is not supported in container"
            raise RuntimeError(msg)

        # Find and terminate all Claude processes
        for proc in psutil.process_iter(attrs=["name"]):
            if proc.info["name"] == "Claude":
                proc.terminate()

        # Wait for processes to terminate
        time.sleep(2)

        match platform.system():
            case "Darwin":
                return subprocess.run(["/usr/bin/open", "-a", "Claude"], shell=False, check=True)  # noqa: S603
            case "win23":
                return subprocess.run(["start", "Claude"], shell=True, check=True)  # noqa: S607, S602
            case "Linux":
                return subprocess.run(["xdg-open", "Claude"], shell=False, check=True)  # noqa: S607, S603

        msg = f"Starting Claude not supported on {platform.system()}"
        raise RuntimeError(msg)
