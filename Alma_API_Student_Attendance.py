#!/usr/bin/env python
# coding: utf-8

# ## Alma API Single Student Attendance
# 
# Writing a code that returns the attendance data of a signle student from the Alma API url endpoint

# In[12]:


#importing relevant packages
import pandas as pd
import requests
import json
from requests.auth import HTTPDigestAuth
from google.cloud import bigquery
from google.oauth2 import service_account
from dotenv import load_dotenv
import os


# In[13]:


env_file_path = '/Users/scipio/Alma_API_Scripts/ALMA_API.env'


# In[14]:


load_dotenv(dotenv_path = env_file_path )


# In[15]:


# retrieving releavnt variables from the .env file
API_KEY = os.getenv('API_KEY')
AUTH_SECRET = os.getenv('AUTH_SECRET')


# **FCA Current School Year**: 65e8a8461e0c3dd517076bcf
# 
# **363 Current School Year ID**: 664cc55127c6b4a81806658b

# In[16]:


# setting up BigQuery authentication
credentials = service_account.Credentials.from_service_account_file(
    '/Users/scipio/Alma_API_Scripts/single-being-353600-adc0535ffe93.json'
                                                                   )
#initializing BigQuery client
client = bigquery.Client(credentials=credentials, project=credentials.project_id)


# ### Extraction of Student Attendance Data FCA

# In[17]:


# Defining credential api_key and auth_secret 
api_key = API_KEY
auth_secret = AUTH_SECRET 

# URL of the API endpoint FCA

#url endpoint to return attendance data of Jaden McKellar
url1= 'https://facs.api.getalma.com/v2/fca/students/60ca0ea65a24b06c6a107faf/attendance?schoolYearId=65e8a8461e0c3dd517076bcf'

#url endpoint to return attendance data of Melvin McKellar
url2= 'https://facs.api.getalma.com/v2/fca/students/60ca3aa494882a4b7d791aef/attendance?schoolYearId=65e8a8461e0c3dd517076bcf'

# url endpoint to return attendance data of Julian Tineo
url3= 'https://facs.api.getalma.com/v2/fca/students/60ca0eb4832dc100d146db46/attendance?schoolYearId=65e8a8461e0c3dd517076bcf'


# Headers
headers = {
    'Content-Type':'application/json',
    'Accept':'application/json, application/problem+json'
}


# Make the GET request with Digest Authentication
response_fca_att1 = requests.get(url1, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))
response_fca_att2 = requests.get(url2, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))
response_fca_att3 = requests.get(url3, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))


# Making GET request into a json object
r_fca_att1 = response_fca_att1.json()
r_fca_att2 = response_fca_att2.json()
r_fca_att3 = response_fca_att3.json()

# Accessing 'response' key value to return lists of dictionaries
r_fca_att1 = r_fca_att1['response']
r_fca_att2 = r_fca_att2['response']
r_fca_att3 = r_fca_att3['response']


# In[18]:


# creating dataframe for attendance extraction for fca student
fca_att_df1 = pd.DataFrame(r_fca_att1)
fca_att_df2 = pd.DataFrame(r_fca_att2)
fca_att_df3 = pd.DataFrame(r_fca_att3)

# adding primary key student_id of Jaden McKellar
fca_att_df1['student_id'] = '60ca0ea65a24b06c6a107faf'
fca_att_df1['district'] = 'Rancocas Valley Regional High School'

# adding primary key student_id Melvin McKellar
fca_att_df2['student_id'] = '60ca3aa494882a4b7d791aef'
fca_att_df2['district'] = 'Rancocas Valley Regional High School'

# adding primary key student_ id Julian Tineo
fca_att_df3['student_id'] = '60ca0eb4832dc100d146db46'
fca_att_df3['district'] = "Penn's Grove"


# ### Extraction of Student Attendance Data FACS 363

# In[19]:


# Defining credential api_key and auth_secret 
api_key = API_KEY
auth_secret = AUTH_SECRET 

# URL of the API endpoint FCA

# url endpoint to return attendance data of Miabella Tineo
url1= 'https://facs.api.getalma.com/v2/facs363/students/60c9f26d1f86da023b455d96/attendance?schoolYearId=664cc55127c6b4a81806658b' # --> will return grade level ids

# url endpoint to return attendance data of Jordan Tineo
url2= 'https://facs.api.getalma.com/v2/facs363/students/60c9feef7f8d901080325e07/attendance?schoolYearId=664cc55127c6b4a81806658b'

# url endpoint to return attendance data of Jaelyon Tineo
url3= 'https://facs.api.getalma.com/v2/facs363/students/60c9fefbee570b7782727eee/attendance?schoolYearId=664cc55127c6b4a81806658b'


# Headers
headers = {
    'Content-Type':'application/json',
    'Accept':'application/json, application/problem+json'
}


# Make the GET request with Digest Authentication
response_363_att1 = requests.get(url1, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))
response_363_att2 = requests.get(url2, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))
response_363_att3 = requests.get(url3, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))

# Making GET requests into a json object
r_363_att1 = response_363_att1.json()
r_363_att2 = response_363_att2.json()
r_363_att3 = response_363_att3.json()

# Accessing 'response' key value to return lists of dictionaries
r_363_att1 = r_363_att1['response']
r_363_att2 = r_363_att2['response']
r_363_att3 = r_363_att3['response']


# In[20]:


# creating a df for the 
facs_363_df1 = pd.DataFrame(r_363_att1)
facs_363_df2 = pd.DataFrame(r_363_att2)
facs_363_df3 = pd.DataFrame(r_363_att3)

# adding student_ id for Miabella Tineo 60c9f26d1f86da023b455d96
facs_363_df1['student_id'] = '60c9f26d1f86da023b455d96'
facs_363_df1['district'] = "Penn's Grove"


# adding student_id for Jordan Tineo 60c9feef7f8d901080325e07
facs_363_df2['student_id'] = '60c9feef7f8d901080325e07'
facs_363_df2['district'] = "Penn's Grove"

# adding student_id for Jaelyon Tineo
facs_363_df3['student_id'] = '60c9fefbee570b7782727eee'
facs_363_df3['district'] = "Penn's Grove"


# In[21]:


# concating dfs from resoective campuses
df = pd.concat([fca_att_df1,fca_att_df2,fca_att_df3,facs_363_df1,facs_363_df2,facs_363_df3])

# returning relevaant columns
df = df[['student_id', 'date','status', 'district']]


# ### Load

# In[22]:


# loading into BigQuery database
table_id = 'Alma_Data_API.Student_Attendance'

# loading df to the BigQuery database to append data to table with each upload
df.to_gbq(table_id, project_id=credentials.project_id, if_exists='replace', credentials=credentials)

