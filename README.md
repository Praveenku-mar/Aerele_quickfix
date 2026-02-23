### QuickFix

It a task

## Configuration Files Explanation

`site_config.json` stores configuration values specific to an individual site, such as database name, credentials, and developer_mode.  
`common_site_config.json` stores shared settings that apply to all sites within the same bench, such as db_host or Redis configuration.  
If you place a secret like a production database password inside `common_site_config.json`, every site under that bench can access it.  

## Bench Start Processes

When running `bench start`, the following four processes are launched:

1. **web** – Handles incoming HTTP requests and serves the Frappe application.
2. **worker** – Executes background jobs from the Redis queue.
3. **scheduler** – Enqueues scheduled tasks at defined intervals (cron-like behavior).
4. **socketio** – Manages real-time communication such as notifications and live updates.

If the worker process crashes, background jobs stop executing immediately but remain queued in Redis.  
The scheduler will continue enqueueing new jobs, causing the queue to grow.  
No background processing resumes until the worker process is restarted.  
This can delay emails, reports, integrations, and any async tasks dependent on the queue.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app quickfix
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/quickfix
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit

## Step 1 - Routing

## 1. What handles `/api/method/quickfix.api.get_job_summary` and how does Frappe find it?

The Python function `get_job_summary` inside the file `quickfix/api.py` handles this request.  
Frappe parses the dotted path `quickfix.api.get_job_summary`, imports the `api.py` module from the `quickfix` app, and then executes the `get_job_summary` function.  
This works only if the function is whitelisted using `@frappe.whitelist()`.  
The `/api/method/` route dynamically resolves and executes whitelisted Python methods.

---

## 2. What happens differently with `/api/resource/Job Card/JC-2024-0001` compared to `/api/method/`?

`/api/resource/` does not call a custom Python function directly.  
Instead, it uses Frappe’s built-in REST controller to fetch a document from the database based on the DocType (`Job Card`) and document name (`JC-2024-0001`).  
It automatically applies permission checks, loads the document using ORM, and returns it as JSON.  
Unlike `/api/method/`, this route interacts with DocTypes through standard CRUD logic rather than executing arbitrary Python code.

---

## 3. What handles `/track-job` and why?

The `/track-job` route is handled by a custom route defined in the app’s `hooks.py` (via `website_route_rules`) or by a file inside the app’s `www/track-job.py` or `www/track-job.html`.  
If it is a website route, Frappe maps the URL to the corresponding file in the `www` directory.  
If it is an API-style endpoint, it may map to a whitelisted Python method defined in hooks.  
Frappe resolves it based on route configuration rather than the default `/api/` router.

## Step 2 - Session & CSRF

## 1. X-Frappe-CSRF-Token – Where it comes from and what happens if omitted

The `X-Frappe-CSRF-Token` value comes from the current user session created after login.  
Frappe generates this token and stores it inside the session to protect against CSRF (Cross-Site Request Forgery) attacks.  
When a POST request is sent, the browser includes this token to prove the request came from a trusted session.  
If you omit it, Frappe will reject the request with a 403 error because it treats the request as unsafe.

---

## 2. Output of `frappe.session.data` in bench console

When you run `import frappe; frappe.session.data`, it shows the current session details.  

In bench console run frappe.session.data, it returns None. In frappe.session, it returns the user and csrf_token.

## Step 3 - Error visibility

## 1. With `developer_mode: 1` – Trigger a Python Exception

<!-- The browser receives the full traceback.  
It shows the exact error message, file path, and line number.  
This exposes internal code details.  
It is useful for debugging but unsafe for public environments.

--- -->

## 2. With `developer_mode: 0` – Trigger the Same Exception

When I tested this by triggering a simple exception, I received the same error message.  
<!-- The browser receives a generic error message like "Internal Server Error".  
The traceback is hidden.  
This prevents exposing file paths, logic, and sensitive system details.  
This is critical in production to avoid leaking internal information.

--- -->

## 3. Where Do Production Errors Go?

Errors are logged in Frappe error logs.  
They are stored in the **Error Log DocType** and server log files.  
Developers must check logs manually.  
Users never see internal error details.

## Step 4 - Permission check location:

## Question

In a whitelisted method, call `frappe.get_doc("Job Card", name)` without `ignore_permissions`.  
Then log in as a QF Technician user who is not assigned to that job.  
What error is raised and at what layer does Frappe stop the request?

---

Frappe raises a `frappe.exceptions.PermissionError`.  
The error message will say "Not permitted" or "You do not have enough permissions".  
The request is stopped at the permission validation layer inside the ORM (`frappe.model.document`).  
The document is never returned because Frappe blocks access before business logic continues.

