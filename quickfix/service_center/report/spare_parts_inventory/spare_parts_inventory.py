# Copyright (c) 2026, Praveenkumar-Dhanasekar and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):

	cols = get_cols()
	data = get_data(filters)

	return cols,data,None,None,get_report_summary()


def get_cols():
	return[
		{
			"fieldname":"part_name",
			"label":"Parts Name",
			"fieldtype":"Data",
			"width":200
		},
		{
			"fieldname":"part_code",
			"label":"Parts Code",
			"fieldtype":"Data",
			"width":200
		},
		{
			"fieldname":"compatible_device_type",
			"label":"Device Type",
			"fieldtype":"Link",
			"options":"Device Type",
			"width":200
		},
		{
			"fieldname":"stock_qty",
			"label":"Stock Quantity",
			"fieldtype":"Int",
			"width":200
		},
		{
			"fieldname":"reorder_level",
			"label":"Reorder Level",
			"fieldtype":"Int",
			"width":200
		},
		{
			"fieldname":"unit_cost",
			"label":"Unit Cost",
			"fieldtype":"Currency",
			"width":200,
			"precision": 2
		},
		{
			"fieldname":"selling_price",
			"label":"Selling Price",
			"fieldtype":"Currency",
			"width":200,
			"precision": 2
		},
		{
			"fieldname":"margin",
			"label":"Margin",
			"fieldtype":"Percentage",
			"width":200,
			"precision": 2
		}
	]


def get_data(filters):

	device_filters = {}

	if filters and filters.get("item"):
		device_filters["name"] = filters.get("item")

	frappe.log_error("q1111",device_filters)
	parts = frappe.get_list(
		"Spare Part",
		filters=device_filters,
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
	total_unit_cost = 0
	total_sell_cost = 0
	total_qty = 0
	total_margin = 0

	for row in parts:
		unit_cost = row.get("unit_cost") or 0
		selling_price = row.get("selling_price") or 0
		total_qty+= row.get("stock_qty") or 0
		total_sell_cost += (row.get("stock_qty") * selling_price)
		total_unit_cost += (row.get("stock_qty") * unit_cost)
		

		margin = 0
		if unit_cost:
			margin = ((selling_price - unit_cost) / unit_cost) * 100
			total_margin += margin
			frappe.log_error("11111",total_margin)

		row["margin"] = round(margin, 2)

		data.append(row)
	if not len(parts) == 1:
		total_margin = total_margin / 100

	data.append({
    "part_name": "Total",
    "stock_qty": total_qty,
    "unit_cost": total_unit_cost,
    "selling_price": total_sell_cost,
    "margin": total_margin
	})

	return data

def get_report_summary():
	data = frappe.get_list("Spare Part",fields=[
			"part_name",
			"part_code",
			"compatible_device_type",
			"unit_cost",
			"selling_price",
			"stock_qty",
			"reorder_level"
		])

	total_parts = len(data)
	below_recorder = 0
	total_inventory_value = 0
	for row in data:
		if row.stock_qty <= row.reorder_level:
			below_recorder +=1
		total_inventory_value += (row.stock_qty * row.unit_cost)

	return [
		{
			"label":"Total Parts",
			"value":total_parts,
			"indicator" : "Blue"
		},
		{
			"label":"Below Reorder",
			"value":below_recorder,
			"indicator":"Green"
		},
		{
			"label":"Total Inventory Value",
			"value":total_inventory_value,
			"datatype":"Currency",
			"indicator":"Gray"
		}
	]




