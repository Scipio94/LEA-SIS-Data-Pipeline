# Alma API

## Alma

Alma is a student information system (SIS) used by Foundation Academies Charter School in Trention, New Jersey. It houses a variety of student information and metrics essential to the school's function. It is also used for reporting. To automate the reporting process I established an API connection to perform ETL in Python and create a data pipeline to BigQuery.

## Files
- **json file**: authentification credentinals for BigQuery.
- **Alma API Ping Exercise**: establishing API connection with Alma.
- **Alma API School Year ID**: Retrieving the school year id for the current school year.
- **Alma API Student Grade-Level**: Retrieving the grade level id and the corresponding student id.
- **Alma API Student Grade-Level ID**: Retrieving the grade level id and the corresponding grade values, e.g. 1,2, etc.
- **Alma API Students**: Retrieving student data.
- **Alma API Student Attendance**: Retrieving student attendance data.

## BigQiery Authentification
1. Ensure that there is Google Cloud service account key JSON file. This file is necessary for authenticating your Python script with Google Cloud.
2. Import the following package and enter the script to authenticate the Google Service Account
~~~ pyton
from google.oauth2 import service_account

# replace file path with file path of JSON authentification file
credentials = service_account.Credentials.from_service_account_file('path/to/your/service-account-file.json')
~~~
3. Initialize BigQuery Client
~~~ python
from google.cloud import bigquery

# Initialize the BigQuery client
client = bigquery.Client(credentials=credentials, project=credentials.project_id)
~~~
4. Load data into a dataframe
~~~ python
df = pd.DataFrame(data = data)
~~~~
6. Upload data to BigQuery
~~~ python
table_id = 'your_dataset.your_table_name'

# Upload the DataFrame to BigQuery
df.to_gbq(table_id, project_id=credentials.project_id, if_exists='replace', credentials=credentials)
~~~
- The if_exists parameter determines the behavior if the table already exists:
- 'replace': If the table exists, it will be replaced.
- 'append': Append data to the existing table.
- 'fail': Raise an error if the table exists.
