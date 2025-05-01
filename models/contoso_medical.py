from abc import ABC
from typing import TypedDict, Any


class UserRecord(TypedDict):
    id: str
    user_id: str
    first_name: str
    last_name: str
    email: str
    groups: list[str]
    caregivers: list[str]
    medical_providers: list[str]

class MedicalRecord(TypedDict):
    id: str
    record_id: str
    patient_id: str
    record_type: str
    details: str

class Facility(TypedDict):
    id: str
    facility_id: str
    name: str

class EmploymentRecord(TypedDict):
    id: str
    employee_id: str
    first_name: str
    last_name: str
    email: str
    job_title: str
    hire_date: str  # ISO format date string (e.g., "2023-01-18")
    hourly_rate: float

class DataExtractor(ABC):

    @staticmethod
    def populate_medical_record(search_result: dict[str, Any]) -> MedicalRecord:
        return MedicalRecord(
            id=search_result["id"],
            record_id=search_result["record_id"],
            patient_id=search_result["patient_id"],
            record_type=search_result["record_type"],
            details=search_result["details"]
        )

    # Function to map a search_result dict into a UserRecord
    @staticmethod
    def populate_user_record(search_result: dict[str, Any]) -> UserRecord:
        return UserRecord(
            id=search_result["id"],
            user_id=search_result["user_id"],
            first_name=search_result["first_name"],
            last_name=search_result["last_name"],
            email=search_result["email"],
            groups=search_result.get("groups", []),
            caregivers=search_result.get("caregivers", []),
            medical_providers=search_result.get("medical_providers", [])
        )

    @staticmethod
    def populate_facility(search_result: dict[str, Any]) -> Facility:
        return Facility(
            id=search_result["id"],
            facility_id=search_result["facility_id"],
            name=search_result["name"]
        )

    @staticmethod
    def populate_employment_record(search_result: dict[str, Any]) -> EmploymentRecord:
        return EmploymentRecord(
            id=search_result["id"],
            employee_id=search_result["employee_id"],
            first_name=search_result["first_name"],
            last_name=search_result["last_name"],
            email=search_result["email"],
            job_title=search_result["job_title"],
            hire_date=search_result["hire_date"],
            hourly_rate=float(search_result["hourly_rate"])  # convert if needed
        )