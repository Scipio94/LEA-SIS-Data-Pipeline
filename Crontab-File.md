# Crontab Scheduling Syntax

## Complete the following steps prior to writing command
1. Enter Terminal
2. crontab -r: clear all commands
3. crontab -l: displays the jobs to be ran
4. crontab -e: enter cronjob command window

## Crontab Job
1. press i: Allows to insert cronjob
~~~ crontab
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
~~~
2. Press 'esc' tab: exits the insert mode
3. Press ':wq' - saves the command
  - ':' - commands mode
  - 'w' - write
  - 'q' - quit

The cronjob syntax above schedules the .py files to be ran externally at 7:30 AM daily everyday of every month Monday through Friday
The cronjob syntax above schedules the .py file Alma_API_Student_Attendance be to ran at 4:30 PM of everyday of every month Monday through Friday

