"""Orchestra Settings — singleton doctype for Concerto configuration."""

import frappe
from frappe.model.document import Document


class OrchestraSettings(Document):
	def validate(self):
		if self.orchestra_url:
			self.orchestra_url = self.orchestra_url.rstrip("/")
		if self.enabled and not self.orchestra_url:
			frappe.throw("Orchestra URL is required when Concerto is enabled")
