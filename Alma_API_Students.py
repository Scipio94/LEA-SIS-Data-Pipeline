#!/usr/bin/env python
# coding: utf-8

# ## Alma API Students
# 
# Writing a code that communicates with the Alma url endpoint via an api to return student demographic data at each campus and uplaoding data extracted from the API to a BigQuery data warehousing software.

# In[1]:


#importing relevant packages
from google.cloud import bigquery #--> python client for bigquery
import pandas as pd
import requests
import json
from requests.auth import HTTPDigestAuth
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
import os


# In[2]:


env_file_path = '/Users/scipio/Alma_API_Scripts/ALMA_API.env'
google_auth_env_file_path = '/Users/scipio/Alma_API_Scripts/GOOG_AUTH.env'


# In[3]:


load_dotenv(dotenv_path = env_file_path )
load_dotenv(dotenv_path = google_auth_env_file_path)


# In[4]:


# retrieving releavnt variables from the .env file
API_KEY = os.getenv('API_KEY')
AUTH_SECRET = os.getenv('AUTH_SECRET')
google_credentials_path = os.getenv('GOOGLE_CREDENTIALS')


# **FCA Current School Year**: 65e8a8461e0c3dd517076bcf 
# 
# **363 Current School Year ID**: 664cc55127c6b4a81806658b

# In[5]:


# setting up BigQuery authentication
credentials = service_account.Credentials.from_service_account_file(google_credentials_path)

#initializing BigQuery client
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


# ### Extraction of Student Data FCA

# In[6]:


# Defining credential api_key and auth_secret 
api_key = API_KEY
auth_secret = AUTH_SECRET


# URL of the API endpoint FCA 2024-2025 SY
url= 'https://facs.api.getalma.com/v2/fca/students?schoolYearId=65e8a8461e0c3dd517076bcf' 

# Headers
headers = {
    'Content-Type':'application/json',
    'Accept':'application/json, application/problem+json'
}

# Make the GET request with Digest Authentication
response_fca = requests.get(url, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))

# Making response into a json object
r_fca = response_fca.json()

# Extracting value from r_fca
for key,value in r_fca.items():
    value #--> list of dictionaries

# coverting python object to a dataframe
df_r_fca = pd.DataFrame(value)

#data cleaning
df_r_fca = df_r_fca[df_r_fca['graduationYear']>2024] # --> filtering out seniors
df_r_fca['race'] = df_r_fca['race'].str[0] #--> making race a string
df_r_fca['languages'] = df_r_fca['languages'].str[0] #--> making langauges a string
df_r_fca['id'] = df_r_fca['id'].str.strip()


# function for race column
def race(row):
    
    """
    If a person's ehtincity is 'Hispanic Or Latino' so is their race
    """
    if row['ethnicity'] == 'Hispanic Or Latino':
        return 'Hispanic Or Latino'
    else:
        return row['race']
    
df_r_fca['race'] = df_r_fca.apply(race, axis = 1)


# ### Extraction of Student Data 363

# In[7]:


# Defining credential api_key and auth_secret 
api_key = API_KEY
auth_secret = AUTH_SECRET

# URL of the API endpoint FACS 2024-2025 SY
url= 'https://facs.api.getalma.com/v2/facs363/students?schoolYearId=664cc55127c6b4a81806658b' 

# Headers
headers = {
    'Content-Type':'application/json',
    'Accept':'application/json, application/problem+json'
}

# Make the GET request with Digest Authentication
response_363 = requests.get(url, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))

# Making response into a json object
r_363 = response_363.json()

# extracting value from r_363
for key,value in r_363.items():
    value #--> list of dictionaries
    

# coverting python object to a dataframe
df_r_363 = pd.DataFrame(value)

#data cleaning
df_r_363['race'] = df_r_363['race'].str[0]
df_r_363['languages'] = df_r_363['languages'].str[0]
df_r_363['id'] = df_r_363['id'].str.strip()

# function for race column
def race(row):
    
    """
    If a person's ehtincity is 'Hispanic Or Latino' so is their race
    """
    if row['ethnicity'] == 'Hispanic Or Latino':
        return 'Hispanic Or Latino'
    else:
        return row['race']
    
df_r_363['race'] = df_r_363.apply(race, axis = 1)


# ### Transformation

# In[8]:


#concating df_r_fca and df_r_363
df = pd.concat([df_r_fca,df_r_363])

# returning active or not active students
df = df[(df['status']=='Active')|(df['status']=='Not Activated')]

# retunring relevant columns
df = df[['id','schoolId','stateId','firstName', 'lastName','gender', 
    'ethnicity', 'race', 'languages','dob','graduationYear', 'status']]

# filteirng out duplicated values 
df = df[~df.duplicated()]


# In[9]:


df.shape


# In[10]:


df.head()


# In[11]:


df.info()


# ### Load

# In[12]:


# loading into BigQuery database
table_id = 'Alma_Data_API.Students'#--> dataset id and table name

df.to_gbq(table_id, project_id=credentials.project_id, if_exists='replace', credentials=credentials)

