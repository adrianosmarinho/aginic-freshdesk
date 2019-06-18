ECHO OFF
ECHO Executing ticket_gen.py ...
py ticket_gen.py -n 10 -o 18-jun.json
ECHO Finished executing ticket_gen.py!
ECHO Executing freshdesk_json_to_sql.py ...
py freshdesk_json_to_sql.py "18-jun.json" "new_freshdesk.db"
ECHO Finished executing freshdesk_json_to_sql.py!
ECHO Executing selects.py ...
py selects.py "new_freshdesk.db"
ECHO Finished executing selects.py!
PAUSE