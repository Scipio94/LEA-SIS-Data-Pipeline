# LEA SIS API Data Pipeline
![Alma-API-Data-Pipeline (1)](https://github.com/user-attachments/assets/5616a106-e6bd-4e7a-ae6d-a6d050a852b9)


## Alma

Alma is a student information system (SIS). It houses a variety of student information and metrics essential to the school's function. It is also used for reporting. To automate the reporting process I established an API connection to perform ETL in Python and create a data pipeline to BigQuery.

## Files
- **Alma API Ping Exercise**: establishing API connection with Alma.
- **Alma API School Year ID**: Retrieving the school year id for the current school year.
- **Alma API Student Grade-Level**: Retrieving the grade level id and the corresponding student id.
- **Alma API Student Grade-Level ID**: Retrieving the grade level id and the corresponding grade values, e.g. 1,2, etc.
- **Alma API Students**: Retrieving student data.
- **Alma API Student Attendance**:Retrieving student attendance data.
- **Crontab-File**: Explanation and logic on automating relevant python files

## Cronjob Automation
The files above were saved in **.ipynb** format, ***Interactive Python Notebook***, JSON based files that contain code cells, markdown, and metadata and is meant to be ran in a Jupyter Notebook environment. However, for the files to be automated the files need to be saved as **.py** format, a plain text file and can be directly executed by a Python interpreter.

1. Download relevant files to .py
2. Access Terminal
3. Access the cronjob command window
4. Insert the following commands:
~~~ cronjob
* * * * * command_to_execute
- - - - -
| | | | |
| | | | +---- Day of the week (0 - 7) (Sunday is both 0 and 7)
| | | +------ Month (1 - 12)
| | +-------- Day of the month (1 - 31)
| +---------- Hour (0 - 23)
+------------ Minute (0 - 59)

30 7 * * 1-5 /Users/scipio/anaconda3/bin/python3 /Users/scipio/Alma_API_Scripts/Alma_API_Student_Grade_Level_ID.py
30 7 * * 1-5 /Users/scipio/anaconda3/bin/python3 /Users/scipio/Alma_API_Scripts/Alma_API_Student_Grade_Level.py
30 7 * * 1-5 /Users/scipio/anaconda3/bin/python3 /Users/scipio/Alma_API_Scripts/Alma_API_Students.py
30 16 * * 1-5 /Users/scipio/anaconda3/bin/python3 /Users/scipio/Alma_API_Scripts/Alma_API_Student_Attendance.py

# schedules command to be ran at 7:30AM of everyday of every month Monday through Friday
# schedules command to be ran at 4:30 PM of everyday of every month Monday through Friday
~~~
5. Save the cronjob command and exit cronjob window


## BigQiery Authentification
1. Ensure that there is Google Cloud service account key JSON file. This file is necessary for authenticating your Python script with Google Cloud.
2. Import the following package and enter the script to authenticate the Google Service Account
~~~ python
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
