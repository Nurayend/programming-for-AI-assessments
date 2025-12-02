# Database information
This file is to show the description of tables. Diagram is available in diagram.svg file

## Users
Table to store users' data
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td> id</td>
    <td>INTEGER   </td>
    <td> PK   </td>
    <td> Unique user ID (Auto-increment).   </td>
  </tr>
  <tr>
    <td>username</td>
    <td>TEXT   </td>
    <td></td>
    <td>Unique Username</td>
  </tr>
  <tr>
    <td>password</td>
    <td>TEXT   </td>
    <td></td>
    <td>Password</td>
  </tr>
  <tr>
    <td>role_id</td>
    <td>INTEGER   </td>
    <td>FK</td>
    <td> Role of the user</td>
  </tr>
</tbody>
</table>

## Roles
Roles of users
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td> id</td>
    <td>INTEGER   </td>
    <td> PK   </td>
    <td> Unique Role ID (Auto-increment).   </td>
  </tr>
  <tr>
    <td>name</td>
    <td>TEXT   </td>
    <td></td>
    <td>Definition of the role</td>
  </tr>
</tbody>
</table>

## Course_directors
Table to link course directors (users with that role) to courses which they lead. 
A course can only be managed by one user (the Course Director), but one user can manage multiple courses
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td>id</td>
    <td>INTEGER   </td>
    <td>PK</td>
    <td>ID</td>
  </tr>
  <tr>
    <td>user_id</td>
    <td> INTEGER</td>
    <td>FK </td>
    <td>Links to the Users table</td>
  </tr>
  <tr>
    <td>course_id</td>
    <td>INTEGER</td>
    <td>FK </td>
    <td>Links to the Courses table </td>
  </tr>
</tbody>
</table>

## Students
Table of students
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td>id</td>
    <td>INTEGER   </td>
    <td> PK   </td>
    <td>Unique Student ID</td>
  </tr>
  <tr>
    <td>graduation_date</td>
    <td>DATE</td>
    <td></td>
    <td>When student will graduate (to check only active students)</td>
  </tr>
  <tr>
    <td>status</td>
    <td>TEXT   </td>
    <td></td>
    <td>Active or Inactive students</td>
  </tr>
</tbody>
</table>

## Courses
Table of courses (or modules not major)
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td> id</td>
    <td>INTEGER   </td>
    <td> PK   </td>
    <td>Unique course ID (Auto-increment)</td>
  </tr>
  <tr>
    <td>name</td>
    <td>TEXT   </td>
    <td></td>
    <td>Course name</td>
  </tr>
</tbody>
</table>

## Enrollment
To link students with course (module)
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td>student_id</td>
    <td>INTEGER   </td>
    <td>FK</td>
    <td>Students unique ID</td>
  </tr>
  <tr>
    <td>course_id</td>
    <td>INTEGER</td>
    <td>FK</td>
    <td>Courses unique ID</td>
  </tr>
</tbody>
</table>

## Assessments
For course (module) assessments. An Assessment can only belong to one Course, but one Course can have multiple Assessments
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td>id</td>
    <td>INTEGER   </td>
    <td>PK</td>
    <td>Unique Assessment ID</td>
  </tr>
  <tr>
    <td>title</td>
    <td>TEXT</td>
    <td></td>
    <td>Name of the assignment (e.g., "Python Project") </td>
  </tr>
  <tr>
    <td>course_id</td>
    <td>INTEGER</td>
    <td>FK</td>
    <td>Link to course (assessment of which course)</td>
  </tr>
  <tr>
    <td>deadline</td>
    <td>DATE</td>
    <td></td>
    <td>Submission deadline</td>
  </tr>
  <tr>
    <td>max_score </td>
    <td>INTEGER</td>
    <td></td>
    <td>Maximum possible score (Default: 100)</td>
  </tr>
</tbody>
</table>

## Submissions
To check students' submissions
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td>id</td>
    <td>INTEGER   </td>
    <td>PK</td>
    <td>Unique Submission ID</td>
  </tr>
  <tr>
    <td>assessment_id</td>
    <td> INTEGER</td>
    <td>FK </td>
    <td>Links to the Assessments table</td>
  </tr>
  <tr>
    <td>student_id</td>
    <td>INTEGER</td>
    <td>FK </td>
    <td>Links to the Students table (Who submitted it?) </td>
  </tr>
  <tr>
    <td>submission_date</td>
    <td>DATE</td>
    <td></td>
    <td>Actual date of submission (Used to check for late submissions)</td>
  </tr>
  <tr>
    <td>score</td>
    <td>REAL</td>
    <td></td>
    <td>The grade/mark achieved</td>
  </tr>
</tbody>
</table>

## Attendance
To check attendance of students. There's a check for unique date, course and student
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td>id</td>
    <td>INTEGER   </td>
    <td>PK</td>
    <td>Unique Attendance ID</td>
  </tr>
  <tr>
    <td>student_id</td>
    <td>INTEGER</td>
    <td>FK</td>
    <td>Links to the Students table</td>
  </tr>
  <tr>
    <td>course_id</td>
    <td>INTEGER   </td>
    <td>FK</td>
    <td>Attendance of which course</td>
  </tr>
  <tr>
    <td>lecture_date </td>
    <td>DATE</td>
    <td></td>
    <td>The specific date of the lecture</td>
  </tr>
  <tr>
    <td>status</td>
    <td>TEXT</td>
    <td></td>
    <td>Attendance status: 'Present', 'Absent', 'Late' </td>
  </tr>
</tbody>
</table>

## Wellbeing_surveys
Table to store data about students' stress level and sleep hours
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td>id</td>
    <td>INTEGER   </td>
    <td>PK</td>
    <td>Unique Wellbeing survey ID</td>
  </tr>
  <tr>
    <td>student_id   </td>
    <td>INTEGER   </td>
    <td>FK</td>
    <td>Links to the Students table</td>
  </tr>
  <tr>
    <td>survey_id</td>
    <td>INTEGER</td>
    <td>FK</td>
    <td>The date the survey was submitted (or any additional data about survey)</td>
  </tr>
  <tr>
    <td>stress_level</td>
    <td>INTEGER </td>
    <td></td>
    <td>Stress rating (1–5). (Constraint: Must be between 1 and 5)</td>
  </tr>
  <tr>
    <td>sleep_hours</td>
    <td>REAL</td>
    <td></td>
    <td>Hours slept the previous night</td>
  </tr>
</tbody>
</table>

## Surveys
Reference table to store any data about surveys (is there will be different types of surveys)
<table><thead>
  <tr>
    <th>Field Name</th>
    <th>Data Type </th>
    <th>Key </th>
    <th>Description</th>
  </tr></thead>
<tbody>
  <tr>
    <td>id</td>
    <td>INTEGER   </td>
    <td>PK</td>
    <td>Unique Wellbeing survey ID</td>
  </tr>
  <tr>
    <td>passed_date</td>
    <td>DATE</td>
    <td></td>
    <td>For determining the timing of the survey</td>
  </tr>
</tbody>
</table>