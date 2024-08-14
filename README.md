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
- **Alma API Scheduler**: Executes the Student Grade-Level, Student Grade-Level ID, and Students python scripts to update tables in BigQuery

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

## Scheduling Scripts
1. import the following packages
  - schedule: used to run python functions periodically at pre-determined intervals.
    - to use may need to use pip intsall schedule and then import schedule
~~~ python
# install schedule package
pip install schedule

#importing schedule package
import schedule
~~~
  - subprocess: used to execute system commands and programs within python scripts.
  - time: used to access time
  - os: used as a way of operating system dependent functionality, like reading or writing to the file system.
2. Create a function to run external script using subprocess:
~~~ python
def run_script_1():
    subprocess.run(["python3", "path/to/your_script1.py"])
# subprocess.run() runs the program as if it was typed directly into the command line
# 'python3' tells the system to use the Python 3 interprter to run the script
# 'path/to/your_script1.py' specifies which python script you want to be ran
~~~
3. Schedule scripts to run
~~~ python
schedule.every().day.at("09:00").do(run_script_1)
# scheduling the script to run everyday at 9:00
~~~
4. Keep the script running using a While loop
~~~ python
while True: #--> creates an infinite loop True always evaluates to True
    schedule.run_pending()
    time.sleep(1) #--> pauses the execution of the program, used to prevent the loop running too frequently
# schedule.run_pending() checks whether or not there is scheduled tasks and runs them
~~~
