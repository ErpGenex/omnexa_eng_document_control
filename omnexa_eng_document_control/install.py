# Copyright (c) 2026, Omnexa and contributors
# License: MIT

import frappe


def after_install():
	_bootstrap()


def after_migrate():
	_bootstrap()


def _bootstrap():
	_ensure_document_controller_role()
	try:
		from omnexa_eng_document_control.workspace.document_control_workspace import sync_document_control_workspace

		sync_document_control_workspace()
	except Exception:
		frappe.log_error(frappe.get_traceback(), "EDC: workspace sync failed")
	try:
		from omnexa_eng_document_control.document_registry.sync import sync_all_vertical_registers

		sync_all_vertical_registers()
	except Exception:
		frappe.log_error(frappe.get_traceback(), "EDC: registry sync failed")


def _ensure_document_controller_role():
	if frappe.db.exists("Role", "Omnexa Document Controller"):
		frappe.db.set_value("Role", "Omnexa Document Controller", "desk_access", 1, update_modified=False)
		return
	frappe.get_doc(
		{
			"doctype": "Role",
			"role_name": "Omnexa Document Controller",
			"desk_access": 1,
		}
	).insert(ignore_permissions=True)
