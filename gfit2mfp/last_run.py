import arrow

def update_last_run():
    """
    Retrieves the last
    """
    with open('last_run.txt', 'r') as last_run:
        old_timestamp = arrow.get(last_run.read())
        last_run.truncate()
        last_run.write(arrow.now().isoformat())
        return old_timestamp.date
