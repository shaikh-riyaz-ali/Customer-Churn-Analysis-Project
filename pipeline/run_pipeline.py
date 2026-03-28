import pandas as pd
from utils.logger import logger

from load.config_load import config_load
from transform.clean_data import clean_data
from extract.extract import extract

def run_pipeline():

    logger.info("pipeline started")

    data = extract()

    data = clean_data(data)

    config_load(data, "clean_csv")

    logger.info("pipeline completed successfully")

if __name__ == "__main__":
    run_pipeline()