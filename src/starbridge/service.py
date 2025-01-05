"""Handles core services operations."""

from starbridge import (
    __is_development_mode__,
    __is_running_in_container__,
    __project_name__,
    __project_path__,
    __version__,
)
from starbridge.mcp import MCPBaseService, MCPContext, MCPServer, mcp_tool
from starbridge.utils import (
    Health,
    get_logger,
    get_process_info,
    get_starbridge_env,
)

logger = get_logger(__name__)


class Service(MCPBaseService):
    """Service class for core services if starbridge."""

    @mcp_tool()
    def health(self, context: MCPContext | None = None) -> Health:  # noqa: ARG002, PLR6301
        """
        Check the health of the core service of Starbridge.

        Args:
            context (MCPContext, optional): The context of the request. Defaults to None.

        Returns:
            Health: The health status of the core service

        """
        return Health(status=Health.Status.UP)  # We are up always

    @mcp_tool()
    def info(self, context: MCPContext | None = None) -> dict:  # noqa: ARG002, PLR6301
        """
        Get info about the environment starbridge is running in and all services.

        Args:
            context (MCPContext, optional): The context of the request. Defaults to None.

        Returns:
            dict: Information about the Starbridge environment and its services

        """
        rtn = {
            "name": __project_name__,
            "version": __version__,
            "path": __project_path__,
            "is_development_mode": __is_development_mode__,
            "is_running_in_container": __is_running_in_container__,
            "env": get_starbridge_env(),
            "process": get_process_info().model_dump(),
        }

        # Auto-discover and get info from all services
        for service_class in MCPServer.service_classes():
            if service_class is Service:  # Skip self
                continue
            service = service_class()
            service_name = service.__class__.__module__.split(".")[1]
            rtn[service_name] = service.info()

        return rtn
