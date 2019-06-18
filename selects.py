import json
import sqlite3
import sys

SECONDS_TO_DAYS = 86400
TIME_NOT_APPLICABLE = "N/A"


def compute_time_difference(database_filename, str_time_end, str_time_start):
    """
    """
    with sqlite3.connect(database_filename) as connection:
        cursor = connection.cursor()
        select_script = "SELECT strftime('%s', '" + str_time_end +"') - strftime('%s', '" + str_time_start +"')"
        cursor.execute(select_script)
        time = cursor.fetchone()
        time = time[0] / SECONDS_TO_DAYS
        #since we can return N/A, ensure time is a str
        time = '{:.2f}'.format(time)
        return time

def get_time_category_or_now(ticket, category):
    """
    """
    if category not in ticket:
        time_category = 'now'
    else:
        time_category = ticket[category]

    return time_category

def compute_time_spent_open(ticket):
    """
    """
    if "Open" not in ticket:
        return TIME_NOT_APPLICABLE

    time_opened = ticket["Open"]
    time_closed = get_time_category_or_now(ticket, "Closed")
    time_difference = compute_time_difference("new_freshdesk.db", time_closed, time_opened)
    return time_difference

def compute_time_waiting_for_customer(ticket):
    """
    """
    if "Waiting for Customer" not in ticket:
        return TIME_NOT_APPLICABLE

    time_customer_entry = ticket["Waiting for Customer"]
    time_pending = get_time_category_or_now(ticket, "Pending")
    time_difference = compute_time_difference("new_freshdesk.db", time_pending, time_customer_entry)
    return time_difference

def compute_time_waiting_for_response(ticket):
    """
    """
    if "Pending" not in ticket:
        return TIME_NOT_APPLICABLE

    time_pending = ticket["Pending"]
    time_resolved = get_time_category_or_now(ticket, "Resolved")
    time_difference = compute_time_difference("new_freshdesk.db", time_resolved, time_pending)
    return time_difference

def compute_time_till_resolution(ticket):
    """
    """
    if "Open" not in ticket:
        return TIME_NOT_APPLICABLE

    time_opened = ticket["Open"]
    
    if "Resolved" not in ticket:
        time_resolved = 'now'
    else:
        time_resolved = ticket["Resolved"]

    time_difference = compute_time_difference("new_freshdesk.db", time_resolved, time_opened)
    return time_difference
   
if __name__ == "__main__":
    database_filename = sys.argv[1]

    # opens a database (sqlite3)
    with sqlite3.connect(database_filename) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT PERFORMED_AT, TICKET_ID, STATUS FROM ACTIVITY_ITEMS")
        rows = cursor.fetchall()
        tickets = {}

        for row in rows:
            performed_at = row[0]
            ticket_id = row[1]
            status = row[2]
            if ticket_id not in tickets:
                tickets[ticket_id] = {}
                tickets[ticket_id][str(status)] = performed_at
            else:
                tickets[ticket_id][str(status)] = performed_at
        #commit the changes
        connection.commit()
    
    print(tickets)

    print("|\tticket_id\t|\ttime_spent_open\t|\ttime_spent_waiting_on_customer\t|\ttime_spent_waiting_for_response\t|\ttime_till_resolution\t|\ttime_to_first_response\t|")
    for ticket_id, ticket_status_dict in tickets.items():
        time_spent_open = compute_time_spent_open(tickets[ticket_id])
        time_waiting_for_customer = compute_time_waiting_for_customer(tickets[ticket_id])
        time_waiting_for_response = compute_time_waiting_for_response(tickets[ticket_id])
        time_spent_till_resolution = compute_time_till_resolution(tickets[ticket_id])
        print("|\t{:d}\t|\t{:s}\t|\t{:s}\t|\t{:s}\t|\t{:s}\t|\ttime_to_first_response\t|".format(ticket_id, time_spent_open, time_waiting_for_customer, time_waiting_for_response, time_spent_till_resolution))
