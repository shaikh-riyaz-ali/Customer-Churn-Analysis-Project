import os

from utils.logger import logger

def config_load(df, filename):

    try:

        os.makedirs("data/processed", exist_ok=True)

        path = f"data/processed/{filename}"

        df.to_csv(path, index=False)

        logger.info(f"Data sucessfully loaded to {path}")

    except Exception as e:

        logger.error(f"Data load failed: {str(e)}")

        raise

                    
        