# Copyright (c) 2026, Omnexa and contributors
# License: MIT

"""Sync vertical document registers into Omnexa Document Register (non-destructive)."""

from __future__ import annotations

import frappe
from frappe.utils import add_years, getdate, today

STATUS_MAP_ENGINEERING = {
	"WIP": "Draft",
	"Shared": "Under Review",
	"Published": "Published",
	"Archived": "Archived"
	}

STATUS_MAP_CONSTRUCTION = {
	"Draft": "Draft",
	"Under Review": "Under Review",
	"Approved": "Approved",
	"Rejected": "Draft",
	"Superseded": "Superseded"
	}


def _settings():
	if not frappe.db.exists("DocType", "Omnexa Document Control Settings"):
		return frappe._dict()
	return frappe.get_single("Omnexa Document Control Settings")


def sync_all_vertical_registers() -> dict:
	settings = _settings()
	if settings and not settings.get("enable_vertical_sync"):
		return {"skipped": True, "reason": "sync disabled"
	}

	stats = {"created": 0, "updated": 0, "sources": []
	}
	if not settings or settings.get("sync_engineering_register"):
		stats["sources"].append(_sync_engineering_register(stats))
	if not settings or settings.get("sync_construction_cde"):
		stats["sources"].append(_sync_construction_cde(stats))
	frappe.db.commit()
	return stats


def _upsert_from_source(payload: dict, stats: dict) -> str:
	existing = frappe.db.get_value(
		"Omnexa Document Register",
		{"source_doctype": payload["source_doctype"], "source_document": payload["source_document"]
	},
		"name",
	)
	if existing:
		doc = frappe.get_doc("Omnexa Document Register", existing)
		doc.update({k: v for k, v in payload.items() if k not in ("name",)})
		doc.flags.ignore_permissions = True
		doc.save()
		stats["updated"] += 1
		return doc.name

	doc = frappe.get_doc({"doctype": "Omnexa Document Register", **payload})
	doc.flags.ignore_permissions = True
	doc.insert()
	stats["created"] += 1
	return doc.name


def _retention_until(years: int | None = None) -> str:
	years = int(years or 7)
	return add_years(today(), years)


def _sync_engineering_register(stats: dict) -> dict:
	if not frappe.db.exists("DocType", "Engineering Document Register"):
		return {"vertical": "Engineering", "count": 0, "skipped": "doctype missing"
	}

	retention_years = frappe.db.get_single_value("Omnexa Document Control Settings", "default_retention_years") or 7
	rows = frappe.get_all(
		"Engineering Document Register",
		fields=[
			"name",
			"document_title",
			"document_type",
			"revision_no",
			"file_url",
			"publishing_state",
			"approval_status",
			"company",
			"branch",
			"modified",
		],
		limit=5000,
	)
	for row in rows:
		status = STATUS_MAP_ENGINEERING.get(row.publishing_state or "", row.approval_status or "Draft")
		if row.approval_status == "Approved" and status != "Published":
			status = "Approved"
		_upsert_from_source(
			{
				"document_title": row.document_title,
				"document_number": row.name,
				"vertical": "Engineering",
				"document_category": _map_category(row.document_type),
				"registration_status": status or "Draft",
				"revision_no": row.revision_no or "R0",
				"file_attachment": row.file_url,
				"company": row.company,
				"branch": row.branch,
				"registration_date": getdate(row.modified).isoformat() if row.modified else today(),
				"retention_until": _retention_until(retention_years),
				"source_doctype": "Engineering Document Register",
				"source_document": row.name,
				"source_app": "omnexa_engineering_consulting",
				"confidentiality": "Internal"
	},
			stats,
		)
	return {"vertical": "Engineering", "count": len(rows)
	}


def _sync_construction_cde(stats: dict) -> dict:
	if not frappe.db.exists("DocType", "Construction CDE Document"):
		return {"vertical": "Construction", "count": 0, "skipped": "doctype missing"
	}

	retention_years = frappe.db.get_single_value("Omnexa Document Control Settings", "default_retention_years") or 7
	rows = frappe.get_all(
		"Construction CDE Document",
		fields=[
			"name",
			"document_number",
			"document_title",
			"revision",
			"file_attachment",
			"approval_status",
			"cde_status",
			"company",
			"branch",
			"issued_date",
		],
		limit=5000,
	)
	for row in rows:
		status = STATUS_MAP_CONSTRUCTION.get(row.approval_status or "Draft", "Draft")
		if row.cde_status == "Published":
			status = "Published"
		if row.cde_status == "Archived":
			status = "Archived"
		_upsert_from_source(
			{
				"document_title": row.document_title,
				"document_number": row.document_number or row.name,
				"vertical": "Construction",
				"document_category": "Drawing",
				"registration_status": status,
				"revision_no": row.revision or "A",
				"file_attachment": row.file_attachment,
				"company": row.company,
				"branch": row.branch,
				"registration_date": row.issued_date or today(),
				"retention_until": _retention_until(retention_years),
				"source_doctype": "Construction CDE Document",
				"source_document": row.name,
				"source_app": "omnexa_construction",
				"confidentiality": "Internal"
	},
			stats,
		)
	return {"vertical": "Construction", "count": len(rows)
	}


def _map_category(document_type: str | None) -> str:
	mapping = {
		"Drawing": "Drawing",
		"Specification": "Specification",
		"Calculation": "Report",
		"Method Statement": "Report"
	}
	return mapping.get(document_type or "", "Other")


@frappe.whitelist()
def sync_registry_now() -> dict:
	frappe.only_for(("System Manager", "Company Admin", "Omnexa Document Controller"))
	return sync_all_vertical_registers()
