import frappe
from frappe.utils import now

def log_change(doc, method):
    if doc.doctype == "Audit Log":
        return  
    doctype = ['Technician','Device Type','Spare Part','Job Card','QuickFix Settings','Service Invoice',"Part Usage Entry","Scheduled Job Log"]
    if doc.doctype in doctype:
        audit = frappe.new_doc("Audit Log")
        audit.doctype_name = doc.doctype
        audit.document_id = doc.name
        if doc.doctype == "Scheduled Job Log" and doc.scheduled_job_type == "utils.check_low_stock":
            frappe.log_error("method",method)
            audit.action = "low_stock_check"
        else:
            audit.action = method
        audit.user = frappe.session.user
        audit.timestamp = now()
        audit.insert(ignore_permissions=True)
        # frappe.db.commit()


def log_login(login_manager):
    doc = frappe.get_last_doc("Activity Log")
    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": "Activity Log",
        "document_id": doc.name,
        "action": "Login",
        "user": frappe.session.user,
        "timestamp": now()
    }).insert(ignore_permissions=True)


def log_logout(login_manager=None):
    doc = frappe.get_last_doc("Activity Log")
    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": "Activity Log",
        "document_id": doc.name,
        "action": "Logout",
        "user": frappe.session.user,
        "timestamp": now()
    }).insert(ignore_permissions=True)
