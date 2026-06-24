# Copyright (c) 2026, Omnexa and contributors
# License: MIT

import frappe
from frappe import _

from omnexa_core.omnexa_core.utils.report_charts import auto_chart_for_columns

from omnexa_eng_document_control.document_registry.report_filters import normalize_filters, sql_scope_conditions


def execute(filters=None):
	filters = normalize_filters(filters)
	conditions, filters = sql_scope_conditions(filters, table_alias="odr")
	rows = frappe.db.sql(
		f"""
		SELECT
			odr.registration_status,
			odr.vertical,
			odr.confidentiality,
			COUNT(*) AS doc_count
		FROM `tabOmnexa Document Register` odr
		WHERE {' AND '.join(conditions)}
		GROUP BY odr.registration_status, odr.vertical, odr.confidentiality
		ORDER BY odr.vertical, odr.registration_status
		""",
		filters,
		as_dict=True,
	)
	return _columns(), rows, None, _summary_chart(rows)


def _columns():
	return [
		{"label": _("Vertical"), "fieldname": "vertical", "fieldtype": "Data", "width": 120},
		{"label": _("Status"), "fieldname": "registration_status", "fieldtype": "Data", "width": 130},
		{"label": _("Confidentiality"), "fieldname": "confidentiality", "fieldtype": "Data", "width": 120},
		{"label": _("Documents"), "fieldname": "doc_count", "fieldtype": "Int", "width": 100},
	]


def _summary_chart(rows: list[dict]) -> dict:
	labels = []
	values = []
	for row in rows:
		labels.append(f"{row.vertical} · {row.registration_status}")
		values.append(row.doc_count)
	return {
		"data": {"labels": labels, "datasets": [{"name": _("Documents"), "values": values}]},
		"type": "bar",
		"title": _("Compliance Matrix"),
		"height": 280,
	}
