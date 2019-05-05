# Opsview-REST-API-update_snmp_community_string
Update Opsview SNMP Community string on many Hosts via REST API


1. Export the hosts in question from the Opsview UI: 
1.1. Go to 'Settings' -> 'Hosts' -> 'List' and filter the list depending on your requirements. Please filter by common configuration such as 'Host Template', 'Host Group', 'IP Address prefix' or 'Components' 
1.2. Click on Export and choose 'JSON' format since the Python script only accepts this format to read from 
1.3. Wait some time for Opsview to create the file and download it. This will depend on the amount of hosts you are exporting. 

2. Place the python script on a machine which has network access to the Opsview Master via HTTP/HTTPS and has python 2.7 installed 

3. Run the script with the following arguments: 
- Opsview URL - e.g. https://127.0.0.1 
- Auth Username - e.g. admin (needs to have write access to the API) 
- Auth Password - e.g. password 
- SNMP Community string - e.g. public (the SNMP string you want your hosts to be updated with) 
- JSON source file - e.g. Host.json (the script needs to have permissions to read the file) 
example of running the command: 

$ python opsview_update_snmp_community.py https://127.0.0.1 admin password public Host.json 

4. The script will iterate over your JSON file with your hosts, change the SNMP Community string and encrypt it. This will take a while depending on how many hosts you have, for 2000 hosts ~15mins 

5. After the script completes, go to the Opsview UI, in the 'Host Settings' page, you will see there's all of the hosts in question with changes pending. 

6. Perform a Reload action which will take some time depending on how many hosts you have edited and the amount of service checks they have. In my testing 2000 hosts with 12 000 checks take 30 mins to Reload, so wait for this to finish. 

Your system should then have all of the SNMP checks go through. You can run the script as many times as you want as long as you perform a single reload at the end. 

The script generates a log file in the same directory which you can inspect if there are any issues in the process. 
