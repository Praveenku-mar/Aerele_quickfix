import frappe
from frappe.utils import now

def log_change(doc, method):
    # if doc.doctype == "Audit Log":
    #     return  
    doctype = ['Technician','Device Type','Spare Part','Job Card','QuickFix Settings','Service Invoice',"Part Usage Entry"]
    if doc.doctype in doctype:
        audit = frappe.new_doc("Audit Log")
        audit.doctype_name = doc.doctype
        audit.document_id = doc.name
        audit.action = method
        audit.user = frappe.session.user
        audit.timestamp = now()
        audit.insert(ignore_permissions=True)


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
