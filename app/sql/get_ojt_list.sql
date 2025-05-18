SELECT studentstbl.student_id, studentstbl.student_name, studentstbl.email, studentstbl.company_name, studentstbl.total_hours, studentstbl.school_id 
FROM ojtlisttbl
INNER JOIN studentstbl ON ojtlisttbl.student_id = studentstbl.student_id WHERE studentstbl.school_id = %s;