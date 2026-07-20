# Copyright (c) 2026, Omnexa and contributors
# License: MIT

"""Universal report filter helpers — aligned with omnexa_core session context."""

from __future__ import annotations

import frappe
from frappe import _

from omnexa_core.omnexa_core.branch_access import get_allowed_branches


def normalize_filters(filters=None) -> frappe._dict:
	return frappe._dict(filters or {})


def require_company(filters: frappe._dict) -> None:
	if not filters.get("company"):
		frappe.throw(_("Company filter is required."), title=_("Filters"))


def sql_scope_conditions(filters: frappe._dict, *, table_alias: str = "odr") -> tuple[list[str], frappe._dict]:
	"""Build SQL WHERE fragments for company/branch/date/status scope."""
	require_company(filters)
	conditions = [f"{table_alias}.company = %(company)s"]
	if filters.get("branch"):
		conditions.append(f"{table_alias}.branch = %(branch)s")
	if filters.get("vertical"):
		conditions.append(f"{table_alias}.vertical = %(vertical)s")
	if filters.get("registration_status"):
		conditions.append(f"{table_alias}.registration_status = %(registration_status)s")
	if filters.get("document_category"):
		conditions.append(f"{table_alias}.document_category = %(document_category)s")
	if filters.get("from_date"):
		conditions.append(f"{table_alias}.registration_date >= %(from_date)s")
	if filters.get("to_date"):
		conditions.append(f"{table_alias}.registration_date <= %(to_date)s")

	allowed = get_allowed_branches(company=filters.company)
	if allowed is not None:
		if not allowed:
			conditions.append("1=0")
		else:
			filters.allowed_branches = tuple(allowed)
			conditions.append(f"{table_alias}.branch in %(allowed_branches)s")
	return conditions, filters


def standard_registry_filters() -> list[dict]:
	return [
		{
			"fieldname": "company",
			"fieldtype": "Link",
			"label": "Company",
			"options": "Company",
			"reqd": 1,
			"width": "180px"
	},
		{
			"fieldname": "branch",
			"fieldtype": "Link",
			"label": "Branch",
			"options": "Branch",
			"width": "180px"
	},
		{
			"fieldname": "from_date",
			"fieldtype": "Date",
			"label": "From Date",
			"width": "120px"
	},
		{
			"fieldname": "to_date",
			"fieldtype": "Date",
			"label": "To Date",
			"width": "120px"
	},
		{
			"fieldname": "vertical",
			"fieldtype": "Select",
			"label": "Vertical",
			"options": "\nEngineering\nConstruction\nEducation\nHealthcare\nFinance\nHR\nTourism\nGeneric",
			"width": "140px"
	},
		{
			"fieldname": "registration_status",
			"fieldtype": "Select",
			"label": "Status",
			"options": "\nDraft\nUnder Review\nApproved\nPublished\nArchived\nSuperseded",
			"width": "140px"
	},
		{
			"fieldname": "document_category",
			"fieldtype": "Select",
			"label": "Category",
			"options": "\nDrawing\nSpecification\nContract\nPolicy\nReport\nCertificate\nCorrespondence\nOther",
			"width": "140px"
	},
	]
