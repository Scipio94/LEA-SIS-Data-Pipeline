#!/usr/bin/env python
# coding: utf-8

# ## Alma API Single Student Attendance
# 
# Writing a code that returns the attendance data of a signle student from the Alma API url endpoint

# In[1]:


#importing relevant packages
import pandas as pd
import requests
import json
from requests.auth import HTTPDigestAuth
from google.cloud import bigquery
from google.oauth2 import service_account


# **FCA Current School Year**: 65e8a8461e0c3dd517076bcf
# 
# **363 Current School Year ID**: 664cc55127c6b4a81806658b

# In[2]:


# setting up BigQuery authentication
credentials = service_account.Credentials.from_service_account_file(
    '/Users/scipio/Downloads/single-being-353600-82aaccaecf53.json'
                                                                   )
#initializing BigQuery client
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


# ### Extraction of Student Attendance Data FCA

# In[3]:


# Defining credential api_key and auth_secret 
api_key = '075DWGKCVHTEH1W6497W'
auth_secret = 'JlpYYSZUVjVWZGpQN2JKSndPRHM0TV9maChtU3VONkJvakhfaGVjUQ=='

# URL of the API endpoint FCA
url= 'https://facs.api.getalma.com/v2/fca/students/60ca0ec59d6473552c13452b/attendance?schoolYearId=65e8a8461e0c3dd517076bcf' # --> will return grade level ids

# Headers
headers = {
    'Content-Type':'application/json',
    'Accept':'application/json, application/problem+json'
}


# Make the GET request with Digest Authentication
response_fca_att = requests.get(url, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))

# Making GET request into a json object
r_fca_att = response_fca_att.json()

# Accessing 'response' key value to return lists of dictionaries
r_fca_att = r_fca_att['response']


# In[4]:


# creating dataframe for attendance extraction for fca student
fca_att_df = pd.DataFrame(r_fca_att)

# adding primary key student_id
fca_att_df['student_id'] = '60ca0ec59d6473552c13452b'


# ### Extraction of Student Attendance Data FACS 363

# In[5]:


# Defining credential api_key and auth_secret 
api_key = '075DWGKCVHTEH1W6497W'
auth_secret = 'JlpYYSZUVjVWZGpQN2JKSndPRHM0TV9maChtU3VONkJvakhfaGVjUQ=='

# URL of the API endpoint FCA
url= 'https://facs.api.getalma.com/v2/facs363/students/60c9f24cb85e9d5e074016cf/attendance?schoolYearId=664cc55127c6b4a81806658b' # --> will return grade level ids

# Headers
headers = {
    'Content-Type':'application/json',
    'Accept':'application/json, application/problem+json'
}


# Make the GET request with Digest Authentication
response_363_att = requests.get(url, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))

# Making GET requests into a json object
r_363_att = response_363_att.json()


# Accessing 'response' key value to return lists of dictionaries
r_363_att = r_363_att['response']


# In[6]:


# creating a df for the 
facs_363_df = pd.DataFrame(r_363_att)

facs_363_df['student_id'] = '60c9f24cb85e9d5e074016cf'


# In[7]:


# concating dfs from resoective campuses
df = pd.concat([fca_att_df,facs_363_df])


# In[8]:


df.shape


# In[9]:


df.info()


# In[10]:


# returning relevaant columns
df = df[['student_id', 'date','status']]


# In[11]:


df


# ### Load

# In[12]:


# loading into BigQuery database
table_id = 'Alma_Data_API.Student_Attendance'

# loading df to the BigQuery database to append data to table with each upload
df.to_gbq(table_id, project_id=credentials.project_id, if_exists='replace', credentials=credentials)

