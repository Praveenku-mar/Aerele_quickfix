import frappe
from frappe.utils import now

def log_change(doc, method):
    if doc.doctype == "Audit Log":
        return  

    audit = frappe.new_doc("Audit Log")
    audit.doctype_name = doc.doctype
    audit.document_id = doc.name
    audit.action = method
    audit.user = frappe.session.user
    audit.timestamp = now()
    audit.insert(ignore_permissions=True)