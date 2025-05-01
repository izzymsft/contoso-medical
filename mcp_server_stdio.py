from random import random

from mcp.server import FastMCP
from mcp.server.fastmcp import Context

from models.contoso_medical import UserRecord, Facility
from shared.facilities_dao import FacilityDao
from shared.mcp_base_server import IzzyMCP
from shared.medical_records_dao import MedicalRecordsDao
from shared.users_dao import UsersDao

mcp = IzzyMCP("Contoso Medical MCP Service", log_level="DEBUG")

@mcp.tool(description="Retrieve all patients from Contoso Medical")
async def retrieve_all_patients() -> list[UserRecord]:
    dao = UsersDao()
    return dao.get_all_users()

@mcp.tool(description="Retrieve all Facilities from Contoso Medical")
async def retrieve_all_facilities() -> list[Facility]:
    dao = FacilityDao()
    return dao.get_all_facilities()

@mcp.tool(description="Returns information about Contoso Medical")
async def get_information() -> str:
    return "This service provides information about Contoso Medical patients, facilities, employees and caregivers"

@mcp.tool(description="Retrieves medical records for a specific patient")
async def get_my_medical_records(user_id: str):
    medical_records_dao = MedicalRecordsDao()
    return medical_records_dao.get_patient_medical_records(user_id)

if __name__ == "__main__":
    mcp.run(transport='stdio')