# Copyright (c) 2026, Praveenkumar-Dhanasekar
# For license information, please see license.txt

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    summary = get_report_summary(data)

    return columns, data, None, None, summary
# columns, data, message, chart, report_summary
# None means nothing to display.
# So your code means:
# None → no message
# None → no chart

def get_columns():
    return [
        {
            "fieldname": "part_name",
            "label": "Parts Name",
            "fieldtype": "Data",
            "width": 200
        },
        {
            "fieldname": "part_code",
            "label": "Parts Code",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "fieldname": "compatible_device_type",
            "label": "Device Type",
            "fieldtype": "Link",
            "options": "Device Type",
            "width": 150
        },
        {
            "fieldname": "stock_qty",
            "label": "Stock Quantity",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "reorder_level",
            "label": "Reorder Level",
            "fieldtype": "Int",
            "width": 120
        },
        {
            "fieldname": "unit_cost",
            "label": "Unit Cost",
            "fieldtype": "Currency",
            "precision": 2,
            "width": 120
        },
        {
            "fieldname": "selling_price",
            "label": "Selling Price",
            "fieldtype": "Currency",
            "precision": 2,
            "width": 120
        },
        {
            "fieldname": "margin",
            "label": "Margin (%)",
            "fieldtype": "Percent",
            "precision": 2,
            "width": 120
        }
    ]


def get_data(filters):

    filters_dict = {}

    if filters and filters.get("item"):
        filters_dict["name"] = filters.get("item")

    parts = frappe.get_list(
        "Spare Part",
        filters=filters_dict,
        fields=[
            "part_name",
            "part_code",
            "compatible_device_type",
            "unit_cost",
            "selling_price",
            "stock_qty",
            "reorder_level"
        ]
    )

    data = []

    total_qty = 0
    total_unit_value = 0
    total_sell_value = 0
    total_margin = 0

    for row in parts:

        unit_cost = row.get("unit_cost") or 0
        selling_price = row.get("selling_price") or 0
        stock_qty = row.get("stock_qty") or 0

        # margin calculation
        margin = 0
        if unit_cost:
            margin = ((selling_price - unit_cost) / unit_cost) * 100

        row["margin"] = round(margin, 2)

        # accumulate totals
        total_qty += stock_qty
        total_unit_value += stock_qty * unit_cost
        total_sell_value += stock_qty * selling_price
        total_margin += margin

        data.append(row)

    # average margin
    avg_margin = 0
    if parts:
        avg_margin = total_margin / len(parts)

    # total row
    data.append({
        "part_name": "Total",
        "stock_qty": total_qty,
        "reorder_level": 0,
        "unit_cost": round(total_unit_value, 2),
        "selling_price": round(total_sell_value, 2),
        "margin": round(avg_margin, 2)
    })

    return data


def get_report_summary(data):

    total_parts = len(data) - 1  
    below_reorder = 0
    total_inventory_value = 0

    for row in data:

        if row.get("part_name") == "Total":
            continue

        stock = row.get("stock_qty") or 0
        reorder = row.get("reorder_level") or 0
        unit_cost = row.get("unit_cost") or 0

        if stock <= reorder:
            below_reorder += 1

        total_inventory_value += stock * unit_cost

    return [
        {
            "label": "Total Parts",
            "value": total_parts,
            "indicator": "Blue"
        },
        {
            "label": "Below Reorder",
            "value": below_reorder,
            "indicator": "Red"
        },
        {
            "label": "Total Inventory Value",
            "value": round(total_inventory_value, 2),
            "datatype": "Currency",
            "indicator": "Green"
        }
    ]