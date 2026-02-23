import frappe
from frappe.query_builder import DocType


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

