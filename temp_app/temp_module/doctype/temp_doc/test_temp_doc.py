# Copyright (c) 2023, human and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestTemp_Doc(FrappeTestCase):
	pass


@frappe.whitelist(allow_guest=1)
def new_module():
	print("hello world")
	return "manly"


@frappe.whitelist(allow_guest=1)
def get_logged_user():
	return frappe.session.user


