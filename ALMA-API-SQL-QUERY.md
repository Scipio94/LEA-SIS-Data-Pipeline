~~~ SQL
CREATE TEMP TABLE t1 AS
/*JOINING Alma API Tables*/
SELECT 
  DISTINCT id, schoolid, stateid, firstname, lastname, grade,gender, race
FROM
(SELECT *
FROM `single-being-353600.Alma_Data_API.Students` AS student -- student data table
LEFT JOIN `single-being-353600.Alma_Data_API.Student_Grade_Level_ID` grade -- student id and grade level id
ON student.id = grade.student_id) AS sub -- subquery
LEFT JOIN `single-being-353600.Alma_Data_API.Grade_Level_ID` AS grade_level -- grade level id table
ON sub.gradelevel_id = grade_level.Grade_Level_ID -- LEFT JOIN on sub query and grade_level table
WHERE grade IS NOT NULL -- Filtering out inactive students.
ORDER BY grade;

/*Complete data*/
SELECT * -- Complete Data
FROM t1;

/*Attendance Data*/
SELECT -- Daily Attendance Data
  id, 
  firstname, 
  lastname, 
  EXTRACT(MONTH FROM CAST(date AS date)) AS month, -- creating month column to calculate attendance
  date,
  att.status
FROM t1
INNER JOIN `single-being-353600.Alma_Data_API.Student_Attendance` AS att -- attendance table
ON t1.id = att.student_id;


/*Attendance Data Calc*/
SELECT -- Attendance Data Calc
  sub.id,
  sub.firstname,
  sub.lastname,
  sub.MONTH,
  ROUND(sub.Days_Present/School_Days,2) AS Att_Pct,
  ROUND(sub.Days_Tardy/School_Days,2) AS Tardy_Pct
,FROM
(SELECT
 DISTINCT id, 
  firstname, 
  lastname, 
  EXTRACT(MONTH FROM CAST(date AS date)) AS month, -- creating month column to calculate attendance
  SUM (CASE WHEN status IN  ('Present','Late') THEN 1 ELSE 0 END) OVER (PARTITION BY id,EXTRACT(MONTH FROM CAST(date AS date))) AS Days_Present,
  SUM (CASE WHEN status = 'Late' THEN 1 ELSE 0 END) OVER (PARTITION BY id,EXTRACT(MONTH FROM CAST(date AS date))) AS Days_Tardy,
  CASE 
    WHEN EXTRACT(MONTH FROM CAST(date AS date)) = 8 THEN 10 
    WHEN EXTRACT(MONTH FROM CAST(date AS date)) = 9 THEN 20
    END AS School_Days
FROM t1
INNER JOIN `single-being-353600.Alma_Data_API.Student_Attendance` AS att -- attendance table
ON t1.id = att.student_id) AS sub
~~~
