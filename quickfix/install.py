import frappe
from frappe import _
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def after_app_install():
    data = [
        {
            "average_repair_hours": 24,
            "description": "Smartphone description",
            "device_type": "Smartphone",
        },
        {
            "average_repair_hours": 48,
            "description": "Laptop description",
            "device_type": "Laptop",
        },
        {
            "average_repair_hours": 24,
            "description": "Tablet description",
            "device_type": "Tablet",
        }
    ]

    for row in data:
        if not frappe.db.exists("Device Type", row["device_type"]):
            device = frappe.get_doc({
                "doctype": "Device Type",
                "device_type": row["device_type"],
                "description": row["description"],
                "average_repair_hours": row["average_repair_hours"]
            })
            device.insert(ignore_permissions=True)

    # For Single Doctype
    settings = frappe.get_single("QuickFix Settings")
    settings.shop_name = "QuickFix"
    settings.manager_email = "praveensekar223@gmail.com"
    settings.default_labour_charge = 1500
    settings.low_stock_threshold = 5
    settings.low_stock_alert_enable = 1
    settings.save(ignore_permissions=True)
    set_property()
    print("Successfully Executed after_app_install hook")



def before_uninstall():
    data = frappe.get_all("Job Card",
            filters={
                "docstatus":1
            }
        )
    if data:
        raise frappe.ValidationError(
            _("Cannot uninstall app. Submitted Job Cards exist. Please cancel all submitted Job Cards before uninstalling.")
        )


def set_property():
    make_property_setter(
        "Job Card",
        "remarks",
        "bold",
        1,
        "Check"
    )
    print("Property setter created successfully")

    