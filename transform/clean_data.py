
import pandas as pd
from utils.logger import logger
from utils.load_config import load_config

rules = load_config("config/business.yaml")

def clean_data(df):

    logger.info("pipeline started")

    data = rules['data']

    # Clean column names
    df.columns = df.columns.str.strip()
    logger.info("Column names whitespace removed")

    # -----------------------------------------
    # Apply mappings FIRST
    # -----------------------------------------

    if "gender_mappings" in data:
        df['gender'] = df['gender'].replace(data['gender_mappings'])

    if "churn_mappings" in data:
        df['churn'] = df['churn'].replace(data['churn_mappings'])

    if "contract_mappings" in data:
        df['contract_type'] = df['contract_type'].replace(data['contract_mappings'])

    logger.info("Mappings applied")

    # -----------------------------------------
    # Datatype conversion
    # -----------------------------------------

    datatype = data["data_types"]
    date_config = data["date_parsing"]

    for col, dtype in datatype.items():

        if col in df.columns:
            try:

                # Datetime
                if dtype == "datetime":

                    formats = date_config["formats"]
                    temp_col = pd.Series([pd.NaT] * len(df))

                    for fmt in formats:
                        parsed = pd.to_datetime(df[col], format=fmt, errors="coerce")
                        temp_col = temp_col.fillna(parsed)

                    df[col] = temp_col
                    logger.info(f"{col} parsed using multiple formats")

                # Integer
                elif dtype == "int":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

                # Float
                elif dtype == "float":
                    df[col] = pd.to_numeric(df[col], errors="coerce").astype(float)

                # String
                elif dtype == "str":
                    df[col] = df[col].astype(str).str.strip().str.lower().str.title()

                logger.info(f"{col} converted to {dtype}")

            except Exception as e:
                logger.error(f"Datatype conversion failed for {col}: {str(e)}")

    # -----------------------------------------
    # Fill missing values
    # -----------------------------------------

    if "fillna" in data:

        for col, value in data['fillna'].items():

            if col in df.columns:

                missing_before = df[col].isnull().sum()

                if value == "median":
                    df[col] = df[col].fillna(df[col].median())
                else:
                    df[col] = df[col].fillna(value)

                logger.info(f"{missing_before} nulls filled in {col}")

    # -----------------------------------------
    # Remove duplicates
    # -----------------------------------------

    before = len(df)
    df = df.drop_duplicates()
    logger.info(f"Duplicates removed: {before - len(df)}")

    # -----------------------------------------
    # Drop critical nulls
    # -----------------------------------------

    if "drop_na" in data:

        subset = data['drop_na']['subset']
        before = len(df)

        df = df.dropna(subset=subset)

        logger.info(f"Critical null rows removed: {before - len(df)}")

    # Final churn fix
    df['churn'] = df['churn'].replace({"False": "No", "True": "Yes"})

    df['signup_date'] = df['signup_date'].fillna(
    pd.Timestamp.today() - pd.to_timedelta(df['tenure'] * 30, unit='D')
)

    logger.info("Data cleaning completed")

    return df