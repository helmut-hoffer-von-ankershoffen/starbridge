"""Handles Confluence operations."""

import inspect
import json
import os

import mcp.types as types
from atlassian import Confluence
from pydantic import AnyUrl


class Service:
    """Service class for Confluence operations."""

    def health(self) -> str:
        try:
            spaces = self.space_list()
        except Exception as e:
            return f"DOWN: {str(e)}"
        if (
            isinstance(spaces, dict)
            and "results" in spaces
            and isinstance(spaces["results"], list)
        ):
            if len(spaces["results"]) > 0:
                return "UP"
        return "DOWN: No spaces found"

    @staticmethod
    def _parse_docstring_params(docstring: str) -> dict[str, str]:
        """Parse docstring to extract parameter descriptions."""
        if not docstring:
            return {}

        param_desc = {}
        lines = docstring.split("\n")
        in_args_section = False

        for line in lines:
            line = line.strip()

            # Check for Args: section
            if line.lower().startswith("args:"):
                in_args_section = True
                continue

            # We're in the Args section and have indented content
            if in_args_section and line:
                # New parameter definition
                if line and line.startswith("Returns:"):
                    in_args_section = False
                    continue

                parts = line.strip().split(":", 1)
                if len(parts) == 2:
                    param_name = parts[0].strip()
                    description = parts[1].strip()
                    if "(" in param_name:
                        param_name = param_name.split("(")[0].strip()
                    param_desc[param_name] = description

        return param_desc

    @staticmethod
    def tool_list():
        """Get available Confluence tools."""
        tools = []
        for method_name in dir(Service):
            if method_name.startswith("mcp_tool_"):
                tool_name = method_name[9:].replace("_", "-")
                method = getattr(Service, method_name)
                docstring = method.__doc__ or f"Call {tool_name}"
                sig = inspect.signature(method)

                # Get parameter descriptions from docstring
                param_desc = Service._parse_docstring_params(docstring)
                # console.print(docstring)

                # Generate properties from signature
                properties = {}
                required_params = []

                for param in sig.parameters.values():
                    if param.name == "self":
                        continue

                    param_type = "string"  # default type
                    if param.annotation != inspect.Parameter.empty:
                        if param.annotation is str:
                            param_type = "string"
                        elif param.annotation is int:
                            param_type = "number"
                        elif param.annotation is bool:
                            param_type = "boolean"

                    if param.default == inspect.Parameter.empty:
                        required_params.append(param.name)

                    properties[param.name] = {
                        "type": param_type,
                        "description": param_desc.get(
                            param.name, f"Parameter {param.name}"
                        ),
                    }

                tools.append(
                    types.Tool(
                        name=tool_name,
                        description=docstring.split("\n")[0].strip(),
                        inputSchema={
                            "type": "object",
                            "required": required_params,
                            "properties": properties,
                        },
                    )
                )
        return tools

    def resource_list(self):
        spaces = self.space_list()
        return [
            types.Resource(
                uri=AnyUrl(f"starbridge://confluence/space/{space['key']}"),
                name=space["name"],
                description=f"Space of type '{space['type']}'",
                mimeType="application/json",
            )
            for space in spaces["results"]
        ]

    def resource_get(self, uri: AnyUrl) -> str:
        if (uri.scheme, uri.host) != ("starbridge", "confluence"):
            raise ValueError(
                f"Unsupported URI scheme/host combination: {uri.scheme}:{uri.host}"
            )
        if (uri.path or "").startswith("/space/"):
            space_key = uri.path.split("/")[-1]
            return json.dumps(self.space_info(space_key), indent=2)

    @staticmethod
    def prompt_list():
        return [
            types.Prompt(
                name="starbridge-space-summary",
                description="Creates a summary of spaces in Confluence",
                arguments=[
                    types.PromptArgument(
                        name="style",
                        description="Style of the summary (brief/detailed)",
                        required=False,
                    )
                ],
            )
        ]

    def mcp_prompt_starbridge_space_summary(
        self, style: str = "brief"
    ) -> types.GetPromptResult:
        detail_prompt = " Give extensive details." if style == "detailed" else ""
        return types.GetPromptResult(
            description="Summarize the current spaces",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Here are the current spaces to summarize:{detail_prompt}\n\n"
                        + "\n".join(
                            f"- {space['key']}: {space['name']} ({space['type']})"
                            for space in self.space_list()["results"]
                        ),
                    ),
                )
            ],
        )

    def space_info(self, space_key):
        return self._api.get_space(space_key)

    def __init__(self):
        self._url = os.environ.get("STARBRIDGE_ATLASSIAN_URL")
        self._email_address = os.environ.get("STARBRIDGE_ATLASSIAN_EMAIL_ADDRESS")
        self._api_token = os.environ.get("STARBRIDGE_ATLASSIAN_API_TOKEN")
        self._api = Confluence(
            url=self._url,
            username=self._email_address,
            password=self._api_token,
            cloud=True,
        )

    def info(self):
        return {
            "url": self._url,
            "email": self._email_address,
            "api_token": self._api_token,
        }

    def mcp_tool_starbridge_confluence_info(self):
        """Info about Confluence environment"""
        return [types.TextContent(type="text", text=json.dumps(self.info(), indent=2))]

    def space_list(self):
        return self._api.get_all_spaces()

    def mcp_tool_starbridge_confluence_space_list(self):
        """List spaces in Confluence"""
        return [
            types.TextContent(type="text", text=json.dumps(self.space_list(), indent=2))
        ]

    def page_create(
        self,
        space_key,
        title,
        body,
        parent_id=None,
        representation="wiki",
        editor="v2",
        full_width=True,
        status="current",
    ):
        return self._api.create_page(
            space=space_key,
            title=title,
            body=body,
            parent_id=parent_id,
            type="page",
            representation=representation,
            editor=editor,
            full_width=full_width,
            status=status,
        )

    def mcp_tool_starbridge_confluence_page_create(
        self, space_key: str, title: str, body: str, parent_id=None, draft: bool = False
    ):
        """Create page in Confluence space given key of space, title and body of page and optional parent page id.

        Args:
            space_key (str): The key identifier of the Confluence space where the page will be created
            title (str): The title of the new page to be created
            body (str): The content/body of the new page
            parent_id (str, optional): The ID of the parent page if this is to be created as a child page. Defaults to None.
            draft (bool, optional): If to create the page in draft mode. Defaults to False, i.e. page will be published.

        Returns:
            list: A list containing a TextContent object with the JSON response of the page creation
        """
        return [
            types.TextContent(
                type="text",
                text=json.dumps(
                    self.page_create(
                        space_key=space_key,
                        title=title,
                        body=body,
                        parent_id=parent_id,
                        representation="wiki",
                        editor="v2",
                        full_width=True,
                        status="draft" if draft else "current",
                    ),
                    indent=2,
                ),
            )
        ]
