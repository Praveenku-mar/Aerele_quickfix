import frappe
from frappe.query_builder import DocType
from frappe.utils import nowdate, now_datetime,now
from datetime import datetime, timedelta
import time
import requests
import hashlib
import hmac
import json


@frappe.whitelist()
def get_job_summary():
	pass


@frappe.whitelist()
def get_overdue_jobs():
	jc = DocType("Job Card")
	result = (
		frappe.qb.from_(jc)
		.select(jc.name, jc.customer_name, jc.assigned_technician, jc.creation)
		.where(jc.status.isin(["Pending Diagnosis", "In Repair"]))
		.run(as_dict=True)
	)
	return result


@frappe.whitelist()
def transfer_job(from_tech, to_tech):
	try:
		frappe.db.sql(
			"""
			UPDATE `tabJob Card`
			SET technician = %s
			WHERE technician = %s
			AND status = 'Open'
			""",
			(to_tech, from_tech),
		)
		frappe.db.commit()
	except Exception:
		frappe.db.rollback()
		frappe.log_error(title="Error Message", message=frappe.get_traceback())
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
							
							<tr>
								<td style="background:#1f2937;padding:20px;text-align:center;color:#ffffff;">
									<h2 style="margin:0;font-size:22px;">QuickFix Service Center</h2>
									<p style="margin:5px 0 0;font-size:14px;opacity:0.8;">
										Job Completion Notification
									</p>
								</td>
							</tr>
		
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
											<td>{nowdate()}</td>
										</tr>
									</table>
		
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
	)


@frappe.whitelist()
def share_job_card(job_card_name, user_email):
	frappe.share.add(
		"Job Card",
		job_card_name,
		user_email,
		read=1,
		write=0,
		share=0,
	)
	return "Successfully Shared"

@frappe.whitelist()
def manager_only_action():
    frappe.only_for("QF Manager")
    return "Access Granted. Manager action executed."



@frappe.whitelist()
def get_job_cards_unsafe():
    return frappe.get_all(
        "Job Card",
        fields="*"
    )


@frappe.whitelist()
def get_job_cards_safe():
	user = frappe.session.user
	frappe.log_error(user)
	roles = frappe.get_roles(user)

	rows = frappe.get_list(
		"Job Card",
		fields=[
			"name",
			"customer_name",
			"customer_phone",
			"customer_email",
			"status",
			"assigned_technician"
		]
	)
	frappe.log_error("1111",rows)
	if "QF Manager" not in roles:
		for row in rows:
			row.pop("customer_phone", None)
			row.pop("customer_email", None)

	return rows


@frappe.whitelist()
def custom_get_count(doctype,filters=None, debug=False, cache=False):
	print("12345")
	frappe.log_error("21345678")
	doc = frappe.new_doc("Audit Log")
	doc.doctype_name=doctype
	doc.action="count_queried"
	doc.timestamp=now()
	doc.user=frappe.session.user
	doc.insert(ignore_permissions=True)
	frappe.db.commit()
	from frappe.client import get_count
	return get_count(doctype, filters, debug, cache)



@frappe.whitelist()
def get_status_chart_data():
	cache_key = "job_card_status_chart"
	data = frappe.cache.get_value(cache_key)

	if not data:

		data = frappe.db.sql("""
			SELECT status, COUNT(name) as total
			FROM `tabJob Card`
			GROUP BY status
			""", as_list=True
			)
		frappe.cache.set_value(cache_key,data,expires_in_sec=300)
	labels = []
	values = []

	for d in data:
		labels.append(d[0])
		values.append(d[1])

	return {
		"labels": labels,
		"datasets": [
			{
				"name": "Job Count",
				"values": values
			}
		],
		"type": "bar"
	}


# @frappe.whitelist(allow_guest=True)
# def get_docc():
#     try:
#         frappe.get_doc("job Card")
#     except Exception as e:
#         frappe.log_error("Failed Job",e)
@frappe.whitelist()
def bulk_cancelled_loop():
	start = time.time()

	drafts = frappe.get_all("Job Card", filters={"status": "Draft"}, pluck="name")

	for name in drafts:
		frappe.db.set_value("Job Card", name, "status", "Cancelled")

	frappe.db.commit()

	end = time.time()
	print(f"Time :{end-start}'s")

@frappe.whitelist()
def bulk_cancelled():
	start = time.time()
	frappe.db.sql("""
	UPDATE `tabJob Card` 
	SET status = "Cancelled"
	WHERE status = "Draft"
	ORDER BY creation
	LIMIT 1000
	"""
	)
	frappe.db.commit()
	end = time.time()
	print(f"Time :{end-start}'s")


@frappe.whitelist()
def insert_audit_logs_bulk(n: int = 500) -> float:
	"""
	Insert *n* Audit Log records using frappe.db.bulk_insert.
	Fields: doctype_name, document_id, action, user, timestamp
	Returns elapsed seconds.
	"""
	now = now_datetime()
	fields = [
		"name", "owner", "creation", "modified",
		"modified_by", "docstatus", "idx",
		"doctype_name", "action", "user", "timestamp",
	]

	rows = []
	current_count = frappe.db.count("Audit Log")
	year = datetime.now().year
	start = time.time()
	for i in range(n):
		row_name = f"AL-{year}-{current_count + i + 1:05d}"
		rows.append((
			row_name,                        # name
			"Administrator",                 # owner
			now,                             # creation
			now,                             # modified
			"Administrator",                 # modified_by
			0,                               # docstatus
			i,                               # idx
			"Job Card",                      # doctype_name
			"Cancelled",                     # action
			"Administrator",                 # user
			now,                             # timestamp (Asia/Kolkata stored as UTC)
		))
	frappe.db.bulk_insert(
		"Audit Log",
		fields=fields,
		values=rows,
		ignore_duplicates=True,
	)
	frappe.db.commit()
	end = time.time()
	print(f"Time :{end-start}'s")


@frappe.whitelist()
def bulk_insert_loop():
	start = time.perf_counter()

	for i in range(500):
		log = frappe.new_doc("Audit Log")
		log.doctype_name = "Job Card",
		log.action = "Cancelled",
		log.timestamp = now,
		log.user = "Admin"

	frappe.db.commit()

	end = time.time()
	print(f"Time :{end-start}'s")



# praveenkumar@praveenkumar-ThinkPad-T480:~/frappe-bench$ bench console
# Apps in this namespace:
# frappe, quickfix

# In [1]: from quickfix.api import bulk_cancelled,bulk_cancelled_loop

# In [2]: bulk_cancelled()
# Time :0.001634359359741211's

# In [3]: bulk_cancelled_loop()
# Time :0.015452861785888672's

# In [4]: from quickfix.api import bulk_insert_loop,insert_audit_logs_bulk

# In [5]: bulk_insert_loop()
# Time :1773033297.7144365's

# In [6]: insert_audit_logs_bulk()
# Time :0.059677839279174805's


@frappe.whitelist(allow_guest=True)
def get_job_summary():
	job_card = frappe.form_dict.get("job_card")
	print(job_card)
	if not job_card:
		frappe.response['http_status_code'] = 404
		return {"error":"Job Card name Required"}

	data = frappe.db.get_value("Job Card",job_card,
		['status','assigned_technician','labour_charge','parts_total','final_amount',"payment_status",'delivery_date'],
		as_dict=True
		)

	if not data:
		frappe.response['http_status_code'] = 404
		return {"error":"Not found"}

	return data

rate_limit = 5

@frappe.whitelist(allow_guest=True)
def get_job_by_phone():
	ip = frappe.local.request_ip or 'unknown'
	cache_key = f"rate_limit:{ip}"

	calls = frappe.cache().get(cache_key) or 0

	if int(calls) >= rate_limit:
		frappe.response["http_status_code"] = 429
		return {"error": "Rate limit exceeded. Try again later."}

	frappe.cache().set(cache_key, int(calls) + 1, 60)

	phone = frappe.form_dict.get("phone_number")

	if not phone:
		frappe.response['http_status_code'] = 400
		return {"error":"Phone number is required"}

	job = frappe.db.get_value("Job Card",
		{"customer_phone":phone},
		[
			"name","status","assigned_technician","delivery_date","final_amount",'labour_charge','parts_total'
		],
		as_dict=True
	)

	if not job:
		frappe.response['http_status_code'] = 404
		return {"error":"Not found"}

	return job



def web_hook(doctype,method):
	id = f"{doctype.name}:job_submitted:{int(time.time())}"
	webhook_id = hashlib.sha256(id.encode()).hexdigest()

	frappe.log_error("webhook_id",webhook_id)
	frappe.enqueue(
        method="quickfix.api.send_webhook",
		queue="default",
		timeout=30,
        job_card_name=doctype.name,
        retry=0,
		webhook_id=webhook_id
    )


def send_webhook(job_card_name,webhook_id,retry=0):
	
	settings = frappe.get_single("QuickFix Settings")

	if not settings.webhook_url:
		return

	doc = frappe.get_doc("Job Card",job_card_name)

	payload = {
		"event":"job_submitted",
		"job_card":doc.name,
		"customer":doc.customer_name,
		"amount":doc.final_amount
	}

	if frappe.db.exists("Audit Log",{"webhook_id":webhook_id}):
		return

	try:
		r = requests.post(
			settings.webhook_url,
			json=payload,
			timeout=5
		)
		r.raise_for_status()

		frappe.get_doc({
			"doctype":"Audit Log",
			"doctype_name":"Job Card",
			"document_id":job_card_name,
			"action":"on_submitted",
			"user":frappe.session.user,
			"timestamp":now(),
			"webhook_id":webhook_id
		}).insert(ignore_permissions=True)
		frappe.db.commit()

	except Exception as e:
		frappe.log_error(f"webhook failed: {e}","Webhook Error")

		if retry < 3:
			frappe.enqueue(
				method="quickfix.api.send_webhook",
				job_card_name = job_card_name,
				enqueue_after_commit=True,
				queue="default",
				timeout=300,
				delay=60
			)





@frappe.whitelist(allow_guest=True)
def payment_webhook():

	# 1. Read raw request body
	payload = frappe.request.data

	# 2. Validate HMAC signature
	secret = frappe.conf.get("payment_webhook_secret", "")
	signature = frappe.get_request_header("X-Signature")

	expected = hmac.new(
		secret.encode(),
		payload,
		hashlib.sha256
	).hexdigest()


	print("==================================",expected)
	print("=================================",signature)
	if not signature or not hmac.compare_digest(expected, signature):
		frappe.throw("Invalid signature", frappe.AuthenticationError)

	# 3. Parse payload
	data = json.loads(payload)

	ref = data.get("ref")
	amount = data.get("amount")

	# 4. Deduplication check
	if frappe.db.exists(
		"Audit Log",
		{"action": "payment_received", "document_name": ref}
	):
		return {"status": "duplicate", "message": "Already processed"}

	# 5. Update Job Card payment status
	job = frappe.get_doc("Job Card", ref)
	job.payment_status = "Paid"
	job.paid_amount = amount
	job.save(ignore_permissions=True)

	# 6. Log to Audit Log
	frappe.get_doc({
		"doctype": "Audit Log",
		"doctype_name":"Job Card",
		"action": "payment_received",
		"document_id": ref,
		"user": "Administrator",
		"timestamp": now()

	}).insert(ignore_permissions=True)

	frappe.db.commit()

	return {"status": "ok"}