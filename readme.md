
Employer
flask create-position position_id employer_id title
example: flask create-position 2 1 janitor

flask update-status position_id student_id status
example: update-status 1 1 accepted

Staff
flask add-student staff_id student_id position_id
example: flask add-student 1 1 1

Student
flask student-shortlist student_id
example: flask student-shortlist 1

General
flask view-shortlist position_id
example: flask view-shortlist 1