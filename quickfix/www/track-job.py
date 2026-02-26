# import frappe


# def get_context(context):
#     frappe.log_error("1111111111")
#     context.no_cache = 1
#     context.allow_guest = True

#     job_id = context.name  
#     frappe.log_error("name",job_id)

#     if not job_id:
#         context.error = "Job ID missing"
#         return

#     job = frappe.get_list(
#         "Job Card",
#         filters={"name": job_id},
#         fields=[
#             "name",
#             "customer_name",
#             "status",
#             "final_amount"
#         ],
#         limit=1
#     )

#     if not job:
#         context.error = "Invalid Job ID"
#         return

#     context.job = job[0]

import frappe

def get_context(context):
    frappe.throw("Python Executed")
