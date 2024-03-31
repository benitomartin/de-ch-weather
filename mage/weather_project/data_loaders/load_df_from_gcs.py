from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
import os
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from dotenv import load_dotenv

load_dotenv()

@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Template for loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """

    now = kwargs.get("execution_date")
    now_fpath = now.strftime("%Y/%m/%d")

    print(now.date())
    print(now.strftime("%Y/%m/%d"))

    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    GCS_BUCKET = os.environ["GCS_BUCKET"]  

    bucket_name = GCS_BUCKET
    object_key = f'{now_fpath}/daily_weather.parquet'

    return GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).load(
        bucket_name,
        object_key,
    )