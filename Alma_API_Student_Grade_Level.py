#!/usr/bin/env python
# coding: utf-8

# ## Student ID and Grade Level ID

# Writing a code that communicates with the Alma url endpoint via an api to return unique student identifiers and the corresponding grade level id and uplaoding data extracted from the API to a BigQuery data warehousing software.

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


# ### FCA Student and Grade Level ID

# In[3]:


# Defining credential api_key and auth_secret 
api_key = '075DWGKCVHTEH1W6497W'
auth_secret = 'JlpYYSZUVjVWZGpQN2JKSndPRHM0TV9maChtU3VONkJvakhfaGVjUQ=='

# URL of the API endpoint FCA
url= 'https://facs.api.getalma.com/v2/fca/students/grade-levels?schoolYearId=65e8a8461e0c3dd517076bcf' # --> will return grade level ids

# Headers
headers = {
    'Content-Type':'application/json',
    'Accept':'application/json, application/problem+json'
}


# Make the GET request with Digest Authentication
response_fca_grade = requests.get(url, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))

# Making GET request into a json object
r_fca_grade = response_fca_grade.json()


# In[4]:


student_grade_fca = r_fca_grade['response']

student_grade_fca = student_grade_fca['students']


# In[5]:


# creating a dataframe using the json object
r_fca_grade_df = pd.DataFrame(data = student_grade_fca)

#data cleaning
r_fca_grade_df['gradeLevels'] = r_fca_grade_df['gradeLevels'].astype('string')#--> casting column as string
r_fca_grade_df['gradeLevels'] = r_fca_grade_df['gradeLevels'].str.split(',').str[1] #--> splitting on ','
r_fca_grade_df['gradelevel_id'] = r_fca_grade_df['gradeLevels'].str.split(':').str[1] #--> splitting on ':'
r_fca_grade_df = r_fca_grade_df[['id','gradelevel_id']]#--> returning relevant columns
r_fca_grade_df['gradelevel_id'] = r_fca_grade_df['gradelevel_id'].str[2:-1] #--> returning grade level id
r_fca_grade_df.rename(columns = {'id':'student_id'},inplace = True) #--> renaming columns


# ### 363 Student and Grade Level ID

# In[6]:


# Defining credential api_key and auth_secret 
api_key = '075DWGKCVHTEH1W6497W'
auth_secret = 'JlpYYSZUVjVWZGpQN2JKSndPRHM0TV9maChtU3VONkJvakhfaGVjUQ=='

# URL of the API endpoint FCA
url= 'https://facs.api.getalma.com/v2/facs363/students/grade-levels?schoolYearId=664cc55127c6b4a81806658b' # --> will return grade level ids

# Headers
headers = {
    'Content-Type':'application/json',
    'Accept':'application/json, application/problem+json'
}


# Make the GET request with Digest Authentication
response_facs363_grade = requests.get(url, headers=headers, auth=HTTPDigestAuth(api_key, auth_secret))

# Making GET request into a json object
r_facs363_grade = response_facs363_grade.json()


# In[7]:


# indexing dictionary based on the key 'response' key
student_grade_facs363 = r_facs363_grade['response']

#indexing dictionary based on student key to get student data 
student_data_facs363 = student_grade_facs363['students']


# ### Transformation

# In[8]:


# creating a dataframe using the json object
r_facs363_grade_df = pd.DataFrame(data = student_data_facs363)

# #data cleaning
r_facs363_grade_df['gradeLevels'] = r_facs363_grade_df['gradeLevels'].astype('string')#--> casting column as string
r_facs363_grade_df['gradeLevels'] = r_facs363_grade_df['gradeLevels'].str.split(',').str[1] #--> splitting on ','
r_facs363_grade_df['gradelevel_id'] = r_facs363_grade_df['gradeLevels'].str.split(':').str[1] #--> splitting on ':'
r_facs363_grade_df = r_facs363_grade_df[['id','gradelevel_id']]#--> returning relevant columns
r_facs363_grade_df['gradelevel_id'] = r_facs363_grade_df['gradelevel_id'].str[2:-1]#--> returning grade level id
r_facs363_grade_df.rename(columns = {'id':'student_id'},inplace = True) #--> renaming columns


# In[9]:


#concating dataframes
df_student_id = pd.concat([r_facs363_grade_df,r_fca_grade_df])


# In[10]:


df_student_id.shape


# In[11]:


df_student_id.info()


# ### Load

# In[12]:


# loading into BigQuery database
table_id = 'Alma_Data_API.Student_Grade_Level_ID' #--> dataset id and table name

df_student_id.to_gbq(table_id, project_id=credentials.project_id, if_exists='replace', credentials=credentials)

