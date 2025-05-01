from utils.cosmos_db_utils import CosmosDbUtils

cosmos_utils = CosmosDbUtils("users")


users = cosmos_utils.get_all_items(max_item_count=2)
# print(users)

single_user = cosmos_utils.get_single_item("3003", "3003")
#print(single_user)

patched_user = cosmos_utils.patch_item(item="3003",
    partition_key="3003",
    patch_operations=[
        {"op": "set", "path": "/last_name", "value": "Ward7"},
    ])

#print(patched_user)