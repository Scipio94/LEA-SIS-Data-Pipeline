#!/usr/bin/env python
# coding: utf-8

# ## Finding Grade Level IDs

# Writing a code that communicates with the Alma url endpoint via an API to return grade level ids at each campus and uplaoding data extracted from the API to a BigQuery data warehousing software.

# In[1]:


#importing relevant packages
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


# ### Grade Level ids of FCA

# In[6]:


# Defining credential api_key and auth_secret 
api_key = API_KEY
auth_secret = AUTH_SECRET

# URL of the API endpoint FCA with school year id query
url= 'https://facs.api.getalma.com/v2/fca/grade-levels?schoolYearId=65e8a8461e0c3dd517076bcf' # --> will return grade level ids

# Headers
headers = {
    'Content-Type':'application/json',
    'Accept':'application/json, application/problem+json'
}

# Make the GET request with Digest Authentication
response_fca = requests.get(url, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))

# Making response into a json object
r_fca = response_fca.json()


# In[7]:


# seperating key value pairs
for key,value in r_fca.items():
    value #--> list of dictionaries


# ### Transformation

# In[8]:


# creating df from dictionary object
grade_df_fca = pd.DataFrame(data = value)

# returning relevant columns and dropping duplicates
grade_df_fca = grade_df_fca[['id','gradeLevelAbbr']].drop_duplicates()

# casting data type of the gradeLevelAbbr column
grade_df_fca['gradeLevelAbbr'] = grade_df_fca['gradeLevelAbbr'].astype('int64')

# stripping white space from the id column
grade_df_fca['id'] = grade_df_fca['id'].str.strip()

grade_df_fca.rename(columns = {'gradeLevelAbbr':'Grade', 'id':'Grade_Level_ID'}, inplace = True )


# ### Grade Levels FACS363

# In[9]:


# Defining credential api_key and auth_secret 
api_key = API_KEY
auth_secret = AUTH_SECRET

# URL of the API endpoint FACS 363 with school year id query
url= 'https://facs.api.getalma.com/v2/facs363/grade-levels?schoolYearId=664cc55127c6b4a81806658b' # --> will return grade level ids

# Headers
headers = {
    'Content-Type':'application/json',
    'Accept':'application/json, application/problem+json'
}

# Make the GET request with Digest Authentication
response_facs_363 = requests.get(url, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))

# Making response into a json object
r_facs_363 = response_facs_363.json()


# In[10]:


# seperating key value pairs
for key,value in r_facs_363.items():
    value #--> list of dictionaries


# ### Transformation

# In[11]:


# creating df from dictionary object
grade_df_facs_363 = pd.DataFrame(data = value)

# stripping white space from the id column
grade_df_facs_363['id'] = grade_df_facs_363['id'].str.strip()


#returning relevant columns
grade_df_facs_363 = grade_df_facs_363[['id','equivalent']]


grade_df_facs_363.rename(columns = {'equivalent':'Grade', 'id':'Grade_Level_ID'}, inplace = True)


# In[12]:


# concating df
grade_level_id = pd.concat([grade_df_fca,grade_df_facs_363])

# data cleaning
grade_level_id['Grade'] = grade_level_id['Grade'].astype('string')


# In[13]:


grade_level_id.shape


# In[14]:


grade_level_id.info()


# In[15]:


grade_level_id


# ### Load

# In[16]:


# loading into BigQuery database
table_id = 'Alma_Data_API.Grade_Level_ID'#--> dataset id and table name

grade_level_id.to_gbq(table_id, project_id=credentials.project_id, if_exists='replace', credentials=credentials)

