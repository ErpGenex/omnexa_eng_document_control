# Copyright (c) 2026, Omnexa and contributors
# License: MIT

from __future__ import annotations

import frappe
from frappe.model.document import Document
from frappe.utils import nowdate, today


class OmnexaDocumentRegister(Document):
	def before_insert(self):
		if not self.registration_date:
			self.registration_date = today()
		if not self.registered_by:
			self.registered_by = frappe.session.user

	def validate(self):
		self._apply_company_branch_defaults()
		self._build_qr_payload()

	def _apply_company_branch_defaults(self):
		from omnexa_core.omnexa_core.branch_access import get_default_branch, get_default_company

		if not self.company:
			self.company = get_default_company()
		if self.company and not self.branch:
			self.branch = get_default_branch(self.company)

	def _build_qr_payload(self):
		self.qr_payload = f"ODR|{self.name or 'NEW'}|{self.document_title or ''}|{self.revision_no or ''}|{nowdate()}"


def permission_query_conditions(user: str | None = None) -> str:
	from omnexa_core.omnexa_core.branch_access import permission_query_conditions_for_branch_field

	return permission_query_conditions_for_branch_field("Omnexa Document Register", user)
