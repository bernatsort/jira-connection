"""
This script demonstrates how to authenticate with a Jira instance using an API token and make a GET request to retrieve information. 
It then prints out details about the response, including the status code, headers, URL, and encoding.
"""
import requests
import pandas as pd
import json 

# https://github.com/pycontribs/jira/issues/1497
# https://community.atlassian.com/t5/Jira-questions/How-to-use-API-token-for-REST-calls-in-Python/qaq-p/760940
# https://medium.com/@metechsolutions/python-by-examples-jira-access-e87771a26dfb

# Define the URL of the Jira instance
url = "https://jira.biscrum.com" 
# Define the API token for authentication
api_token = "your_jira_token" #'your-personal-access-token'

# useremail = "your_email"
# auth = useremail + ":" + api_token
# auth = HTTPBasicAuth(useremail, api_token)

# Define headers for the request, including the authorization header with the API token
"""
1. `"Accept": "application/json"`:
   - This header specifies the media types that are acceptable for the response. 
   - In this case, it indicates that the client (your Python script) prefers to receive JSON-formatted responses from the server. 
   - This is a common practice in RESTful API interactions, as JSON is a widely used format for exchanging data between clients and servers.

2. `"Authorization": "Bearer " + api_token`:
   - This header is used for authentication purposes. 
   - It includes the access token required to authenticate the client (your Python script) with the Jira server. 
   - The `Bearer` keyword indicates that the token being provided is a bearer token, which is a type of access token commonly used for OAuth 2.0 authentication. 
   - The `api_token` variable contains the actual token value. In the context of OAuth 2.0 authentication, which is commonly used for securing APIs, 
     a bearer token is a type of access token that is used by the client (your Python script) to access protected resources on behalf of a user. 
     The term "bearer" indicates that the token itself is sufficient proof of authentication, meaning that whoever possesses the token can access the protected resources without further authentication checks.

When the request is sent to the Jira server, these headers are included in the HTTP request headers. 
The `"Accept"` header informs the server about the expected format of the response, while the `"Authorization"` header provides the necessary credentials for authentication.
"""
headers = {
    "Accept": "application/json"
    # ,"Content-Type": "application/json"
    ,"Authorization": "Bearer " + api_token 
}

# Make a GET request to the Jira URL with the specified headers
response = requests.get(
                        url, 
                        headers=headers 
                        # ,verify=False
                        )

# Print out the status code, headers, URL, the encoding and the content of the response
print("Response Status Code:", response.status_code)
print("\n")
print("Response Headers:", response.headers)
print("\n")
print("Request URL:", response.url)
print("\n")
print("Response Encoding:", response.encoding)
print("\n")
# print("Raw Content:", response.text) # response.content
# print("\n")

# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Connection to Jira successful!")
else:
    print("Failed to connect to Jira. Status code:", response.status_code)


# Mention the JQL query. 
# Here, all issues, of a project, are 
# fetched,as,no criteria is mentioned. 
query = { 
    'jql': 'project = OMACL and fixVersion =0.1 and cf[25144] = Quality  AND resolution = Unresolved ORDER BY priority DESC, updated DESC'
} 
  
# Create a request object with above parameters. 
response = requests.request( 
    "GET", 
    url, 
    headers=headers, 
    #auth=auth, 
    params=query 
) 
print(response)
# Check if the request was successful (status code 200)
if response.status_code == 200:
    print("Connection to Jira successful!")
else:
    print("Failed to connect to Jira. Status code:", response.status_code)

# Get all project issues,by using the 
# json loads method. 
projectIssues = json.dumps(json.loads(response.text), 
                           sort_keys=True, 
                           indent=4, 
                           separators=(",", ": ")) 
  
# The JSON response received, using 
# the requests object, 
# is an intricate nested object. 
# Convert the output to a dictionary object. 
dictProjectIssues = json.loads(projectIssues) 
  
# We will append,all issues,in a list object. 
listAllIssues = [] 
  
# The Issue details, we are interested in, 
# are "Key" , "Summary" and "Reporter Name" 
keyIssue, keySummary, keyReporter = "", "", "" 
  
  
def iterateDictIssues(oIssues, listInner): 
  
    # Now,the details for each Issue, maybe 
    # directly accessible, or present further, 
    # in nested dictionary objects. 
    for key, values in oIssues.items(): 
  
        # If key is 'fields', get its value, 
        # to fetch the 'summary' of issue. 
        if(key == "fields"): 
  
            # Since type of object is Json str, 
            # convert to dictionary object. 
            fieldsDict = dict(values) 
  
            # The 'summary' field, we want, is  
            # present in, further,nested dictionary 
            # object. Hence,recursive call to  
            # function 'iterateDictIssues'. 
            iterateDictIssues(fieldsDict, listInner) 
  
        # If key is 'reporter',get its value, 
        # to fetch the 'reporter name' of issue. 
        elif (key == "reporter"): 
  
            # Since type of object is Json str  
            # convert to dictionary object. 
            reporterDict = dict(values) 
  
            # The 'displayName', we want,is present 
            # in,further, nested dictionary object. 
            # Hence,recursive call to function 'iterateDictIssues'. 
            iterateDictIssues(reporterDict, listInner) 
  
        # Issue keyID 'key' is directly accessible. 
        # Get the value of key "key" and append 
        # to temporary list object. 
        elif(key == 'key'): 
            keyIssue = values 
            listInner.append(keyIssue) 
  
        # Get the value of key "summary",and, 
        # append to temporary list object, once matched. 
        elif(key == 'summary'): 
            keySummary = values 
            listInner.append(keySummary) 
  
        # Get the value of key "displayName",and, 
        # append to temporary list object,once matched. 
        elif(key == "displayName"): 
            keyReporter = values 
            listInner.append(keyReporter) 
  
  
# Iterate through the API output and look 
# for key 'issues'. 
for key, value in dictProjectIssues.items(): 
  
    # Issues fetched, are present as list elements, 
    # against the key "issues". 
    if(key == "issues"): 
  
        # Get the total number of issues present 
        # for our project. 
        totalIssues = len(value) 
  
        # Iterate through each issue,and, 
        # extract needed details-Key, Summary, 
        # Reporter Name. 
        for eachIssue in range(totalIssues): 
            listInner = [] 
  
            # Issues related data,is nested  
            # dictionary object. 
            iterateDictIssues(value[eachIssue], listInner) 
  
            # We append, the temporary list fields, 
            # to a final list. 
            listAllIssues.append(listInner) 

# Print listAllIssues for debugging and insoecting the structurre of the data
print("listAllIssues", listAllIssues)

# Prepare a dataframe object,with the final  
# list of values fetched. 
dfIssues = pd.DataFrame(listAllIssues, columns=["Reporter", 
                                                "Email",
                                                "Summary", 
                                                "Key"]) 
  
# Reframing the columns to get proper  
# sequence in output. 
columnTiles = ["Key", "Summary", "Email", "Reporter"] 
dfIssues = dfIssues.reindex(columns=columnTiles) 
print(dfIssues) 