"""Handles Claude operations."""

import json
import platform
import subprocess
import sys
import time
from pathlib import Path

from pydantic import BaseModel


class Application(BaseModel):
    """Class to interact with Claude Desktop application."""

    @staticmethod
    def info(mcp_server_name: str = "starbridge") -> dict:
        """Check if Claude Desktop application is installed."""
        data = {
            "is_installed": Application.is_installed(),
            "application_directory": None,
            "config_path": None,
            "log_path": None,
            "config": None,
        }
        if Application.is_installed():
            data["application_directory"] = str(Application.application_directory())
            if Application.has_config():
                data["config_path"] = str(Application.config_path())
                data["config"] = Application.config_read()
                data["log_path"] = str(Application.log_path(mcp_server_name))
        return data

    @staticmethod
    def health() -> str:
        """Check if Claude Desktop application is installed and is running."""
        if Application.is_installed() is False:
            return "DOWN: Not installed"
        if Application.is_running() is False:
            return "DOWN: Not running"
        return "UP"

    @staticmethod
    def is_installed() -> bool:
        """Check if Claude Desktop application is installed."""
        if Application.application_directory().is_dir():
            return True
        return False

    @staticmethod
    def is_running() -> bool:
        """Check if Claude Desktop application is running."""
        if platform.system() != "Darwin":
            raise RuntimeError("This command only works on macOS")

        ps_check = subprocess.run(
            ["pgrep", "-x", "Claude"], capture_output=True, text=True, check=False
        )

        if ps_check.returncode == 0:
            return True
        return False

    @staticmethod
    def application_directory() -> Path:
        """Get path of Claude config directory based on platform."""
        if sys.platform == "darwin":
            return Path(
                Path.home(),
                "Library",
                "Application Support",
                "Claude",
            )
        elif sys.platform == "win32":
            return Path(
                Path.home(),
                "AppData",
                "Roaming",
                "Claude",
            )
        elif sys.platform == "linux":
            return Path(
                Path.home(),
                ".config",
                "Claude",
            )
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    @staticmethod
    def config_path() -> Path:
        """Get path of Claude config based on platform."""
        path = Application.application_directory()
        return path / "claude_desktop_config.json"

    @staticmethod
    def has_config() -> bool:
        """Check if Claud has configuration."""
        return Application.config_path().is_file()

    @staticmethod
    def config_read() -> dict:
        """Read config from file."""
        config_path = Application.config_path()
        if config_path.is_file():
            with open(config_path, encoding="utf8") as file:
                return json.load(file)
        raise FileNotFoundError(f"No config file found at '{config_path}'")

    @staticmethod
    def config_write(config: dict) -> dict:
        """Write config to file."""
        config_path = Application.config_path()
        with open(config_path, "w", encoding="utf8") as file:
            json.dump(config, file, indent=2)
        return config

    @staticmethod
    def log_directory() -> Path:
        """Get path of Claude log directory based on platform."""
        if sys.platform == "darwin":
            return Path(
                Path.home(),
                "Library",
                "Logs",
                "Claude",
            )
        elif sys.platform == "win32":
            return Path(
                Path.home(),
                "AppData",
                "Roaming",
                "Claude",
                "logs",
            )
        elif sys.platform == "linux":
            return Path(
                Path.home(),
                ".logs",
                "Claude",
            )
        raise RuntimeError(f"Unsupported platform {sys.platform}")

    @staticmethod
    def log_path(mcp_server_name: str | None = "starbridge") -> Path:
        """Get path of mcp ."""
        path = Application.log_directory()
        if mcp_server_name is None:
            return path / "mcp.log"
        return path / f"mcp-server-{mcp_server_name}.log"

    @staticmethod
    def install_mcp_server(
        mcp_server_config: dict, mcp_server_name="starbridge", restart=True
    ) -> bool:
        """Install MCP server in Claude Desktop application."""
        if Application.is_installed() is False:
            raise RuntimeError(
                f"Claude Desktop application is not installed at '{Application.application_directory()}'"
            )
        try:
            config = Application.config_read()
        except FileNotFoundError:
            config = {"mcpServers": {}}

        if (
            mcp_server_name in config["mcpServers"]
            and config["mcpServers"][mcp_server_name] == mcp_server_config
        ):
            return False

        config["mcpServers"][mcp_server_name] = mcp_server_config
        Application.config_write(config)
        if restart:
            Application.restart()
        return True

    @staticmethod
    def uninstall_mcp_server(mcp_server_name: str = "starbridge", restart=True) -> bool:
        """Uninstall MCP server from Claude Desktop application."""
        if Application.is_installed() is False:
            raise RuntimeError(
                f"Claude Desktop application is not installed at '{Application.application_directory()}'"
            )
        try:
            config = Application.config_read()
        except FileNotFoundError:
            config = {"mcpServers": {}}
        if "name" not in config["mcpServers"]:
            return False
        del config["mcpServers"][mcp_server_name]
        Application.config_write(config)
        if restart:
            Application.restart()
        return True

    @staticmethod
    def restart():
        """Restarts the Claude desktop application on macOS."""
        if platform.system() != "Darwin":
            raise RuntimeError("This command only works on macOS")

        ps_check = subprocess.run(
            ["pgrep", "-x", "Claude"], capture_output=True, text=True, check=False
        )

        if ps_check.returncode == 0:
            subprocess.run(["pkill", "-x", "Claude"], check=False)
            time.sleep(1)

        subprocess.run(["open", "-a", "Claude"], check=True)

    @staticmethod
    def _run_brew_command(args: list) -> tuple[int, str, str]:
        """Run a homebrew command and return (returncode, stdout, stderr)"""
        process = subprocess.run(
            ["brew"] + args, capture_output=True, text=True, check=False
        )
        return process.returncode, process.stdout, process.stderr

    @staticmethod
    def install_via_brew() -> bool:
        """Install Claude via Homebrew if not already installed."""
        if platform.system() != "Darwin":
            raise RuntimeError("Homebrew installation only supported on macOS")

        # Check if already installed
        returncode, _, _ = Application._run_brew_command(["list", "--cask", "claude"])
        if returncode == 0:
            return False  # Already installed

        # Install Claude
        returncode, _, stderr = Application._run_brew_command([
            "install",
            "--cask",
            "claude",
        ])
        if returncode != 0:
            raise RuntimeError(f"Failed to install Claude: {stderr}")

        return True

    @staticmethod
    def uninstall_via_brew() -> bool:
        """Uninstall Claude via Homebrew."""
        if platform.system() != "Darwin":
            raise RuntimeError("Homebrew uninstallation only supported on macOS")

        # Check if installed
        returncode, _, _ = Application._run_brew_command(["list", "--cask", "claude"])
        if returncode != 0:
            return False  # Not installed

        # Uninstall Claude
        returncode, _, stderr = Application._run_brew_command([
            "uninstall",
            "--cask",
            "claude",
        ])
        if returncode != 0:
            raise RuntimeError(f"Failed to uninstall Claude: {stderr}")

        return True
