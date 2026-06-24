# Copyright (c) 2026, Omnexa and contributors
# License: MIT

import frappe
from frappe.tests import IntegrationTestCase


class TestDocumentRegistry(IntegrationTestCase):
	def test_doctype_exists(self):
		self.assertTrue(frappe.db.exists("DocType", "Omnexa Document Register"))

	def test_report_module_paths(self):
		from frappe.core.doctype.report.report import get_report_module_dotted_path

		for report in ("Omnexa Document Registry Index", "Omnexa Document Compliance Summary"):
			path = get_report_module_dotted_path("Omnexa Eng Document Control", report)
			self.assertTrue(frappe.get_attr(path + ".execute"))

	def test_registry_insert(self):
		company = frappe.db.get_value("Company", {}, "name")
		if not company:
			self.skipTest("no company")
		branch = frappe.db.get_value("Branch", {"company": company}, "name")
		if not branch:
			self.skipTest("no branch")
		doc = frappe.get_doc(
			{
				"doctype": "Omnexa Document Register",
				"document_title": "Integration Test Doc",
				"vertical": "Generic",
				"registration_status": "Draft",
				"company": company,
				"branch": branch,
			}
		)
		doc.flags.ignore_permissions = True
		doc.insert()
		self.assertTrue(doc.qr_payload)
		doc.delete()
