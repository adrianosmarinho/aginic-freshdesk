import sqlite3
import json

class FreshdeskJsonToSQLConverter:
    """ A converter to transform the Json data provided by Aginic into a Relational Database """

    def __init__(self, database_filename, json_filename):
        self._database_filename = database_filename
        self._json_filename = json_filename

    def drop_table(self, table_name):
        drop_table_script = "DROP TABLE IF EXISTS " + table_name
        with sqlite3.connect(self._database_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(drop_table_script)
            connection.commit()

    def create_table_metadata(self):
        create_table_script = """
            CREATE TABLE IF NOT EXISTS METADATA (
                START_AT DATETIME,
                END_AT DATETIME,
                ACTIVITIES_COUNT INT
            )
        """ 
        with sqlite3.connect(self._database_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(create_table_script)
            connection.commit()

    def create_table_activities(self):
        create_table_script = """
            CREATE TABLE IF NOT EXISTS ACTIVITIES (
                PERFORMED_AT DATETIME,
                TICKET_ID INT,
                PERFORMER_TYPE VARCHAR(255),
                PERFORMER_ID INT,
                PRIMARY KEY(PERFORMED_AT, TICKET_ID)
            )
        """
        with sqlite3.connect(self._database_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(create_table_script)
            connection.commit()

    def create_table_activity_items(self):
        create_table_script = """
            CREATE TABLE IF NOT EXISTS ACTIVITY_ITEMS (
                PERFORMED_AT DATETIME,
                TICKET_ID INT,
                SHIPPING_ADDRESS VARCHAR(255),
                SHIPPING_DATE DATE,
                CATEGORY VARCHAR(255),
                ISSUE_TYPE VARCHAR(255),
                SOURCE INT,
                STATUS VARCHAR(255),
                PRIORITY INT,
                GROUP_ VARCHAR(255),
                REQUESTER INT,
                PRODUCT VARCHAR(255),
                PRIMARY KEY(PERFORMED_AT, TICKET_ID),
                FOREIGN KEY(PERFORMED_AT) REFERENCES ACTIVITIES(PERFORMED_AT),
                FOREIGN KEY(TICKET_ID) REFERENCES ACTIVITIES(TICKET_ID)
            )
        """
        with sqlite3.connect(self._database_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(create_table_script)
            connection.commit()

    def insert_into_table_metadata(self, metadata):
        insert_into_script = "INSERT OR IGNORE INTO METADATA VALUES (?, ?, ?)"
        with sqlite3.connect(self._database_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(insert_into_script, (metadata["start_at"], metadata["end_at"], metadata["activities_count"]))
            connection.commit()

    def insert_into_activities(self, activity_data):
        insert_into_script = "INSERT OR IGNORE INTO ACTIVITIES VALUES (?, ?, ?, ?)"
        
        with sqlite3.connect(self._database_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(insert_into_script, (activity_data["performed_at"], activity_data["ticket_id"], activity_data["performer_type"], activity_data["performer_id"]))
            connection.commit()

        self.insert_into_activity_items(activity_data["performed_at"], activity_data["ticket_id"], activity_data["activity"])

    def insert_into_activity_items(self, performed_at, ticket_id, activity_item):
        insert_into_script = """
            INSERT OR IGNORE INTO ACTIVITY_ITEMS VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        with sqlite3.connect(self._database_filename) as connection:
            cursor = connection.cursor()
            cursor.execute(insert_into_script,
                (performed_at, ticket_id, activity_item["shipping_address"], activity_item["shipping_date"],
                 activity_item["category"], activity_item["issue_type"], activity_item["source"], activity_item["status"],
                 activity_item["priority"], activity_item["group"], activity_item["requester"], activity_item["product"]
                ))
            connection.commit()

#testing

if __name__ == "__main__":
    print("hi")

    database_filename = "new_freshdesk.db"
    json_filename = "test.json"
    # creates the database
    converter = FreshdeskJsonToSQLConverter(database_filename, json_filename)
    converter.drop_table("METADATA")
    converter.drop_table("ACTIVITIES")
    converter.drop_table("ACTIVITY_ITEMS")
    converter.create_table_metadata()
    converter.create_table_activities()
    converter.create_table_activity_items()

    #reads the json file and populates the database
    with open(json_filename) as json_file:  
        data = json.load(json_file)
        print(data["metadata"])
        print("inserting into metadata")
        converter.insert_into_table_metadata(data["metadata"])
        print("inserting into activities")
        for activity_data in data["activities_data"]:
            converter.insert_into_activities(activity_data)
