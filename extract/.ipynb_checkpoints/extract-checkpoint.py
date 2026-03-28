import pandas as pd
from utils.logger import logger

def extract():

    logger.info("data extraction started")

    data = pd.read_csv(r"D:\customer chrun\data\raw\messy_customer_churn_100k.csv")

    logger.info("data extraction completed")

    return data