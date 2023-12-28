class MissedScript(Exception):
    def __str__(self):
        return 'One or more sql scripts are missing'


class UnregisteredScript(Exception):
    def __str__(self):
        return 'Attempt to execute an unregistered script. Add the script via add_sql_scripts'


class DatabaseNotExists(Exception):
    def __str__(self):
        return 'The database does not exist. Try to create it via create_db'
