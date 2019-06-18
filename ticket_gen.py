import sys
import json
from datetime import datetime, date

def parse_arguments():
    arguments = {}
    try:
        if (len(sys.argv) != 5):
            print("ERROR: Invalid arguments. Please type: py ticket_gen.py -n <number_of_activites> -o <output_file.json>")
        else:
            number_of_activities = parse_number_of_activities()
            arguments["number_of_activities"] = number_of_activities
            output_filename = parse_output_filename()
            arguments["output_filename"] = output_filename
    except ValueError as error:
            print("ERROR: " + error.args[0])
            print("You informed: " + error.args[1])
            raise
    finally:
        return arguments
            

def parse_number_of_activities():
    if sys.argv[1] != "-n":
        raise ValueError("The flag '-n' is not present.", sys.argv[1])

    if int(sys.argv[2]) > 0:
        number_of_activities = int(sys.argv[2])
        return number_of_activities
    else:
        raise ValueError("The number of activities must be a positive integer.", sys.argv[2])


def parse_output_filename():
    if sys.argv[3] != "-o":
        raise ValueError("The flag '-o' is not present.", sys.argv[3])

    if(sys.argv[4].endswith(".json")):
        output_filename = sys.argv[4]
        return output_filename
    else:
        raise ValueError("Incorrect file type.", sys.argv[4])

def get_json_encodable_version_from(the_object):
    if isinstance(the_object, (datetime, date)):
        return the_object.__str__()

def generate_random_product_category(category_and_product_id):
    product_categories = ["Game", "Phone"]
    index = category_and_product_id
    return product_categories[index]

def generate_random_product(faker, category_id):
    products ={
        0: ["PS4 Game", "X-Box Game"],
        1: ["mobile", "landline"]
    }
    index = faker.pyint(0, 1)
    return products[category_id][index]

def generate_random_issue_type(faker):
    issue_types = ["Incident", "Request", "Change", "Problem"]
    index = faker.pyint(0, 3)
    return issue_types[index]

def generate_random_status(faker):
    status_types = ["Open", "Closed", "Resolved", "Waiting for Customer", "Waiting for Third Party", "Pending"]
    index = faker.pyint(0, 5)
    return status_types[index]

def generate_random_group(faker):
    group_types = ["refund", "request", "problem"]
    index = faker.pyint(0, 2)
    return group_types[index]

def generate_activity_items(faker, performed_at, end_date, performer_type_and_source_id):
    activity_items = {}
    activity_items["note"] = generate_random_note(faker)
    activity_items["shipping_address"] = faker.address()
    activity_items["shipping_date"] = faker.date_between(start_date=performed_at, end_date=end_date)
    category_and_product_id =  faker.pyint(0, 1)
    activity_items["category"] = generate_random_product_category(category_and_product_id)
    activity_items["issue_type"] = generate_random_issue_type(faker)
    activity_items["source"] = performer_type_and_source_id
    activity_items["status"] =  generate_random_status(faker)
    activity_items["priority"] = faker.pyint(0, 4)
    activity_items["group"] = generate_random_group(faker)
    activity_items["requester"] = faker.pyint()
    activity_items["product"] = generate_random_product(faker, category_and_product_id )
    return activity_items

def generate_random_note(faker):
    note = {}
    note["id"] = faker.pyint()
    note["type"] = faker.pyint(0, 4)
    return note

def generate_activity_data(faker, start_date, end_date, max_ticket_id):
    performer_types = ["customer", "third party", "user"]
    activity_data = {}
    activity_data["performed_at"] = faker.date_time_between(start_date=start_date, end_date=end_date, tzinfo=None)
    activity_data["ticket_id"] = faker.pyint(0, max_ticket_id)

    performer_type_and_source_id = faker.pyint(0, 2)
    activity_data["performer_type"] = performer_types[performer_type_and_source_id]
    activity_data["performer_id"] = faker.pyint()
    activity_items = generate_activity_items(faker, activity_data["performed_at"], end_date, performer_type_and_source_id)
    activity_data["activity"] = activity_items
 

    return activity_data

from faker import Faker

if __name__ == "__main__":
    arguments = parse_arguments()

    if ("number_of_activities" in arguments) and ("output_filename" in arguments):

        #future json file
        activities = {}
        faker = Faker('en_AU')

        # build activities metadata
        metadata_start_at = faker.date_time_between(start_date="now", end_date="+2y", tzinfo=None)
        metadata_end_at = faker.date_time_between(start_date=metadata_start_at, end_date="+20y", tzinfo=None)
        metadata_activities_count = arguments["number_of_activities"]
        
        activities["metadata"] = {
            "start_at" : metadata_start_at,
            "end_at": metadata_end_at,
            "activities_count" : metadata_activities_count
        }

        # build activities item
        activities["activities_data"] = []
        for i in range(arguments["number_of_activities"]):
            current_activity = generate_activity_data(faker, activities["metadata"]["start_at"], activities["metadata"]["end_at"], arguments["number_of_activities"]//2)
            activities["activities_data"].append(current_activity)

        #write activities to a json file
        with open(arguments["output_filename"], 'w') as output_file:  
            json.dump(activities, output_file, indent=4, default=get_json_encodable_version_from)

    else:
        print("something went wrong with your arguments")

