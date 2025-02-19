from argparse import ArgumentParser
from datetime import datetime, timedelta
import pandas as pd


from src.components import feature_group_config as config
from src.components.data_info import fetch_demand_values_from_data_warehouse
from src.components.feature_store_api import get_or_create_feature_group
from src.logger import get_logger

logger = get_logger()

def run(date: datetime):
    """
    """
    demand_values = fetch_demand_values_from_data_warehouse(from_date=(date-timedelta(days=28)),to_date=date)

    # add new column with the timestamp in Unix seconds
    logger.info('Adding column `seconds` with Unix seconds...')
    demand_values['date'] = pd.to_datetime(demand_values['date'], utc=True)
    demand_values['seconds'] = demand_values['date'].astype(int)// 10 ** 6

    # get a pointer to the feature group we wanto to write to
    logger.info('Getting pointer to the feature group we waant to save data to.')
    feature_group = get_or_create_feature_group(config.FEATURE_GROUP_METADATA)

    # start a job to insert the data into the feature group
    # we wait to make sure the job is finished before we exit the script, and
    # the inference pipeline can start using the new data
    logger.info('Starting job to insert data into feature group...')
    feature_group.insert(demand_values, write_options={'start_offline_backfill': False})

    logger.info('Finished jon to insert data into  feature group')


if __name__ == "__main__":
    # parse command line commands
    parser = ArgumentParser()
    parser.add_argument('--datetime', type=lambda s: datetime.strptime(s, "%Y-%m-%d %H:%M:%S"),
                        help='Datetime argument in the format of YYYY-MM-DD HH:MM:SS')
    args = parser.parse_args()

    # if args.datetime was provided use it as the current_date, otherwise
    # use the current datetime in UTC
    if args.datetime:
        current_date = pd.to_datetime(args.datetime)
    else:
        current_date = pd.to_datetime(datetime.utcnow()).floor('H')

    logger.info(f'Running feature pipeline for {current_date=}')
    run(current_date)
