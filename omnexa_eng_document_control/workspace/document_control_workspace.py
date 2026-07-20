# Copyright (c) 2026, Omnexa and contributors
# License: MIT

"""Document Control workspace — global registry hub."""

from __future__ import annotations

import frappe


def sync_document_control_workspace(*, save: bool = True) -> dict:
	if not frappe.db.exists("Workspace", "Document Control"):
		return {"skipped": True
	}
	ws = frappe.get_doc("Workspace", "Document Control")
	links = [
		{"type": "Card Break", "label": "📁 Registry", "link_type": "DocType"
	},
		{"type": "Link", "label": "Document Register", "link_type": "DocType", "link_to": "Omnexa Document Register"
	},
		{"type": "Link", "label": "Settings", "link_type": "DocType", "link_to": "Omnexa Document Control Settings"
	},
		{"type": "Card Break", "label": "📊 Reports", "link_type": "DocType"
	},
		{
			"type": "Link",
			"label": "Registry Index",
			"link_type": "Report",
			"link_to": "Omnexa Document Registry Index",
			"is_query_report": 1
	},
		{
			"type": "Link",
			"label": "Compliance Summary",
			"link_type": "Report",
			"link_to": "Omnexa Document Compliance Summary",
			"is_query_report": 1
	},
		{"type": "Card Break", "label": "🔗 Vertical Sources", "link_type": "DocType"
	},
	]
	if frappe.db.exists("DocType", "Engineering Document Register"):
		links.append(
			{
				"type": "Link",
				"label": "Engineering Register",
				"link_type": "DocType",
				"link_to": "Engineering Document Register"
	}
		)
	if frappe.db.exists("DocType", "Construction CDE Document"):
		links.append(
			{
				"type": "Link",
				"label": "Construction CDE",
				"link_type": "DocType",
				"link_to": "Construction CDE Document"
	}
		)
	ws.set("links", [])
	for row in links:
		ws.append("links", row)
	ws.set(
		"shortcuts",
		[
			{"label": "Document Register", "link_to": "Omnexa Document Register", "type": "DocType", "doc_view": "List", "color": "Blue"
	},
			{"label": "Registry Index", "link_to": "Omnexa Document Registry Index", "type": "Report", "color": "Green"
	},
			{"label": "Compliance Summary", "link_to": "Omnexa Document Compliance Summary", "type": "Report", "color": "Orange"
	},
		],
	)
	if save:
		ws.flags.ignore_permissions = True
		ws.save()
		frappe.clear_cache(doctype="Workspace")
	return {"links": len(links), "shortcuts": 3
	}
