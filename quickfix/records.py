
import frappe
import json
@frappe.whitelist(allow_guest=True)
def job_card():
        data = [
{
"customer_name":"Ramesh",
"customer_phone":"9871112233",
"customer_email":"ramesh@mail.com",
"device_type":"Smartphone",
"device_brand":"OnePlus",
"imei_or_serial":"OP-NORD2",
"problem_description":"Touch not responding",
"assigned_technician":"TECH-0002",
"diagnosis_notes":"Display assembly replaced",
"estimated_cost":4200,
"parts_used":[
{"part":"SM-101","part_name":"Smartphone AMOLED Display","unit_price":4200,"quantity":1,"total_price":4200}
],
"parts_total":4200,
"labour_charge":500,
"final_amount":4700,
"status":"Ready For Delivery"
},

{
"customer_name":"Sathish",
"customer_phone":"9786543210",
"customer_email":"sathish@mail.com",
"device_type":"Laptop",
"device_brand":"Dell",
"imei_or_serial":"DL-3511",
"problem_description":"Hard disk failure",
"assigned_technician":"TECH-0003",
"diagnosis_notes":"SSD installed",
"estimated_cost":3800,
"parts_used":[
{"part":"LP-118","part_name":"Laptop 512GB SSD","unit_price":3800,"quantity":1,"total_price":3800}
],
"parts_total":3800,
"labour_charge":600,
"final_amount":4400,
"status":"In Repair"
},

{
"customer_name":"Keerthi",
"customer_phone":"9554411223",
"customer_email":"keerthi@mail.com",
"device_type":"Tablet",
"device_brand":"Apple",
"imei_or_serial":"IPAD-AIR4",
"problem_description":"Screen cracked",
"assigned_technician":"TECH-0004",
"diagnosis_notes":"Display replaced",
"estimated_cost":7200,
"parts_used":[
{"part":"TB-121","part_name":"Tablet 10\" Display","unit_price":7200,"quantity":1,"total_price":7200}
],
"parts_total":7200,
"labour_charge":800,
"final_amount":8000,
"status":"Ready For Delivery"
},

{
"customer_name":"Harish",
"customer_phone":"9442233445",
"customer_email":"harish@mail.com",
"device_type":"Smartphone",
"device_brand":"Oppo",
"imei_or_serial":"OP-A74",
"problem_description":"Front camera blurry",
"assigned_technician":"TECH-0001",
"diagnosis_notes":"Camera replaced",
"estimated_cost":1200,
"parts_used":[
{"part":"SM-108","part_name":"Smartphone Camera Module","unit_price":1200,"quantity":1,"total_price":1200}
],
"parts_total":1200,
"labour_charge":250,
"final_amount":1450,
"status":"Ready For Delivery"
},

{
"customer_name":"Dinesh",
"customer_phone":"9887766554",
"customer_email":"dinesh@mail.com",
"device_type":"Laptop",
"device_brand":"HP",
"imei_or_serial":"HP-14S",
"problem_description":"Battery not charging",
"assigned_technician":"TECH-0002",
"diagnosis_notes":"Battery replaced",
"estimated_cost":2600,
"parts_used":[
{"part":"LP-122","part_name":"Laptop Battery Pack","unit_price":2600,"quantity":1,"total_price":2600}
],
"parts_total":2600,
"labour_charge":400,
"final_amount":3000,
"status":"Ready For Delivery"
},

{
"customer_name":"Lokesh",
"customer_phone":"9331122445",
"customer_email":"lokesh@mail.com",
"device_type":"Smartphone",
"device_brand":"Samsung",
"imei_or_serial":"SM-M21",
"problem_description":"Speaker distortion",
"assigned_technician":"TECH-0003",
"diagnosis_notes":"Speaker replaced",
"estimated_cost":700,
"parts_used":[
{"part":"SM-107","part_name":"Smartphone Speaker Module","unit_price":700,"quantity":1,"total_price":700}
],
"parts_total":700,
"labour_charge":200,
"final_amount":900,
"status":"Ready For Delivery"
},

{
"customer_name":"Anitha",
"customer_phone":"9776655443",
"customer_email":"anitha@mail.com",
"device_type":"Tablet",
"device_brand":"Lenovo",
"imei_or_serial":"LN-TB8505",
"problem_description":"Charging slow",
"assigned_technician":"TECH-0004",
"diagnosis_notes":"Charging port replaced",
"estimated_cost":900,
"parts_used":[
{"part":"SM-104","part_name":"Smartphone Charging Port Flex","unit_price":900,"quantity":1,"total_price":900}
],
"parts_total":900,
"labour_charge":250,
"final_amount":1150,
"status":"In Repair"
},

{
"customer_name":"Vasanth",
"customer_phone":"9005566778",
"customer_email":"vasanth@mail.com",
"device_type":"Laptop",
"device_brand":"Acer",
"imei_or_serial":"ACR-ES15",
"problem_description":"Fan noise",
"assigned_technician":"TECH-0001",
"diagnosis_notes":"Cooling fan replaced",
"estimated_cost":1300,
"parts_used":[
{"part":"LP-116","part_name":"Laptop Cooling Fan","unit_price":1300,"quantity":1,"total_price":1300}
],
"parts_total":1300,
"labour_charge":350,
"final_amount":1650,
"status":"Ready For Delivery"
},

{
"customer_name":"Kumar",
"customer_phone":"9012233445",
"customer_email":"kumar@mail.com",
"device_type":"Smartphone",
"device_brand":"Realme",
"imei_or_serial":"RM-C25",
"problem_description":"Battery swelling",
"assigned_technician":"TECH-0002",
"diagnosis_notes":"Battery replaced",
"estimated_cost":1500,
"parts_used":[
{"part":"SM-103","part_name":"Smartphone Battery 5000mAh","unit_price":1500,"quantity":1,"total_price":1500}
],
"parts_total":1500,
"labour_charge":300,
"final_amount":1800,
"status":"Ready For Delivery"
},

{
"customer_name":"Bala",
"customer_phone":"9558899776",
"customer_email":"bala@mail.com",
"device_type":"Laptop",
"device_brand":"Lenovo",
"imei_or_serial":"LN-IDEAPAD3",
"problem_description":"Keyboard keys missing",
"assigned_technician":"TECH-0003",
"diagnosis_notes":"Keyboard replaced",
"estimated_cost":2100,
"parts_used":[
{"part":"LP-114","part_name":"Laptop Keyboard Backlit","unit_price":2100,"quantity":1,"total_price":2100}
],
"parts_total":2100,
"labour_charge":450,
"final_amount":2550,
"status":"Ready For Delivery"
},

{
"customer_name":"Saranya",
"customer_phone":"9446677881",
"customer_email":"saranya@mail.com",
"device_type":"Tablet",
"device_brand":"Samsung",
"imei_or_serial":"SM-T295",
"problem_description":"No power",
"assigned_technician":"TECH-0004",
"diagnosis_notes":"Battery replaced",
"estimated_cost":1600,
"parts_used":[
{"part":"TB-123","part_name":"Tablet Battery 6000mAh","unit_price":1600,"quantity":1,"total_price":1600}
],
"parts_total":1600,
"labour_charge":300,
"final_amount":1900,
"status":"In Repair"
},

{
"customer_name":"Prakash",
"customer_phone":"9888877665",
"customer_email":"prakash@mail.com",
"device_type":"Smartphone",
"device_brand":"Motorola",
"imei_or_serial":"MOTO-G40",
"problem_description":"Network issue",
"assigned_technician":"TECH-0001",
"diagnosis_notes":"Antenna replaced",
"estimated_cost":900,
"parts_used":[
{"part":"SM-110","part_name":"Smartphone Antenna Module","unit_price":900,"quantity":1,"total_price":900}
],
"parts_total":900,
"labour_charge":200,
"final_amount":1100,
"status":"Ready For Delivery"
},

{
"customer_name":"Yogesh",
"customer_phone":"9771122334",
"customer_email":"yogesh@mail.com",
"device_type":"Laptop",
"device_brand":"HP",
"imei_or_serial":"HP-PAV15",
"problem_description":"RAM upgrade",
"assigned_technician":"TECH-0002",
"diagnosis_notes":"RAM installed",
"estimated_cost":3000,
"parts_used":[
{"part":"LP-120","part_name":"Laptop 8GB RAM","unit_price":3000,"quantity":1,"total_price":3000}
],
"parts_total":3000,
"labour_charge":400,
"final_amount":3400,
"status":"Ready For Delivery"
},

{
"customer_name":"Nithya",
"customer_phone":"9665544332",
"customer_email":"nithya@mail.com",
"device_type":"Smartphone",
"device_brand":"Apple",
"imei_or_serial":"IPH-11",
"problem_description":"Battery draining fast",
"assigned_technician":"TECH-0003",
"diagnosis_notes":"Battery replaced",
"estimated_cost":3500,
"parts_used":[
{"part":"SM-103","part_name":"Smartphone Battery 5000mAh","unit_price":3500,"quantity":1,"total_price":3500}
],
"parts_total":3500,
"labour_charge":500,
"final_amount":4000,
"status":"Ready For Delivery"
},

{
"customer_name":"Sanjay",
"customer_phone":"9553344112",
"customer_email":"sanjay@mail.com",
"device_type":"Laptop",
"device_brand":"Dell",
"imei_or_serial":"DL-7480",
"problem_description":"WiFi not working",
"assigned_technician":"TECH-0004",
"diagnosis_notes":"WiFi card replaced",
"estimated_cost":1200,
"parts_used":[
{"part":"LP-130","part_name":"Laptop WiFi Card","unit_price":1200,"quantity":1,"total_price":1200}
],
"parts_total":1200,
"labour_charge":300,
"final_amount":1500,
"status":"In Repair"
},

{
"customer_name":"Ravi",
"customer_phone":"9449911223",
"customer_email":"ravi@mail.com",
"device_type":"Smartphone",
"device_brand":"Poco",
"imei_or_serial":"POCO-X3",
"problem_description":"Microphone not working",
"assigned_technician":"TECH-0001",
"diagnosis_notes":"Mic replaced",
"estimated_cost":650,
"parts_used":[
{"part":"SM-111","part_name":"Smartphone Microphone Module","unit_price":650,"quantity":1,"total_price":650}
],
"parts_total":650,
"labour_charge":200,
"final_amount":850,
"status":"Ready For Delivery"
},

{
"customer_name":"Kiran",
"customer_phone":"9884411223",
"customer_email":"kiran@mail.com",
"device_type":"Tablet",
"device_brand":"Huawei",
"imei_or_serial":"HW-M5",
"problem_description":"Display flickering",
"assigned_technician":"TECH-0002",
"diagnosis_notes":"Display replaced",
"estimated_cost":4100,
"parts_used":[
{"part":"TB-121","part_name":"Tablet 10\" Display","unit_price":4100,"quantity":1,"total_price":4100}
],
"parts_total":4100,
"labour_charge":600,
"final_amount":4700,
"status":"Ready For Delivery"
},

{
"customer_name":"Senthil",
"customer_phone":"9778899001",
"customer_email":"senthil@mail.com",
"device_type":"Laptop",
"device_brand":"Asus",
"imei_or_serial":"ASUS-X515",
"problem_description":"Touchpad not working",
"assigned_technician":"TECH-0003",
"diagnosis_notes":"Touchpad replaced",
"estimated_cost":1500,
"parts_used":[
{"part":"LP-140","part_name":"Laptop Touchpad Module","unit_price":1500,"quantity":1,"total_price":1500}
],
"parts_total":1500,
"labour_charge":350,
"final_amount":1850,
"status":"Ready For Delivery"
},

{
"customer_name":"Divya",
"customer_phone":"9442211998",
"customer_email":"divya@mail.com",
"device_type":"Smartphone",
"device_brand":"Samsung",
"imei_or_serial":"SM-A32",
"problem_description":"Power button stuck",
"assigned_technician":"TECH-0004",
"diagnosis_notes":"Button flex replaced",
"estimated_cost":500,
"parts_used":[
{"part":"SM-112","part_name":"Smartphone Button Flex","unit_price":500,"quantity":1,"total_price":500}
],
"parts_total":500,
"labour_charge":150,
"final_amount":650,
"status":"Ready For Delivery"
},

{
"customer_name":"Mohan",
"customer_phone":"9557788990",
"customer_email":"mohan@mail.com",
"device_type":"Laptop",
"device_brand":"MSI",
"imei_or_serial":"MSI-GF63",
"problem_description":"GPU overheating",
"assigned_technician":"TECH-0001",
"diagnosis_notes":"Thermal paste applied and fan cleaned",
"estimated_cost":900,
"parts_used":[
{"part":"LP-150","part_name":"Thermal Paste Kit","unit_price":900,"quantity":1,"total_price":900}
],
"parts_total":900,
"labour_charge":300,
"final_amount":1200,
"status":"Ready For Delivery"
}
]




        for record in data:
        
            job = frappe.get_doc({
                "doctype": "Job Card",
                "customer_name": record["customer_name"],
                "customer_phone": record["customer_phone"],
                "customer_email": record["customer_email"],
                "device_type": record["device_type"],
                "device_brand": record["device_brand"],
                "imei_or_serial": record["imei_or_serial"],
                "problem_description": record["problem_description"],
                "assigned_technician": record["assigned_technician"],
                "diagnosis_notes": record["diagnosis_notes"],
                "estimated_cost": record["estimated_cost"],
                "parts_total": record["parts_total"],
                "labour_charge": record["labour_charge"],
                "final_amount": record["final_amount"],
                "status": record["status"],
                "parts_used": []
            })

            # Insert child table parts
            for part in record["parts_used"]:
                job.append("parts_used", {
                    "part": part["part"],
                    "part_name": part["part_name"],
                    "unit_price": part["unit_price"],
                    "quantity": part["quantity"],
                    "total_price": part["total_price"]
                })

            job.insert(ignore_permissions=True)

        frappe.db.commit()

        print("All Job Cards Inserted Successfully")
        return "Successfully"



@frappe.whitelist(allow_guest=True)
def Spare_parts():
    parts = [
  { "part_name": "Smartphone AMOLED Display", "part_code": "SM-101", "compatible_device_type": "Smartphone", "unit_cost": 2800.00, "selling_price": 3500.00, "stock_qty": 18, "reorder_level": 5, "is_active": 1 },
  { "part_name": "Smartphone LCD Display", "part_code": "SM-102", "compatible_device_type": "Smartphone", "unit_cost": 2200.00, "selling_price": 3000.00, "stock_qty": 12, "reorder_level": 4, "is_active": 1 },
  { "part_name": "Smartphone Battery 5000mAh", "part_code": "SM-103", "compatible_device_type": "Smartphone", "unit_cost": 900.00, "selling_price": 1400.00, "stock_qty": 25, "reorder_level": 8, "is_active": 1 },
  { "part_name": "Smartphone Charging Port Flex", "part_code": "SM-104", "compatible_device_type": "Smartphone", "unit_cost": 450.00, "selling_price": 800.00, "stock_qty": 30, "reorder_level": 10, "is_active": 1 },
  { "part_name": "Smartphone Rear Camera 64MP", "part_code": "SM-105", "compatible_device_type": "Smartphone", "unit_cost": 1600.00, "selling_price": 2300.00, "stock_qty": 10, "reorder_level": 3, "is_active": 1 },
  { "part_name": "Smartphone Front Camera 16MP", "part_code": "SM-106", "compatible_device_type": "Smartphone", "unit_cost": 1200.00, "selling_price": 1700.00, "stock_qty": 14, "reorder_level": 4, "is_active": 1 },
  { "part_name": "Smartphone Speaker Module", "part_code": "SM-107", "compatible_device_type": "Smartphone", "unit_cost": 300.00, "selling_price": 600.00, "stock_qty": 40, "reorder_level": 12, "is_active": 1 },
  { "part_name": "Smartphone Power Button Flex", "part_code": "SM-108", "compatible_device_type": "Smartphone", "unit_cost": 250.00, "selling_price": 500.00, "stock_qty": 35, "reorder_level": 10, "is_active": 1 },
  { "part_name": "Smartphone Volume Button Flex", "part_code": "SM-109", "compatible_device_type": "Smartphone", "unit_cost": 250.00, "selling_price": 500.00, "stock_qty": 28, "reorder_level": 8, "is_active": 1 },
  { "part_name": "Smartphone Motherboard", "part_code": "SM-110", "compatible_device_type": "Smartphone", "unit_cost": 4500.00, "selling_price": 6000.00, "stock_qty": 6, "reorder_level": 2, "is_active": 1 },

  { "part_name": "Laptop 15.6\" FHD Display", "part_code": "LP-111", "compatible_device_type": "Laptop", "unit_cost": 5000.00, "selling_price": 6500.00, "stock_qty": 8, "reorder_level": 3, "is_active": 1 },
  { "part_name": "Laptop 14\" HD Display", "part_code": "LP-112", "compatible_device_type": "Laptop", "unit_cost": 4200.00, "selling_price": 5600.00, "stock_qty": 9, "reorder_level": 3, "is_active": 1 },
  { "part_name": "Laptop Battery 6 Cell", "part_code": "LP-113", "compatible_device_type": "Laptop", "unit_cost": 1800.00, "selling_price": 2500.00, "stock_qty": 16, "reorder_level": 5, "is_active": 1 },
  { "part_name": "Laptop Keyboard Backlit", "part_code": "LP-114", "compatible_device_type": "Laptop", "unit_cost": 1500.00, "selling_price": 2200.00, "stock_qty": 20, "reorder_level": 6, "is_active": 1 },
  { "part_name": "Laptop Touchpad Module", "part_code": "LP-115", "compatible_device_type": "Laptop", "unit_cost": 900.00, "selling_price": 1400.00, "stock_qty": 14, "reorder_level": 5, "is_active": 1 },
  { "part_name": "Laptop Cooling Fan", "part_code": "LP-116", "compatible_device_type": "Laptop", "unit_cost": 700.00, "selling_price": 1100.00, "stock_qty": 22, "reorder_level": 6, "is_active": 1 },
  { "part_name": "Laptop 8GB DDR4 RAM", "part_code": "LP-117", "compatible_device_type": "Laptop", "unit_cost": 2200.00, "selling_price": 3000.00, "stock_qty": 18, "reorder_level": 6, "is_active": 1 },
  { "part_name": "Laptop 512GB SSD", "part_code": "LP-118", "compatible_device_type": "Laptop", "unit_cost": 3200.00, "selling_price": 4200.00, "stock_qty": 12, "reorder_level": 4, "is_active": 1 },
  { "part_name": "Laptop Charger 65W", "part_code": "LP-119", "compatible_device_type": "Laptop", "unit_cost": 1000.00, "selling_price": 1600.00, "stock_qty": 25, "reorder_level": 8, "is_active": 1 },
  { "part_name": "Laptop Motherboard", "part_code": "LP-120", "compatible_device_type": "Laptop", "unit_cost": 6500.00, "selling_price": 8500.00, "stock_qty": 5, "reorder_level": 2, "is_active": 1 },

  { "part_name": "Tablet 10\" Display", "part_code": "TB-121", "compatible_device_type": "Tablet", "unit_cost": 3000.00, "selling_price": 3900.00, "stock_qty": 11, "reorder_level": 4, "is_active": 1 },
  { "part_name": "Tablet 8\" Display", "part_code": "TB-122", "compatible_device_type": "Tablet", "unit_cost": 2500.00, "selling_price": 3300.00, "stock_qty": 13, "reorder_level": 4, "is_active": 1 },
  { "part_name": "Tablet Battery 6000mAh", "part_code": "TB-123", "compatible_device_type": "Tablet", "unit_cost": 1100.00, "selling_price": 1700.00, "stock_qty": 19, "reorder_level": 6, "is_active": 1 },
  { "part_name": "Tablet Charging Port Board", "part_code": "TB-124", "compatible_device_type": "Tablet", "unit_cost": 600.00, "selling_price": 950.00, "stock_qty": 24, "reorder_level": 8, "is_active": 1 },
  { "part_name": "Tablet Rear Camera 13MP", "part_code": "TB-125", "compatible_device_type": "Tablet", "unit_cost": 1400.00, "selling_price": 2000.00, "stock_qty": 9, "reorder_level": 3, "is_active": 1 },
  { "part_name": "Tablet Front Camera 8MP", "part_code": "TB-126", "compatible_device_type": "Tablet", "unit_cost": 1000.00, "selling_price": 1500.00, "stock_qty": 10, "reorder_level": 3, "is_active": 1 },
  { "part_name": "Tablet Speaker Module", "part_code": "TB-127", "compatible_device_type": "Tablet", "unit_cost": 400.00, "selling_price": 700.00, "stock_qty": 28, "reorder_level": 9, "is_active": 1 },
  { "part_name": "Tablet Power Button Flex", "part_code": "TB-128", "compatible_device_type": "Tablet", "unit_cost": 300.00, "selling_price": 600.00, "stock_qty": 26, "reorder_level": 8, "is_active": 1 },
  { "part_name": "Tablet Volume Button Flex", "part_code": "TB-129", "compatible_device_type": "Tablet", "unit_cost": 300.00, "selling_price": 600.00, "stock_qty": 21, "reorder_level": 7, "is_active": 1 },
  { "part_name": "Tablet Motherboard", "part_code": "TB-130", "compatible_device_type": "Tablet", "unit_cost": 4800.00, "selling_price": 6200.00, "stock_qty": 6, "reorder_level": 2, "is_active": 1 }

]

    for part in parts:
        if not frappe.db.exists("Spare Part", {"part_code": part["part_code"]}):
            doc = frappe.get_doc({
            "doctype": "Spare Part",
            **part
            })
            doc.insert()

    frappe.db.commit()

    return "Successfully added"