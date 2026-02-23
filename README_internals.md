## Run: frappe.db.sql("SHOW TABLES LIKE '%Job%'") and list what you see. Explain the tab prefix convention.


Out[2]: (('tabScheduled Job Log',), ('tabScheduled Job Type',))

It returns the list of tables where the table name contains the word `JOB`.  

This means the query is filtering table names using a condition like `LIKE '%JOB%'`.  
The database searches system metadata and returns matching table names.  
Only tables containing `JOB` in their name are included in the result.

---

## Run: frappe.db.sql("DESCRIBE `tabJob Card`", as_dict=True) and list 5 column names you recognise from your DocType fields.

It returns the description of the table fields.  

This means the query is showing the table structure, including column names, data types, null values, keys, and default values.  
The database is describing the schema, not the actual data inside the table.  
It helps understand how the table is designed.