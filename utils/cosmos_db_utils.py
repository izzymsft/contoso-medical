import os
import re
from typing import Any, Iterable, Dict, Union, List, Literal
from azure.cosmos import CosmosClient, DatabaseProxy, ContainerProxy, PartitionKey, CosmosDict
from azure.cosmos.container import PartitionKeyType


ValidCosmosCollectionNames = Literal["users", "medical_records", "facilities", "employment_records"]

def remove_non_alphanumeric(input_str):
    # Use re.sub() to remove all non-alphanumeric characters
    return re.sub(r'[\W_]', '', input_str)

class CosmosDbUtils:
    def __init__(self, collection: ValidCosmosCollectionNames):
        cosmos_connection_string = os.environ["COSMOS_CONNECTION"]
        cosmos_database_name_string = os.environ["COSMOS_DATABASE_NAME"]

        self.client: CosmosClient = CosmosClient.from_connection_string(conn_str=cosmos_connection_string)
        self.database_name: str = cosmos_database_name_string
        self.collection_name: str = collection

    def create_collection(self, partition_key_path: str):
        partition_key_path = PartitionKey(path=partition_key_path)
        container_identifier = self.collection_name
        self.get_database().create_container_if_not_exists(id=container_identifier, partition_key=partition_key_path)

    def get_database(self) -> DatabaseProxy:
        return self.client.get_database_client(self.database_name)

    def get_collection(self) -> ContainerProxy:
        return self.get_database().get_container_client(self.collection_name)

    def update_database_name(self, database_name: str):
        self.database_name = database_name
        return self

    def update_collection_name(self, collection_name: str):
        self.collection_name = collection_name
        return self

    def get_single_item(self, item_id: str, partition_key: Any | None = None) -> CosmosDict:
        """Returns a dictionary representing the item retrieved"""
        container_proxy = self.get_collection()
        single_item = container_proxy.read_item(item=item_id, partition_key=partition_key)
        return single_item

    def get_all_items(self, max_item_count: int | None = None) -> list[dict[str, Any]]:
        """Returns a list of all the items in the collection"""
        container_proxy = self.get_collection()
        all_items = container_proxy.read_all_items(max_item_count=max_item_count)

        return_list: list[dict[str, Any]] = []

        for item in all_items:
            return_list.append(item)

        return return_list

    def create_item(self, item: dict):
        """Returns a dictionary representing the item created"""
        container_proxy = self.get_collection()
        return container_proxy.create_item(item)

    def upsert_item(self, item: dict):
        """Returns a dictionary representing the item upserted"""
        container_proxy = self.get_collection()
        return container_proxy.upsert_item(item)

    def patch_item(self, item: Union[str, Dict[str, Any]], partition_key: PartitionKeyType,
                   patch_operations: List[Dict[str, Any]]):
        """
        Partially updates (patches) an item in the Cosmos DB container using the specified patch operations.

        Supported patch operations:
          - add: Adds a new property or appends to an array (fails if the property already exists)
          - replace: Replaces the value of an existing property (fails if the property does not exist)
          - remove: Removes an existing property
          - set: Adds or replaces the value of a property
          - incr: Increments a numeric property by a specified value

        Parameters:
            item (str or dict): The ID of the item to update, or the full item dict (must include 'id').
            partition_key (Any): The partition key value associated with the item.
            patch_operations (List[Dict[str, Any]]): A list of patch operations to apply.
                Each operation is a dict with keys: "op", "path", and "value".

        Returns:
            dict: The updated item from Cosmos DB.

        Example:
            self.patch_item(
                item="item_id_123",
                partition_key="customer_001",
                patch_operations=[
                    {"op": "add", "path": "/newField", "value": "newValue"},
                    {"op": "replace", "path": "/existingField", "value": 123},
                    {"op": "remove", "path": "/obsoleteField"},
                    {"op": "set", "path": "/status", "value": "active"},
                    {"op": "incr", "path": "/views", "value": 1}
                ]
            )
        """
        container_proxy = self.get_collection()
        return container_proxy.patch_item(item, partition_key=partition_key, patch_operations=patch_operations)

    def delete_item(self, item: dict[str, Any] | str, partition_key):
        container_proxy = self.get_collection()
        return container_proxy.delete_item(item, partition_key=partition_key)

    def query_container(self, query: str,
                        parameters: list[dict[str, object]] | None = None,
                        partition_key: Any | None = None,
                        enable_cross_partition_query: bool | None = None,
                        max_item_count: int | None = None):
        container_proxy = self.get_collection()

        results: Iterable[Dict[str, Any]] = container_proxy.query_items(query, parameters=parameters, partition_key=partition_key,
                                              enable_cross_partition_query=enable_cross_partition_query,
                                              max_item_count=max_item_count)

        return results