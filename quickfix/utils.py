import frappe
import qrcode
import base64
from io import BytesIO
from frappe.utils import today,now,get_first_day, add_months,get_last_day

def get_shop_name():
    return frappe.get_single_value("QuickFix Settings","shop_name")

def format_job_id(value):
    return f"JOB#{value}"


@frappe.whitelist()
def generate_qr_code(data):

    qr = qrcode.make(data)

    buffer = BytesIO()
    qr.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return qr_base64

    

def check_low_stock():

    start = today() + " 00:00:00"
    end = today() + " 23:59:59"

    exists =  frappe.db.exists(
        "Audit Log",
        {
            "action": "low_stock_check",
            "timestamp": ["between", [start, end]]
        }
        )

    frappe.log_error("exists",exists)
    if exists: 
        return
    
    audit = frappe.new_doc("Audit Log")
    audit.doctype_name = "Scheduled Job Log"
    audit.action = "low_stock_check"
    audit.user = frappe.session.user
    audit.timestamp = now()
    audit.insert(ignore_permissions=True)

    frappe.log_error("End")

    low_parts = frappe.db.sql("""
        SELECT name, part_name, stock_qty, reorder_level
        FROM `tabSpare Part`
        WHERE stock_qty <= reorder_level
    """, as_dict=True)

    if not low_parts:
        return

    html = """
            <div style="font-family: Arial, sans-serif; background:#f4f6f9; padding:20px;">

        <div style="max-width:650px; margin:auto; background:white; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.1);">

        <!-- Header -->

        <div style="background:#e74c3c; color:white; padding:16px; text-align:center;">
        <h2 style="margin:0;">⚠ Low Stock Alert</h2>
        <p style="margin:5px 0 0 0;">QuickFix Inventory Notification</p>
        </div>

        <!-- Content -->

        <div style="padding:20px;">

        <p style="font-size:14px;">
        The following spare parts are running <b>low in stock</b>. Please refill immediately to avoid service delays.
        </p>

        <table style="width:100%; border-collapse:collapse; margin-top:15px;">

        <tr style="background:#2c3e50; color:white;">
        <th style="padding:10px;">Part Name</th>
        <th style="padding:10px;">Available Stock</th>
        <th style="padding:10px;">Minimum Required</th>
        <th style="padding:10px;">Status</th>
        </tr>

        {% for p in low_parts %}

        <tr style="text-align:center; border-bottom:1px solid #eee;">

        <td style="padding:10px;">{{ p.part_name }}</td>

        <td style="padding:10px; color:#e74c3c; font-weight:bold;">
        {{ p.stock_qty }}
        </td>

        <td style="padding:10px;">
        {{ p.min_stock_level }}
        </td>

        <td style="padding:10px;">
        <span style="background:#ffdddd; color:#c0392b; padding:4px 8px; border-radius:4px;">
        LOW
        </span>
        </td>

        </tr>

        {% endfor %}

        </table>

        </div>

        <!-- Footer -->

        <div style="background:#f1f1f1; text-align:center; padding:12px; font-size:12px; color:#666;">
        QuickFix Service System<br>
        Automated Inventory Alert
        </div>

        </div>

        </div>
    """

    if not low_parts:
        return

    message = frappe.render_template(html, {
        "low_parts": low_parts
    })
    email = frappe.get_single_value("QuickFix Settings","manager_email")
    frappe.sendmail(recipients=email,
        subject="Low Stock Alert - QuickFix",
        message=message,
        now=True
    )



def monthly_revenue_report():

    # Previous month date range
    start = get_first_day(add_months(today(), -1))
    end = get_last_day(add_months(today(), -1))
    data = frappe.db.sql("""
        SELECT
            assigned_technician,
            COUNT(name) AS total_jobs,
            SUM(final_amount) AS total_revenue,
            SUM(parts_total) AS parts_total,
            SUM(labour_charge) AS labour_collected
        FROM `tabJob Card`
        WHERE status='Delivered'
        AND creation BETWEEN %s AND %s
        GROUP BY assigned_technician
    """, (start, end), as_dict=True)

    frappe.log_error(frappe.as_json(data), "Revenue Data")

    if not data:
        frappe.log_error("No revenue records found", "Monthly Revenue Report")
        return

    report = []

    company_total_profit = 0
    total_parts_amount = 0
    total_jobs_company = 0

    # Process technician-wise revenue
    for row in data:

        jobs = row.get("total_jobs") or 0
        parts = row.get("parts_total") or 0
        revenue = row.get("total_revenue") or 0
        labour_collected = row.get("labour_collected") or 0

        technician_earnings = jobs * 1000
        company_labour_share = jobs * 500

        company_profit = company_labour_share + parts

        report.append({
            "technician": row.get("assigned_technician"),
            "jobs": jobs,
            "revenue": revenue,
            "parts": parts,
            "labour_collected": labour_collected,
            "technician_earnings": technician_earnings,
            "company_earnings": company_labour_share,
            "profit": company_profit
        })

        company_total_profit += company_profit
        total_parts_amount += parts
        total_jobs_company += jobs

    # Email HTML Template
    html = """
    <div style="font-family:Arial;background:#f4f6f9;padding:20px">

    <div style="max-width:900px;margin:auto;background:white;border-radius:8px;
    box-shadow:0 3px 10px rgba(0,0,0,0.1);overflow:hidden">

    <div style="background:#2c3e50;color:white;padding:15px;text-align:center">
    <h2>QuickFix Monthly Revenue Report</h2>
    <p>Service Center Performance Summary</p>
    </div>

    <div style="padding:20px">

    <table style="width:100%;border-collapse:collapse">

    <tr style="background:#34495e;color:white">
    <th style="padding:10px">Technician</th>
    <th>Jobs</th>
    <th>Total Revenue</th>
    <th>Parts</th>
    <th>Labour Collected</th>
    <th>Technician Earnings</th>
    <th>Company Earnings</th>
    <th>Profit</th>
    </tr>

    {% for r in report %}

    <tr style="text-align:center;border-bottom:1px solid #eee">
    <td style="padding:10px">{{ r.technician }}</td>
    <td>{{ r.jobs }}</td>
    <td>{{ frappe.format_value(r.revenue, {"fieldtype":"Currency"}) }}</td>
    <td>{{ frappe.format_value(r.parts, {"fieldtype":"Currency"}) }}</td>
    <td>{{ frappe.format_value(r.labour_collected, {"fieldtype":"Currency"}) }}</td>
    <td>{{ frappe.format_value(r.technician_earnings, {"fieldtype":"Currency"}) }}</td>
    <td>{{ frappe.format_value(r.company_earnings, {"fieldtype":"Currency"}) }}</td>
    <td style="font-weight:bold;color:#27ae60">
    {{ frappe.format_value(r.profit, {"fieldtype":"Currency"}) }}
    </td>
    </tr>

    {% endfor %}

    </table>

    <div style="margin-top:20px;background:#ecf0f1;padding:15px;border-radius:6px">

    <p><b>Total Jobs Completed:</b> {{ total_jobs }}</p>
    <p><b>Total Spare Parts Revenue:</b> 
    {{ frappe.format_value(total_parts, {"fieldtype":"Currency"}) }}</p>

    <p><b>Total Company Profit:</b> 
    <span style="color:#27ae60;font-size:18px">
    {{ frappe.format_value(company_profit, {"fieldtype":"Currency"}) }}
    </span>
    </p>

    </div>

    </div>

    <div style="background:#f1f1f1;text-align:center;padding:10px;font-size:12px">
    QuickFix Service Management System<br>
    Automated Monthly Financial Report
    </div>

    </div>

    </div>
    """

    message = frappe.render_template(html, {
        "report": report,
        "total_jobs": total_jobs_company,
        "total_parts": total_parts_amount,
        "company_profit": company_total_profit
    })

    manager_email = frappe.get_single_value("QuickFix Settings", "manager_email")

    if not manager_email:
        frappe.log_error("Manager email not configured", "Monthly Revenue Report")
        return

    frappe.sendmail(
        recipients=[manager_email],
        subject="QuickFix Monthly Revenue Report",
        message=message,
        now=True
    )



def send_mail():
    job_card = frappe.get_all("Job Card",
            filters={"status":"Ready For Delivery"},
            fields=["name"]
        )

    if not job_card:
        return 
    
    for job in job_card:
        frappe.enqueue(
                method="quickfix.api.send_job_ready_email",
                queue="default",
                job_card=job.name
            )