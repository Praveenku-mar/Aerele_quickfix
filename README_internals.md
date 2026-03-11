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

2. Run: frappe.db.sql("DESCRIBE `tabJob Card`", as_dict=True) and list 5 column names you recognise from your DocType fields.

It returns the description of the table fields.  

This means the query is showing the table structure, including column names, data types, null values, keys, and default values.  
The database is describing the schema, not the actual data inside the table.  
It helps understand how the table is designed.

---
<!-- Part - D -->
## DocStatus transitions


3. Can you call `doc.save()` on a submitted document?  

You cannot normally call `doc.save()` on a submitted document because its `docstatus` is `1` (submitted) and Frappe prevents modification unless `allow_on_submit` is enabled.  
Frappe raises a validation error at the document lifecycle layer.  

---

4. What about `doc.submit()` on a cancelled document?

You also cannot call `doc.submit()` on a cancelled document because its `docstatus` is `2`.  
A cancelled document must be amended (which creates a new draft copy) before it can be submitted again.

---
5. Why would you see a "Document has been modified after you have opened it" error
and how does Frappe prevent concurrent overwrites?

This error appears when two users open the same document and one user saves changes before the other.  
Frappe compares the document’s `modified` timestamp in the database with the one loaded in memory.  
If they do not match, Frappe throws a `TimestampMismatchError`.  

---
## Dangerous patterns

6. The following snippet has TWO bugs related to document lifecycle. Identify both and write the corrected version.

I found only one bug,
## Bugs

 Calling `self.save()` inside `validate()` is wrong. `validate()` runs during save, so this causes recursion and breaks the document lifecycle.

--- 
<!-- C1 - Device Type, Technician, Spare Part, QuickFix Setting -->

7. When appending a row to `Job Card.parts_used` and saving, what 4 columns are auto-set?

Frappe automatically sets:

- `parent` – Name of the parent document  
- `parenttype` – Parent DocType (Job Card)  
- `parentfield` – Fieldname of the child table (parts_used)  
- `idx` – Row order number  

These link the child row to its parent.

---

8. What is the DB table name for Part Usage Entry DocType?

The table name will be "tabPart Usage Entry"

---

9. If you delete row at idx=2 and re-save, what happens to remaining idx values?

Frappe reorders the rows automatically.  
It renumbers `idx` values sequentially starting from 1.  
There will be no gaps in the index.

----


10. After renaming a Technician record using Rename Document, does the `assigned_technician` field in linked Job Cards update automatically? Why? What does "track changes" mean here?

Yes, the `assigned_technician` field updates automatically.  
Frappe updates all Link fields in other documents that reference the renamed record.  
This happens because Rename Document updates references at the database level to maintain link integrity.

---

11. What is the difference between setting a field as "unique" in the DocType versus using `frappe.db.exists()` inside `validate()`?


Setting a field as **unique** creates a database-level unique constraint.  
The database itself blocks duplicate values, even under concurrent requests.  
Unique constraint is strict and safe. 

Using `frappe.db.exists()` in `validate()` is only an application-level check.  
It can fail under race conditions because two requests can pass validation before either is saved.  
`frappe.db.exists()` is weaker and not reliable for true uniqueness.
---

12. Call self.save() inside on_update and see to the issues of it and explain them in the same readme_internals. Correct the pattern and explain it.


If you call `self.save()` inside `on_update`, it causes infinite recursion.  
Flow is: `save()` → `on_update()` → `save()` → `on_update()` → repeats.  
This continues until the request crashes or hits recursion limits.  
It also creates unnecessary DB writes and performance issues.

## correct version:
If you only need to modify fields on the same document:

```python
def validate(self):
    self.total = self.qty * self.rate
```
---

13 .What is the issue with using `frappe.get_all()` inside a whitelisted method exposed to guests or low-privilege users, especially regarding `permission_query_conditions`?

`frappe.get_all()` ignores user permissions by default.  
It does not apply `permission_query_conditions` defined for the DocType.  
If exposed in a guest-accessible or low-privilege whitelisted method, it can return data the user should not see.  

---

14. Why is `doc_events` safer than `override_doctype_class` for most use cases?

`doc_events` attaches logic to specific lifecycle hooks without replacing the core DocType class.  
It keeps the standard behavior intact and only adds extra logic where needed.  

`override_doctype_class` completely replaces the original class.  
If you miss internal logic from the base class, you can break validations, permissions, or workflows.  

`doc_events` is additive and low risk.  
`override_doctype_class` is invasive and easier to misuse.
---
15.Multiple `validate` Handlers on Job Card

When two `validate` handlers exist:

- The `validate()` method inside the main DocType controller runs first.  
- The `validate` function registered through `doc_events` runs after that.
---
16. What If Both Raise `frappe.ValidationError`?

Execution stops immediately when the first `frappe.ValidationError` is raised.  
The second handler will not run.  
Frappe aborts the request at the first thrown validation exception.  
Only one error is returned to the browser — the one raised first.

---
17. `app_include_js` vs `web_include_js`

### Difference

`app_include_js` loads JavaScript only inside the Desk (logged-in backend UI).  
It affects internal users like Admin, Managers, Technicians using the Frappe workspace.

`web_include_js` loads JavaScript only on public website or portal pages.  
It does not load inside the Desk.

---

### When to Use Each

Use `app_include_js` when customizing form behavior, list views, dashboards, or adding Desk-level UI logic.  

Use `web_include_js` when adding frontend scripts for public pages, portals, landing pages, or guest-facing features.  

Desk customization belongs in `app_include_js`.  
Public website behavior belongs in `web_include_js`.

---
18. `doctype_js`, `doctype_list_js`, and `doctype_tree_js`

### `doctype_js` (Job Card)

`doctype_js` attaches JavaScript to the Job Card form view.  
It runs when opening or editing a single Job Card document.  
Use it for field triggers, validations, button actions, and client-side logic specific to the form.

---

### `doctype_list_js` (Job Card)

`doctype_list_js` applies to the Job Card list view.  
It runs when viewing the table of multiple Job Cards.  
Use it for custom list buttons, indicators, filters, or list-level UI behavior.

---

### `doctype_tree_js` (Not Applicable for Job Card)

`doctype_tree_js` is used for hierarchical DocTypes that use a tree structure.  
Example: Item Group, Account, or Territory.  
These DocTypes have parent-child relationships and are displayed as expandable trees.  
Job Card does not use tree view because it is a flat transactional document, not hierarchical data.
---

19. `override_whitelisted_methods` vs Monkey Patching

`override_whitelisted_methods` is a hook-based override defined in `hooks.py`.  
It explicitly replaces a whitelisted method with your own implementation.  


Monkey patching modifies the original function at import time.  
It directly reassigns or alters the method in memory without a formal hook.  

### When to Use Each

Use `override_whitelisted_methods` when you want to safely replace standard API behavior in a maintainable way.  
Use monkey patching only in rare edge cases where no hook exists and you fully control the environment.  
In production application, Monkey patching is risky and not recommended.
---

20. . What If Two Apps Override the Same Whitelisted Method?

If two apps register `override_whitelisted_methods` for the same method, the app loaded last takes precedence.  
This can create conflicts and unpredictable behavior if not managed carefully.

---

21. Signature Mismatch and TypeError

When overriding a method, your replacement must have the exact same function signature (same arguments).  
If the original method expects arguments like:
```python
def get_data(docname, user=None):
```
---
22. Calling `frappe.call` inside `validate` (before_save)

Calling `frappe.call` inside the client-side `validate` event does not work reliably because `validate` runs synchronously before the document is saved.  
`frappe.call` is asynchronous by default, so the server response may not return before the save continues.  
This creates race conditions where validation logic depends on data that has not arrived yet.  
As a result, the document may save before the async check completes.
---

23. ## Tree DocType

A Tree DocType represents hierarchical data stored in parent-child structure.  
Examples include Account, Cost Center, Item Group, or an Employee reporting hierarchy.  
Each record can have a parent, forming a structured expandable tree instead of a flat list.  
It is used when data naturally follows levels or categories.

---

## `doctype_tree_js`

`doctype_tree_js` is used to customize the behavior of a Tree view in Desk.  
It allows adding custom buttons, filters, node actions, or UI logic specific to the tree interface.  
It does not affect form or list view — only the tree view.

---

## Extra Fields Required for Tree DocType

A Tree DocType must include:

- `parent_field` – A Link field pointing to the same DocType to define hierarchy.  
- `is_group` – A Check field indicating whether the record can have child nodes.  

Without these, Frappe cannot maintain or render the hierarchical structure properly.

---
24. Client Script DocType vs Shipped JS (App-Level)

### Tradeoffs

A consultant would use **Client Script DocType** for quick, site-specific customizations without touching app code.  
It is editable from Desk, requires no deployment, and is fast for small behavior changes.

An app developer uses **shipped JS (doctype_js / app_include_js)** when building reusable, version-controlled, production-grade features.  
This code lives inside the app repository and follows proper deployment workflows.

### Risks of Client Script in Production

Client Scripts are stored in the database, not version controlled by default.  
They can be edited directly in production without review.  
This increases the risk of breaking behavior silently.  
They are harder to audit, test, and maintain at scale.

Use Client Script for temporary or small custom logic.  
Use shipped JS for structured application development.

---

## Hiding Fields vs Permission Security Pitfall

### Example: Hide `customer_phone` for Non-Managers (Client Side)

```javascript
frappe.ui.form.on("Job Card", {
    refresh(frm) {
        if (!frappe.user.has_role("Manager")) {
            frm.set_df_property("customer_phone", "hidden", 1);
        }
    }
});
```
---
25.  Prepared Report vs Real-Time Script Report

### When to Use Prepared Report

Prepared Report is used when the report takes a long time to run or processes a large amount of data.  
The report runs in the background using a worker and the result is stored.  
Users later download or view the stored result instead of running the query again.

### When to Use Real-Time Script Report

Real-time Script Report runs immediately when the user opens the report.  
It is used when the report query is fast and the data size is small.  
The result always reflects the current data in the database.

### Staleness Tradeoff

Prepared Reports can become **stale** because they show the data from the time the report was generated.  
If new records are added or updated later, the prepared report will not include those changes.
---
26 . Caching Risk

If the underlying data changes after the report is prepared, the user still sees the **old stored result**.  
The report will only show updated data after it is prepared again.

---
27. Avoid `frappe.get_all()` Inside Jinja Templates

Calling `frappe.get_all()` directly inside a Jinja template is bad practice.  
Templates should only display data, not run database queries.  
Putting queries in templates makes rendering slow and mixes presentation with business logic.

---

## Correct Pattern: Pre-compute in `before_print()`

Instead, compute the data in Python before rendering the template.

```python
def before_print(self):
    self.precomputed_field = frappe.get_all(
        "Job Card",
        filters={"assigned_technician": self.assigned_technician},
        fields=["name", "status"]
    )
```
---
28. Raw Printing vs HTML-PDF Printing (WeasyPrint)

### Raw Printing (ESC/POS)

Raw printing sends **ESC/POS commands directly to a thermal printer**.  
The printer interprets these commands to print text, align content, cut paper, or control formatting.  
It bypasses HTML rendering and works directly with the printer hardware.  
This method is fast and commonly used for POS bills and receipt printers.

---

### HTML-PDF Printing (WeasyPrint)

Frappe normally renders print formats as **HTML**, then converts them to **PDF using WeasyPrint**.  
The browser-style HTML and CSS are processed by WeasyPrint to generate a printable PDF.  
This approach works well for invoices, reports, and structured documents.  
However, WeasyPrint does not support all browser CSS features.

---

## CSS That Works in Browsers but Often Fails in WeasyPrint

Examples include:

- `position: fixed` (especially complex layouts)
- `flexbox` (`display: flex`)
- `grid layout` (`display: grid`)

These layouts may render correctly in browsers but break or behave differently in WeasyPrint PDFs.
---
29.  Disabling the Scheduler for a Specific Site

You can disable the scheduler for a site by running:

```bash
bench --site site-name set-config enable_scheduler 0
```

This updates the site’s `site_config.json` and stops scheduled tasks from being queued for that site.

### Why Disable It on a Dev Site

On a development site, scheduled jobs like emails, cleanup tasks, or integrations may run automatically.  
This can create unnecessary logs, background jobs, or external API calls during testing.  
Disabling the scheduler keeps the dev environment predictable and quiet.

---

## What Happens to Scheduled Jobs if the Worker Was Down?

If the worker process is down, queued jobs stay in Redis.  
They are not executed while the worker is offline.

When the worker starts again, it picks up the queued jobs and begins processing them.  
So the jobs are delayed, not lost.

---
30. Task A - N+1 query detection and fix:
The following code has an N+1 query problem. Identify it and rewrite it:
# N+1 PROBLEM - fix this
job_cards = frappe.get_all("Job Card", fields=["name","assigned_technician"])
for jc in job_cards:
    tech = frappe.get_doc("Technician", jc.assigned_technician)
    print(tech.technician_name, tech.phone)

## Answer:

job_card = frappe.get_all("Job Card", fields=["name","assigned_technician"])
for job in job_card:
    tech_name,tech_phone = frappe.db.get_value("Technician",job,fields=["technician_name","phone"])
    print(tech_name,tech_phone)

---
31. Why You Should Not Add a Search Index to Every Field

Adding an index to every field is unnecessary and harmful.  
Indexes improve **read/search speed**, but they slow down **write operations** like insert, update, and delete.

Every time a record changes, the database must update **all related indexes**.  
If too many indexes exist, each write operation becomes slower and consumes more CPU and disk space.

### Performance Cost of Over-Indexing

1. **Slower Inserts and Updates** – The database must update multiple indexes for every change.  
2. **More Storage Usage** – Each index takes extra disk space.  
3. **Slower Maintenance** – Query planning and index management become heavier.

Indexes should only be added to fields that are **frequently searched, filtered, or used in joins**.

---

32. API Response 

## DELETE

http://quickfix-dev.localhost:8000/api/resource/Spare Part/PH-200-PART-2026-0031

{
    "data": "ok"
}

## PUT 

http://quickfix-dev.localhost:8000/api/resource/Spare Part/PH-200-PART-2026-0031

{
    "data": {
        "name": "LP-114-PART-2026-0014",
        "owner": "Administrator",
        "creation": "2026-03-06 15:22:38.723970",
        "modified": "2026-03-09 18:50:08.502976",
        "modified_by": "Administrator",
        "docstatus": 0,
        "idx": 0,
        "part_name": "Laptop Keyboard Backlit",
        "part_code": "LP-114",
        "compatible_device_type": "Laptop",
        "unit_cost": 1500.0,
        "selling_price": 2200.0,
        "stock_qty": 18.0,
        "reorder_level": 6.0,
        "is_active": 1,
        "doctype": "Spare Part"
    }
}

## POST

http://quickfix-dev.localhost:8000/api/resource/Spare Part

body :
{
    "part_name":"Battery",
    "part_code":"PH-200",
    "compatible_device_type":"Smartphone",
    "unit_cost":2000,
    "selling_price":3000,
    "stock_qty":100,
    "reorder_level":5,
    "is_active":1
}

## GET

http://quickfix-dev.localhost:8000/api/resource/Job Card

{
    "data": [
        {
            "name": "JC-2026-00019"
        },
        {
            "name": "JC-2026-00018"
        }
    ]
}

http://quickfix-dev.localhost:8000/api/resource/Job Card/JC-2026-00019

{
    "data": {
        "name": "JC-2026-00019",
        "owner": "Administrator",
        "creation": "2026-03-06 15:28:03.224429",
        "modified": "2026-03-06 15:35:09.057130",
        "modified_by": "Administrator",
        "docstatus": 0,
        "idx": 0,
        "customer_name": "Manoj",
        "customer_phone": "9223344556",
        "customer_email": "manoj@mail.com",
        "device_type": "Tablet",
        "device_brand": "Samsung",
        "imei_or_serial": "SM-T500",
        "problem_description": "Display cracked",
        "assigned_technician": "TECH-0004",
        "diagnosis_notes": "Display replaced",
        "estimated_cost": 3900.0,
        "priority": "Normal",
        "parts_total": 3900.0,
        "labour_charge": 1500.0,
        "final_amount": 5400.0,
        "payment_status": "Unpaid",
        "final": 0.0,
        "status": "Ready For Delivery",
        "doctype": "Job Card",
        "parts_used": [
            {
                "name": "stg3ghcdsk",
                "owner": "Administrator",
                "creation": "2026-03-06 15:28:03.224429",
                "modified": "2026-03-06 15:35:09.057130",
                "modified_by": "Administrator",
                "docstatus": 0,
                "idx": 1,
                "part": "TB-121-PART-2026-0021",
                "part_name": "Tablet 10\" Display",
                "unit_price": 3900.0,
                "quantity": 1.0,
                "total_price": 3900.0,
                "parent": "JC-2026-00019",
                "parentfield": "parts_used",
                "parenttype": "Job Card",
                "doctype": "Part Usage Entry"
            }
        ]
    }
}

---
31. Session Cookie Auth vs Token Auth

### Session Cookie Authentication

Session cookie authentication is used when a user logs in through the browser.  
After login, the server creates a session and sends a session cookie to the browser.  
The browser automatically sends this cookie with every request.  
This method is best for normal browser-based usage.

---

### Token Authentication

Token authentication uses an API key and API secret instead of a login session.  
The client sends the token in the request header to authenticate.  
This method is mainly used for server-to-server communication or external integrations.

---

### When to Use Each

Session cookies are appropriate for **browser users** interacting with the Frappe UI.  
Token authentication is appropriate for **backend services, scripts, or external systems** calling the API.
---

32. Explain retry behavior: how many times does Frappe retry a failed background job by
default?

If a background job fails, it will not retry automatically. The job is marked Failed immediately.

---
33.  Risks of `allow_guest=True` Endpoints

`allow_guest=True` allows anyone on the internet to call that API without logging in.  
This removes authentication protection, so the endpoint must be extremely careful about what it exposes.

### 1. Data Leakage

Attackers can call the endpoint repeatedly and extract sensitive information such as customer data, phone numbers, or internal records if the method returns database results.

### 2. Abuse / Spam Requests

Since no login is required, attackers can send thousands of requests (bots or scripts).  
This can overload the server, trigger heavy database queries, or create denial-of-service conditions.

### 3. Unauthorized Data Manipulation

If the endpoint allows creating or updating records, attackers can insert fake data, modify records, or corrupt system data without any authentication.

### Conclusion

Guest endpoints must strictly validate input, limit what data is returned, and avoid write operations whenever possible.

---

34. Server Script Sandbox – Analysis

### Python Functions / Modules Blocked

Server Scripts run inside a restricted sandbox.  
Many Python modules are blocked for security reasons.

Examples of blocked modules/functions include:
- `os` (file system access)
- `subprocess` (running system commands)
- `socket` (network access)
- `open()` for reading/writing files
- `import` of unsafe system modules

These restrictions prevent server scripts from accessing the OS or executing arbitrary commands.

---

### 3 Things You Cannot Do in Server Script (but can in App Code)

1. Access the operating system or file system (`os`, file read/write).  
2. Run shell commands or external programs (`subprocess`).  
3. Import arbitrary Python libraries or install dependencies.

App code has full Python capability, while Server Scripts run in a restricted environment.

---

### When Server Scripts Are Acceptable

1. Small business logic changes such as validating a field or auto-setting a value.  
2. Quick automation like sending a notification or updating a field when a document is saved.

These are lightweight and low-risk modifications.

---

### When You Should Use App Code Instead

1. Complex business logic involving multiple DocTypes, heavy queries, or integrations.  
2. Features requiring version control, testing, or long-term maintenance.

These require structured development and deployment.

---

### Governance / Maintainability Risk

Server Scripts are stored in the database, not in the app repository.  
They can be edited directly in production without code review.  
This makes auditing changes difficult and increases the risk of hidden logic or accidental breakage.

Over time, too many server scripts create "shadow code" that is hard to maintain and migrate.

---

35. Frappe Cache 

### 1. `frappe.cache.get_value("bootinfo")`

`bootinfo` contains data sent to the browser when the Desk loads.  
It includes user information, roles, permissions, system defaults, installed apps, and workspace settings needed to initialize the UI.

---

### 2. `frappe.cache.get_value("quickfix:translations")`

Translations are cached in Redis to avoid loading language files repeatedly.  
Frappe stores translated labels and messages so UI text can be quickly returned based on the user's selected language.

---

### 3. Running `frappe.clear_cache()`

When `frappe.clear_cache()` is executed:

- Cached metadata and permissions are cleared.
- The next browser reload forces Frappe to rebuild cache data.
- Desk may reload menus, roles, and workspace information again.
- This ensures the system reflects recent changes.

---

## 5 Things Frappe Caches in Redis

1. **Bootinfo** – Data used to initialize the Desk UI.  
2. **DocType Metadata (meta)** – Field definitions, permissions, and DocType structure.  
3. **Website Context** – Website configuration and routing data.  
4. **Translations** – Language labels and translated UI text.  
5. **User Permissions** – Cached permission rules for faster access control checks.