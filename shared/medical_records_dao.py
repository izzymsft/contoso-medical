from models.contoso_medical import DataExtractor, MedicalRecord
from utils.cosmos_db_utils import CosmosDbUtils


class MedicalRecordsDao(DataExtractor):

    def __init__(self):
        self.cosmos_util = CosmosDbUtils("medical_records")

    def get_all_medical_records(self) -> list[MedicalRecord]:
        search_results = self.cosmos_util.get_all_items(max_item_count=1024)
        all_records: list[MedicalRecord] = []

        for search_result in search_results:
            all_records.append(self.populate_medical_record(search_result))

        return all_records

    def get_patient_medical_records(self, patient_id: str)-> list[MedicalRecord]:

        search_results = self.get_all_medical_records()

        patient_records: list[MedicalRecord] = []

        for search_result in search_results:
            current_patient_id = search_result['patient_id']
            if current_patient_id == patient_id:
                patient_records.append(search_result)

        return patient_records

