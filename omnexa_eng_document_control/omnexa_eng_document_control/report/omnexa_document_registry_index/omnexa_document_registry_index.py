# Copyright (c) 2026, Omnexa and contributors
# License: MIT

import frappe
from frappe import _

from omnexa_core.omnexa_core.utils.report_charts import auto_chart_for_columns

from omnexa_eng_document_control.document_registry.report_filters import normalize_filters, sql_scope_conditions


def execute(filters=None):
	filters = normalize_filters(filters)
	conditions, filters = sql_scope_conditions(filters, table_alias="odr")
	data = frappe.db.sql(
		f"""
		SELECT
			odr.name,
			odr.document_title,
			odr.document_number,
			odr.vertical,
			odr.document_category,
			odr.registration_status,
			odr.revision_no,
			odr.company,
			odr.branch,
			odr.registration_date,
			odr.source_doctype,
			odr.source_document,
			odr.source_app,
			odr.confidentiality
		FROM `tabOmnexa Document Register` odr
		WHERE {' AND '.join(conditions)}
		ORDER BY odr.registration_date DESC, odr.modified DESC
		LIMIT 1000
		""",
		filters,
		as_dict=True,
	)
	return _columns(), data, None, _chart(data)


def _columns():
	return [
		{"label": _("Register ID"), "fieldname": "name", "fieldtype": "Link", "options": "Omnexa Document Register", "width": 130},
		{"label": _("Title"), "fieldname": "document_title", "fieldtype": "Data", "width": 220},
		{"label": _("Number"), "fieldname": "document_number", "fieldtype": "Data", "width": 140},
		{"label": _("Vertical"), "fieldname": "vertical", "fieldtype": "Data", "width": 110},
		{"label": _("Category"), "fieldname": "document_category", "fieldtype": "Data", "width": 110},
		{"label": _("Status"), "fieldname": "registration_status", "fieldtype": "Data", "width": 110},
		{"label": _("Revision"), "fieldname": "revision_no", "fieldtype": "Data", "width": 80},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 110},
		{"label": _("Registered"), "fieldname": "registration_date", "fieldtype": "Date", "width": 100},
		{"label": _("Source"), "fieldname": "source_doctype", "fieldtype": "Data", "width": 160},
	]


def _chart(data: list[dict]) -> dict:
	by_status: dict[str, int] = {}
	by_vertical: dict[str, int] = {}
	for row in data:
		by_status[row.registration_status] = by_status.get(row.registration_status, 0) + 1
		by_vertical[row.vertical] = by_vertical.get(row.vertical, 0) + 1
	return {
		"data": {
			"labels": list(by_status.keys()),
			"datasets": [{"name": _("By Status"), "values": list(by_status.values())}],
		},
		"type": "donut",
		"title": _("Registry by Status"),
		"height": 240,
		"fieldtype": "Currency",
		"custom_options": json_donut_footer(by_vertical),
	}


def json_donut_footer(by_vertical: dict[str, int]) -> dict:
	parts = [f"{k}: {v}" for k, v in sorted(by_vertical.items())]
	return {"subtitle": " | ".join(parts) if parts else ""}
