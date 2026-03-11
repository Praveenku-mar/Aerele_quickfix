Dear {{ doc.customer_name or "Customer" }},

We are pleased to inform you that your vehicle / job is ready for delivery.

Job Card: {{ doc.name }}
Status: {{ doc.status }}
{% if doc.expected_delivery_date %}
Expected Delivery Date: {{ frappe.format(doc.expected_delivery_date, {"fieldtype": "Date"}) }}
{% endif %}

Please visit us at your earliest convenience to collect it.

Thank you for choosing us.

Regards,
{{ doc.company or "Our Service Team" }}