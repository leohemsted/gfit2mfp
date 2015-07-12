import os

import arrow

FILENAME = 'last_run.txt'

def retrieve_last_run():
    """
    Gets the previous timestamp from the last_run file. Creates the file if it doesn't exist.
    """
    if not os.path.isfile(FILENAME):
        return update_last_run()
    else:
        with open(FILENAME, 'r') as last_run:
            return arrow.get(last_run.read()).datetime

def update_last_run():
    """
    Stores the current timestamp in the last_run file. Creates the file if it doesn't exist.
    """
    # append+ so it creates if it doesn't exist
    with open(FILENAME, 'w+') as last_run:
        timestamp = arrow.utcnow()
        last_run.write(timestamp.isoformat())
        return timestamp.datetime
