import frappe
from frappe.query_builder import DocType
from datetime import datetime


@frappe.whitelist()
def get_job_summary():
    pass

@frappe.whitelist()
def get_overdue_jobs():
    JC = DocType("Job Card")
    result = (
    frappe.qb.from_(JC)
    .select(JC.name, JC.customer_name, JC.assigned_technician, JC.creation)
    .where(JC.status.isin(["Pending Diagnosis", "In Repair"]))
    .run(as_dict=True)
    )

    return result

@frappe.whitelist()
def transfer_job(from_tech,to_tech):
    try:
        frappe.db.sql("""
        UPDATE `tabJob Card`
        SET technician = %s
        WHERE technician = %s
        AND status = 'Open'
        """, (to_tech, from_tech))
        frappe.db.commit()
    except Exception as e:
        frappe.db.rollback()
        frappe.log_error(
        title="Error Message",
        message=frappe.get_traceback()
        )
        raise


def send_job_ready_email(job_card):
    doc = frappe.get_doc("Job Card", job_card)

    html = f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;padding:0;background:#f2f4f8;font-family:Arial,Helvetica,sans-serif;">
            <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                    <td align="center" style="padding:30px 15px;">
                        
                        <table width="600" cellpadding="0" cellspacing="0" 
                               style="background:#ffffff;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,0.08);overflow:hidden;">
                            
                            <!-- Header -->
                            <tr>
                                <td style="background:#1f2937;padding:20px;text-align:center;color:#ffffff;">
                                    <h2 style="margin:0;font-size:22px;">QuickFix Service Center</h2>
                                    <p style="margin:5px 0 0;font-size:14px;opacity:0.8;">
                                        Job Completion Notification
                                    </p>
                                </td>
                            </tr>
        
                            <!-- Body -->
                            <tr>
                                <td style="padding:30px;">
                                    <p style="font-size:16px;margin:0 0 15px;">
                                        Dear <b>{doc.customer_name}</b>,
                                    </p>
        
                                    <p style="font-size:15px;margin:0 0 20px;color:#444;">
                                        Great news! Your job 
                                        <b style="color:#1f2937;">{doc.name}</b> 
                                        has been successfully completed and is ready for delivery.
                                    </p>
        
                                    <!-- Details Box -->
                                    <table width="100%" cellpadding="10" cellspacing="0" 
                                           style="border:1px solid #e5e7eb;border-radius:6px;">
                                        <tr>
                                            <td style="background:#f9fafb;"><b>Job Card No</b></td>
                                            <td>{doc.name}</td>
                                        </tr>
                                        <tr>
                                            <td style="background:#f9fafb;"><b>Total Amount</b></td>
                                            <td style="color:#16a34a;font-weight:bold;">
                                                ₹ {doc.final_amount}
                                            </td>
                                        </tr>
                                        <tr>
                                            <td style="background:#f9fafb;"><b>Delivery Date</b></td>
                                            <td>{datetime.nowdate()}</td>
                                        </tr>
                                    </table>
        
                                    <!-- CTA Button -->
                                    <div style="text-align:center;margin:30px 0;">
                                        <a href="#" 
                                           style="background:#2563eb;color:#ffffff;
                                                  padding:12px 25px;
                                                  text-decoration:none;
                                                  border-radius:5px;
                                                  font-size:14px;
                                                  display:inline-block;">
                                            Contact Support
                                        </a>
                                    </div>
        
                                    <p style="font-size:14px;color:#666;margin:0;">
                                        Thank you for choosing QuickFix.
                                    </p>
                                </td>
                            </tr>
        
                            <!-- Footer -->
                            <tr>
                                <td style="background:#f9fafb;padding:20px;text-align:center;font-size:13px;color:#555;">
                                    <b>QuickFix</b><br>
                                    Phone: 9092837965<br>
                                    Email: quickfix@gmail.com
                                </td>
                            </tr>
        
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """

    frappe.sendmail(
        recipients=[doc.customer_email],
        subject=f"Job {doc.name} is Ready for Delivery",
        message=html,
        now=True
    )

@frappe.whitelist()
def share_job_card(job_card_name,user_email):
    frappe.share.add(
        "Job Card",
        job_card_name,
        user_email,
        read=1,
        write=0,
        share=0
    )

    return "Successfully Shared"

@frappe.whitelist()
def manager_only_action():
    frappe.only_for("QF Manager")
    return "Access Granted. Manager action executed."


@frappe.whitelist()
def get_job_card_unsafe():
    return frappe.get_all("Job Card",fields=["*"])


@frappe.whitelist()
def get_job_card_safe():
    user = frappe.session.user
    role = frappe.get_roles(user)

    data = frappe.get_list("Job Card",
        fields=["name","customer_name","customer_phone","customer_email","assigned_technician","status","total_amount"]
    )

    if "QF Manager" not in role:
        for row in data:
            row.pop("customer_phone",None)
            row.pop("customer_email", None)
    
    return data
