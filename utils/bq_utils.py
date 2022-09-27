import logging
import pandas as pd
from google.oauth2 import service_account
from utils.config import get_config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

config = get_config()


def fetch_data_bigquery(query):
    # Run a Standard SQL query with the project set explicitly
    credentials = service_account.Credentials.from_service_account_file(config['gcp_path_to_private_key'])
    project_id = config['gcp_project_id']
    df = pd.read_gbq(query, project_id=project_id, dialect='standard', credentials=credentials)
    return df


def fetch_release_data(days_ago=90):
    query = f"SELECT * FROM `bigquery-public-data.google_cloud_release_notes.release_notes` WHERE published_at >= DATE_ADD(CURRENT_DATE(), INTERVAL -{days_ago} DAY)"
    result = fetch_data_bigquery(query)
    return result


if __name__ == '__main__':
    data = fetch_release_data(7)
    fo="me"