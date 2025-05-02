import os
from random import random

from mcp.server import FastMCP
from mcp.server.fastmcp import Context

from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage
from models.contoso_medical import UserRecord, Facility
from shared.facilities_dao import FacilityDao
from shared.mcp_base_server import IzzyMCP
from shared.medical_records_dao import MedicalRecordsDao
from shared.users_dao import UsersDao
import base64

mcp = IzzyMCP("Contoso Medical MCP Service", log_level="DEBUG")


def get_current_file_directory() -> str:
    """
    Returns the absolute path of the directory where the current Python file is located.

    :return: Absolute path to the current file's directory.
    """
    return os.path.dirname(os.path.abspath(__file__))



def encode_png_to_base64(file_path: str) -> str:
    """
    Encodes a PNG file into a Base64 string.

    :param file_path: Path to the PNG file.
    :return: Base64-encoded string of the PNG image.
    """
    with open(file_path, "rb") as image_file:
        encoded_bytes = base64.b64encode(image_file.read())
        return encoded_bytes.decode("utf-8")

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

# Image Webserver is hosted from facility_images using python3 -m http.server 8000 --directory .
@mcp.tool(description="Retrieve path for a facility image")
def retrieve_facility_image(facility_id: str) -> str:
    """

    :param facility_id: The identifier for the facility
    :return:
    """
    facility_image_path = f"http://localhost:8000/{facility_id}.png"

    return facility_image_path

if __name__ == "__main__":
    mcp.run(transport='stdio')