'''
Created by savavel

Last Modified: 2019-05-05 22:46

Authenticates with Opsview Master and edits 
SNMP Community string for many Opsview Hosts via REST API.

Requires:
 - Opsview Admin credentials
 - Opsview Endpoint URL
 - New SNMP Community String
 - Exported Hosts JSON file from the UI

'''



import sys
import requests
import json
import datetime
from pprint import pprint

if len(sys.argv) < 6:
    print
    print "Not enough arguments supplied."
    print "Please ensure you have specified the following:"
    print 
    print "Usage:"
    print "python opsview_update_snmp_community.py   [Opsview URL]   [Auth Username]  [Auth Password]   [SNMP Community]   [JSON source file]"
    print 
    sys.exit(0)


# Opsview Master Base URL
# Change this to point to your server address, can be http/https
url = sys.argv[1]

# Authentication Credentials
# Change these to reflect the Opsview credentials you use for editing the host configuration
auth_username = sys.argv[2]
auth_password = sys.argv[3]

# The SNMP community string to use
snmp_community_str = sys.argv[4]

# Source file to read the hostnames from
source_file = sys.argv[5]

# REST API login URL
url_login = url + '/rest/login' 

# REST API edit host URL with encrypted SNMP as output
query_url = url + '/rest/config/host?include_encrypted=1'

log_output_file = open('update_snmp_community-'+ datetime.datetime.today().strftime('%Y-%m-%d') + '.log', "w")


# BEGIN LOGIN ---------------------------------------------------
data = {'username': auth_username,'password': auth_password}
data_json= json.dumps(data)
headers = {'Content-type': 'application/json'}

# Get the Authentication token
response = requests.post(url_login, data=data_json, headers=headers)
if response.status_code != 200:
    print "Error authenticating, please check your credentials"
    sys.exit()

response_data = json.loads(response.text)
token = response_data.get('token')
print "Authentication Successful"
print "Token: "+ response_data.get('token')
print 

# END LOGIN ----------------------------------------------------



# BEGIN UPDATE HOSTS SNMP STR ---------------------------------

# Read hostsnames list
with open(source_file) as json_file:
    host_json = json.load(json_file)

query_headers = {'Content-type': 'application/json', 'X-Opsview-Username': auth_username, 'X-Opsview-Token': token}
hostcount = 0

# Iterate over the hosts and update the snmp_community for each
for host in host_json:
    hostname = host.get('name').encode('utf-8')
    print "EDITING: "+ hostname
    log_output_file.write(str(datetime.datetime.now()) +"\nEDITING: "+ hostname +"\nUSING SNMP: "+ snmp_community_str +"\n")

    query_data = {'name': hostname, 'snmp_community': snmp_community_str}
    query_data_json = json.dumps(query_data)

    query_response = requests.put(query_url, data=query_data_json, headers=query_headers)

    if response.status_code != 200:
        print "Error authenticating, please check your credentials"
        sys.exit()

    hostcount += 1
    log_output_file.write(query_response.text + "\n\n")

# END UPDATE HOSTS SNMP STR ---------------------------------
print
print "Finished editing hosts"
print "Total hosts edited: "+ str(hostcount)
