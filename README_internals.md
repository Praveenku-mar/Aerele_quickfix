<!-- B2 - ORM Internals & Query Builder
Part - A -->
## Table naming
## Question

1. Run: frappe.db.sql("SHOW TABLES LIKE '%Job%'") and list what you see. Explain the tab prefix convention.


Out[2]: (('tabScheduled Job Log',), ('tabScheduled Job Type',))

It returns the list of tables where the table name contains the word `JOB`.  

This means the query is filtering table names using a condition like `LIKE '%JOB%'`.  
The database searches system metadata and returns matching table names.  
Only tables containing `JOB` in their name are included in the result.

---

1. Run: frappe.db.sql("DESCRIBE `tabJob Card`", as_dict=True) and list 5 column names you recognise from your DocType fields.

It returns the description of the table fields.  

This means the query is showing the table structure, including column names, data types, null values, keys, and default values.  
The database is describing the schema, not the actual data inside the table.  
It helps understand how the table is designed.

---
<!-- Part - D -->
## DocStatus transitions


2. Can you call `doc.save()` on a submitted document?  

You cannot normally call `doc.save()` on a submitted document because its `docstatus` is `1` (submitted) and Frappe prevents modification unless `allow_on_submit` is enabled.  
Frappe raises a validation error at the document lifecycle layer.  

---

3. What about `doc.submit()` on a cancelled document?

You also cannot call `doc.submit()` on a cancelled document because its `docstatus` is `2`.  
A cancelled document must be amended (which creates a new draft copy) before it can be submitted again.

---
4. Why would you see a "Document has been modified after you have opened it" error
and how does Frappe prevent concurrent overwrites?

This error appears when two users open the same document and one user saves changes before the other.  
Frappe compares the document’s `modified` timestamp in the database with the one loaded in memory.  
If they do not match, Frappe throws a `TimestampMismatchError`.  

---
## Dangerous patterns

5. The following snippet has TWO bugs related to document lifecycle. Identify both and write the corrected version.

I found only one bug,
## Bugs

 Calling `self.save()` inside `validate()` is wrong. `validate()` runs during save, so this causes recursion and breaks the document lifecycle.

--- 
<!-- C1 - Device Type, Technician, Spare Part, QuickFix Setting -->

6. When appending a row to `Job Card.parts_used` and saving, what 4 columns are auto-set?

Frappe automatically sets:

- `parent` – Name of the parent document  
- `parenttype` – Parent DocType (Job Card)  
- `parentfield` – Fieldname of the child table (parts_used)  
- `idx` – Row order number  

These link the child row to its parent.

---

7. What is the DB table name for Part Usage Entry DocType?

The table name will be "tabPart Usage Entry"

---

8. If you delete row at idx=2 and re-save, what happens to remaining idx values?

Frappe reorders the rows automatically.  
It renumbers `idx` values sequentially starting from 1.  
There will be no gaps in the index.

----


9. After renaming a Technician record using Rename Document, does the `assigned_technician` field in linked Job Cards update automatically? Why? What does "track changes" mean here?

Yes, the `assigned_technician` field updates automatically.  
Frappe updates all Link fields in other documents that reference the renamed record.  
This happens because Rename Document updates references at the database level to maintain link integrity.

---

10. What is the difference between setting a field as "unique" in the DocType versus using `frappe.db.exists()` inside `validate()`?


Setting a field as **unique** creates a database-level unique constraint.  
The database itself blocks duplicate values, even under concurrent requests.  
Unique constraint is strict and safe. 

Using `frappe.db.exists()` in `validate()` is only an application-level check.  
It can fail under race conditions because two requests can pass validation before either is saved.  
`frappe.db.exists()` is weaker and not reliable for true uniqueness.
---

11. Call self.save() inside on_update and see to the issues of it and explain them in the same readme_internals. Correct the pattern and explain it.


If you call `self.save()` inside `on_update`, it causes infinite recursion.  
Flow is: `save()` → `on_update()` → `save()` → `on_update()` → repeats.  
This continues until the request crashes or hits recursion limits.  
It also creates unnecessary DB writes and performance issues.

## correct version:
If you only need to modify fields on the same document:

```python
def validate(self):
    self.total = self.qty * self.rate