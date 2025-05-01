import logging
import os
from typing import Any

from mcp import InitializedNotification
from mcp.server import FastMCP
from mcp.server.lowlevel import Server
from mcp.server.session import ServerSession
from mcp.types import Tool as MCPTool, CreateMessageRequest, RootsListChangedNotification, ListRootsResult

from mcp.server.fastmcp.server import stdio_server, logger

class IzzyMCP(FastMCP):

    def __init__(
            self, name: str | None = None, instructions: str | None = None, **settings: Any
    ):
        super().__init__(name=name, instructions=instructions, **settings)

        self.client_roots  = None
        self._register_notification_handlers()

    def _register_notification_handlers(self):
        pass

    @staticmethod
    def _get_role_tools() -> list[str]:
        user_role = os.environ.get("USER_ROLE")

        # ["hospital-admin", "caregiver", "patient"]
        tool_database: dict[str, list[str]] = {
            "hospital-admin" : ["get_information", "retrieve_all_patients", "retrieve_all_facilities"],
            "caregiver": ["get_information", "get_my_medical_records"],
            "patient": ["get_information", "get_my_medical_records"]
        }

        return tool_database[user_role]

    async def list_tools(self) -> list[MCPTool]:

        filtered_tool_names = self._get_role_tools()
        filtered_tool_list: list[MCPTool] = []
        tool_list: list[MCPTool] = await super().list_tools()

        for current_tool in tool_list:
            if current_tool.name in filtered_tool_names:
                filtered_tool_list.append(current_tool)

        return filtered_tool_list

    def get_session(self):
        return self.get_context().session