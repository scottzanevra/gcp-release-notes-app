import logging
import os
import pandas as pd
from google.oauth2 import service_account

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get environment variables
GCP_PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'dataplex-demo-342803')
PATH_TO_PRIVATE_KEY = os.environ.get('PATH_TO_PRIVATE_KEY',
                                '/Users/szanevra/Downloads/dataplex-demo-342803-e2b0cc499e2a.json')

# Set environment variables
os.environ['CONFIG_FILE'] = 'config.yml'


def fetch_data_bigquery(query):
    # Run a Standard SQL query with the project set explicitly
    credentials = service_account.Credentials.from_service_account_file(PATH_TO_PRIVATE_KEY)
    df = pd.read_gbq(query, project_id=GCP_PROJECT_ID, dialect='standard', credentials=credentials)
    return df


def fetch_release_data(days_ago=90):
    query = f"SELECT * FROM `bigquery-public-data.google_cloud_release_notes.release_notes` " \
            f"WHERE published_at >= DATE_ADD(CURRENT_DATE(), INTERVAL -{days_ago} DAY)"
    result = fetch_data_bigquery(query)
    return result


if __name__ == '__main__':
    data = fetch_release_data(7)
    fo="me"