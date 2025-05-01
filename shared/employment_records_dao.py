from models.contoso_medical import DataExtractor, EmploymentRecord
from utils.cosmos_db_utils import CosmosDbUtils


class EmploymentRecordDao(DataExtractor):
    """
    Data Access Object (DAO) for managing employment records
    stored in the 'employment_records' Cosmos DB container.

    Inherits from:
        DataExtractor: Provides helper methods to populate structured records from raw data.
    """

    def __init__(self):
        """
        Initializes the EmploymentRecordDao with a CosmosDbUtils instance
        targeting the 'employment_records' container.
        """
        self.cosmos_util = CosmosDbUtils("employment_records")

    def get_all_employment_records(self) -> list[EmploymentRecord]:
        """
        Retrieves all employment records from the database.

        Returns:
            list[EmploymentRecord]: A list of all employment records.
        """
        search_results = self.cosmos_util.get_all_items(max_item_count=1024)
        all_records: list[EmploymentRecord] = []

        for search_result in search_results:
            all_records.append(self.populate_employment_record(search_result))

        return all_records

    def get_employee_employment_record(self, employee_id: str) -> EmploymentRecord | None:
        """
        Retrieves the employment record for a specific employee.

        Args:
            employee_id (str): The ID of the employee.

        Returns:
            EmploymentRecord | None: The employee's employment record if found, otherwise None.
        """
        search_results = self.get_all_employment_records()

        for search_result in search_results:
            current_employee_id = search_result['employee_id']
            if current_employee_id == employee_id:
                return search_result

        return None

    def update_employee_hourly_rate(self, employee_id: str, new_hourly_rate: float) -> EmploymentRecord:
        """
        Updates the hourly rate for a specific employee.

        Args:
            employee_id (str): The ID of the employee.
            new_hourly_rate (float): The new hourly rate to be set.

        Returns:
            EmploymentRecord: The updated employment record after applying the patch.
        """
        patch_operations = [
            {"op": "set", "path": "/hourly_rate", "value": new_hourly_rate}
        ]

        patched_result: dict = self.cosmos_util.patch_item(
            employee_id,
            partition_key=employee_id,
            patch_operations=patch_operations
        )

        result: EmploymentRecord = self.populate_employment_record(patched_result)

        return result
