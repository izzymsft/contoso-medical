from models.contoso_medical import DataExtractor, Facility
from utils.cosmos_db_utils import CosmosDbUtils


class FacilityDao(DataExtractor):
    """
    Data Access Object (DAO) for retrieving and processing facility records
    from the 'facilities' container in Cosmos DB.

    Inherits from:
        DataExtractor: Provides helper methods to populate structured records from raw data.
    """

    def __init__(self):
        """
        Initializes the FacilityDao with a CosmosDbUtils instance
        targeting the 'facilities' container.
        """
        self.cosmos_util = CosmosDbUtils("facilities")

    def get_all_facilities(self) -> list[Facility]:
        """
        Retrieves all facility records from the database.

        Returns:
            list[Facility]: A list of all facilities.
        """
        search_results = self.cosmos_util.get_all_items(max_item_count=1024)
        all_records: list[Facility] = []

        for search_result in search_results:
            all_records.append(self.populate_facility(search_result))

        return all_records

    def get_facility_details(self, facility_id: str) -> Facility | None:
        """
        Retrieves details of a specific facility by its facility ID.

        Args:
            facility_id (str): The unique identifier of the facility.

        Returns:
            Facility | None: The facility record if found, otherwise None.
        """
        search_results = self.get_all_facilities()

        for search_result in search_results:
            if search_result['facility_id'] == facility_id:
                return search_result

        return None
