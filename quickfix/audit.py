import frappe
from frappe.utils import now

def log_change(doc, method):
    # if doc.doctype == "Audit Log":
    #     return  
    doc = ['Technician','Device Type','Spare Part','Job Card','QuickFix Settings','Service Invoice',"Part Usage Entry"]
    if doc.doctype in doc:
        audit = frappe.new_doc("Audit Log")
        audit.doctype_name = doc.doctype
        audit.document_id = doc.name
        audit.action = method
        audit.user = frappe.session.user
        audit.timestamp = now()
        audit.insert(ignore_permissions=True)


def log_login(login_manager):
    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": "User",
        "document_id": frappe.session.sid,
        "action": "Login",
        "user": frappe.session.user,
        "timestamp": now()
    }).insert(ignore_permissions=True)


def log_logout(login_manager=None):
    frappe.get_doc({
        "doctype": "Audit Log",
        "doctype_name": "User",
        "document_id": frappe.session.sid,
        "action": "Logout",
        "user": frappe.session.user,
        "timestamp": now()
    }).insert(ignore_permissions=True)
