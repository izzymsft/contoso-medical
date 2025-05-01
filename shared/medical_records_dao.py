from models.contoso_medical import DataExtractor, MedicalRecord
from utils.cosmos_db_utils import CosmosDbUtils


class MedicalRecordsDao(DataExtractor):
    """
    Data Access Object (DAO) for retrieving and processing medical records
    from the 'medical_records' container in Cosmos DB.

    Inherits from:
        DataExtractor: Base class providing record population utilities.
    """

    def __init__(self):
        """
        Initializes the MedicalRecordsDao with a CosmosDbUtils instance
        targeting the 'medical_records' container.
        """
        self.cosmos_util = CosmosDbUtils("medical_records")

    def get_all_medical_records(self) -> list[MedicalRecord]:
        """
        Retrieves all medical records stored in the database.

        Returns:
            list[MedicalRecord]: A list of all medical records.
        """
        search_results = self.cosmos_util.get_all_items(max_item_count=1024)
        all_records: list[MedicalRecord] = []

        for search_result in search_results:
            all_records.append(self.populate_medical_record(search_result))

        return all_records

    def get_patient_medical_records(self, patient_id: str) -> list[MedicalRecord]:
        """
        Retrieves all medical records associated with a specific patient.

        Args:
            patient_id (str): The ID of the patient whose records are to be retrieved.

        Returns:
            list[MedicalRecord]: A list of medical records for the specified patient.
        """
        search_results = self.get_all_medical_records()

        patient_records: list[MedicalRecord] = []

        for search_result in search_results:
            current_patient_id = search_result['patient_id']
            if current_patient_id == patient_id:
                patient_records.append(search_result)

        return patient_records
