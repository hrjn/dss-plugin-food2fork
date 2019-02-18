
import dataiku
import logging
import requests
import json

from dataiku.customrecipe import *

BASE_URL = "https://www.food2fork.com/api/"


logging.basicConfig(format="%(asctime)s [%(levelname)s] %(message)s")
logging.getLogger().setLevel(logging.INFO)

logging.info("Preparing output dataset...")
output_dataset_name = get_output_names_for_role("output_role")[0]
output_dataset = dataiku.Dataset(output_dataset_name)
output_schema = [{"name": "id", "type": "string"},
                 {"name": "title", "type": "string"},
                 {"name": "ingredients", "type": "string"}]
output_dataset.write_schema(output_schema)

logging.info("Fetching parameters...")
recipe_config = get_recipe_config()
nb_max_search = int(recipe_config.get("nb_max_search"))
meal_type = recipe_config.get("meal_type")

logging.info("Retrieving API key..")
client = dataiku.api_client()
# Leverage user secrets for properly accessing API key:
auth_info = client.get_auth_info(with_secrets=True)
api_key = None
for secret in auth_info["secrets"]:
    if secret["key"] == "food2fork":
        api_key = secret["value"]
        break
if not api_key:
    raise Exception("Secret not found!")

logging.info("Querying the SEARCH endpoint...")
search_endpoint = BASE_URL + "search"
params = {"key": api_key, "q": meal_type, "count": nb_max_search}
req_search = requests.post(search_endpoint, data=params)
search_output = json.loads(req_search.text)

logging.info("Processing and forwarding to the GET endpoint...")
get_endpoint = BASE_URL + "get"
final_outputs = [{"id": rcp["recipe_id"],
                  "title": rcp["title"]} for rcp in search_output["recipes"]]

logging.info("Writing results in output dataset...")
writer = output_dataset.get_writer()
for output in final_outputs:
    req_ing = requests.post(get_endpoint, data={"key": api_key, "rId": output["id"]})
    resp = json.loads(req_ing.text)
    output["ingredients"] = resp["recipe"]["ingredients"]
    writer.write_row_dict(output)
writer.close()
