from typing import Any

from models.contoso_medical import UserRecord, DataExtractor
from utils.cosmos_db_utils import CosmosDbUtils


class UsersDao(DataExtractor):

    def __init__(self):
        self.cosmos_util = CosmosDbUtils("users")

    def get_user(self, user_id: str) -> UserRecord:
        """
        Retrieves a User
        :param user_id:
        :return:
        """
        search_result: dict[str, Any] = self.cosmos_util.get_single_item(user_id, partition_key=user_id)
        return self.populate_user_record(search_result)

    def get_all_users(self) -> list[UserRecord]:

        search_results = self.cosmos_util.get_all_items(max_item_count=1024)

        all_users: list[UserRecord] = []

        for search_result in search_results:
            all_users.append(self.populate_user_record(search_result))

        return all_users


    def get_patient_caregivers(self, patient_id: str) -> list[UserRecord]:

        patient_record: UserRecord = self.get_user(patient_id)
        all_users = self.get_all_users()
        caregiver_filter: list[str] = patient_record['caregivers']

        patient_caregivers: list[UserRecord] = []

        for possible_caregiver in all_users:
            caregiver_user_id = possible_caregiver['user_id']
            if caregiver_user_id in caregiver_filter:
                patient_caregivers.append(possible_caregiver)

        return patient_caregivers

    def get_patient_providers(self, patient_id: str) -> list[UserRecord]:

        patient_record: UserRecord = self.get_user(patient_id)
        all_users = self.get_all_users()
        provider_filter: list[str] = patient_record['medical_providers']

        patient_providers: list[UserRecord] = []

        for possible_provider in all_users:
            provider_user_id = possible_provider['user_id']
            if provider_user_id in provider_filter:
                patient_providers.append(possible_provider)

        return patient_providers

    def get_provider_patients(self, provider_id: str) -> list[UserRecord]:

        all_users = self.get_all_users()

        patients: list[UserRecord] = []

        for possible_patient in all_users:
            provider_ids: list[str] = possible_patient['medical_providers']
            if provider_id in provider_ids:
                patients.append(possible_patient)

        return patients

    def get_caregiver_patients(self, care_giver_id: str) -> list[UserRecord]:

        all_users = self.get_all_users()

        patients: list[UserRecord] = []

        for possible_patient in all_users:
            caregiver_identifiers: list[str] = possible_patient['caregivers']
            if care_giver_id in caregiver_identifiers:
                patients.append(possible_patient)

        return patients