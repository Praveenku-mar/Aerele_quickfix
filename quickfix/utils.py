import frappe
import qrcode
import base64
from io import BytesIO
from frappe.utils import today

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

    today_date = today()

    if frappe.db.exists(
        "Audit Log",
        {
            "action": "low_stock_check",
            "timestamp": ["like", today_date + "%"]
        },
        "name"
    ):
        return

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

    revenue = frappe.db.sql("""
        SELECT assigned_technician, parts_total, final_amount, labour_charge
        FROM `tabJob Card`
        WHERE status = 'Delivered'
        AND creation >= DATE_FORMAT(CURDATE() - INTERVAL 1 MONTH, '%Y-%m-01')
        AND creation < DATE_FORMAT(CURDATE(), '%Y-%m-01')
    """, as_dict=True)

    if not revenue:
        return

    result = {}
    total_revenue = 0
    parts_total = 0

    for row in revenue:

        tech = row.get("assigned_technician")

        if tech not in result:
            result[tech] = {
                "total_charge": 0
            }

        result[tech]["total_charge"] += row.get("labour_charge") or 0

        parts_total += row.get("parts_total") or 0
        total_revenue += row.get("final_amount") or 0


    html = """
            <div style="font-family: Arial, sans-serif; background:#f4f6f9; padding:20px;">

        <div style="max-width:720px; margin:auto; background:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 3px 10px rgba(0,0,0,0.15);">

        <!-- Header -->

        <div style="background:linear-gradient(90deg,#2c3e50,#4ca1af); color:white; padding:18px; text-align:center;">
        <h2 style="margin:0;">QuickFix Monthly Revenue Report</h2>
        <p style="margin:5px 0 0 0; font-size:13px;">Service Performance Summary</p>
        </div>

        <!-- Content -->

        <div style="padding:20px;">

        <p style="font-size:14px; color:#444;">
        Here is the revenue summary for all delivered service jobs.
        </p>

        <table style="width:100%; border-collapse:collapse; margin-top:15px; font-size:14px;">

        <tr style="background:#34495e; color:white;">
        <th style="padding:10px;">Technician</th>
        <th style="padding:10px;">Labour Revenue</th>
        </tr>

        {% for tech, data in technician_revenue.items() %}

        <tr style="text-align:center; border-bottom:1px solid #eee;">
        <td style="padding:10px;">{{ tech }}</td>

        <td style="padding:10px; font-weight:bold; color:#2c3e50;">
        {{ frappe.format_value(data.total_charge, {"fieldtype":"Currency"}) }}
        </td>
        </tr>

        {% endfor %}

        </table>


        <!-- Summary Cards -->

        <div style="display:flex; gap:12px; margin-top:20px;">

        <div style="flex:1; background:#ecf0f1; padding:14px; border-radius:6px; text-align:center;">
        <p style="margin:0; font-size:13px; color:#666;">Parts Revenue</p>
        <h3 style="margin:5px 0; color:#2c3e50;">
        {{ frappe.format_value(parts_total, {"fieldtype":"Currency"}) }}
        </h3>
        </div>

        <div style="flex:1; background:#e8f6f3; padding:14px; border-radius:6px; text-align:center;">
        <p style="margin:0; font-size:13px; color:#666;">Total Revenue</p>
        <h3 style="margin:5px 0; color:#27ae60;">
        {{ frappe.format_value(total_revenue, {"fieldtype":"Currency"}) }}
        </h3>
        </div>

        </div>

        </div>

        <!-- Footer -->

        <div style="background:#f1f1f1; text-align:center; padding:12px; font-size:12px; color:#777;">
        QuickFix Service Management System<br>
        Automated Monthly Revenue Report
        </div>

        </div>

        </div>
            """

    message = frappe.render_template(html, {
        "technician_revenue": result,
        "total_revenue": total_revenue,
        "parts_total": parts_total
    })
    email = frappe.get_single_value("QuickFix Settings","manager_email")
    frappe.sendmail(
        recipients=email,
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