from models.contoso_medical import DataExtractor, Facility
from utils.cosmos_db_utils import CosmosDbUtils


class FacilityDao(DataExtractor):

    def __init__(self):
        self.cosmos_util = CosmosDbUtils("facilities")

    def get_all_facilities(self) -> list[Facility]:
        search_results = self.cosmos_util.get_all_items(max_item_count=1024)
        all_records: list[Facility] = []

        for search_result in search_results:
            all_records.append(self.populate_facility(search_result))

        return all_records

    def get_facility_details(self, facility_id: str) -> Facility | None:

        search_results = self.get_all_facilities()

        for search_result in search_results:
            if search_result['facility_id'] == facility_id:
                return search_result

        return None
