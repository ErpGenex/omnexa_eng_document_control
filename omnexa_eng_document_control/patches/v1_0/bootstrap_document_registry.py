# Copyright (c) 2026, Omnexa and contributors
# License: MIT


def execute():
	from omnexa_eng_document_control.document_registry.sync import sync_all_vertical_registers
	from omnexa_eng_document_control.workspace.document_control_workspace import sync_document_control_workspace

	sync_document_control_workspace()
	return sync_all_vertical_registers()
