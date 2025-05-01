from models.contoso_medical import DataExtractor, EmploymentRecord
from utils.cosmos_db_utils import CosmosDbUtils


class EmploymentRecordDao(DataExtractor):

    def __init__(self):
        self.cosmos_util = CosmosDbUtils("employment_records")

    def get_all_employment_records(self) -> list[EmploymentRecord]:
        search_results = self.cosmos_util.get_all_items(max_item_count=1024)
        all_records: list[EmploymentRecord] = []

        for search_result in search_results:
            all_records.append(self.populate_employment_record(search_result))

        return all_records

    def get_employee_employment_record(self, employee_id: str) -> EmploymentRecord | None:

        search_results = self.get_all_employment_records()

        for search_result in search_results:
            current_employee_id = search_result['employee_id']
            if current_employee_id == employee_id:
                return search_result

        return None