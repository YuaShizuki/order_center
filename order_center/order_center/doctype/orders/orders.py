# -*- coding: utf-8 -*-
# Copyright (c) 2015, keshav bhide and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
import time
import datetime
import requests
import json


class Orders(Document):
    def validate(self):
        err = lambda x: frappe.throw(_("require %s to save order." % x))
        if not self.awb:
            frappe.throw(_("require AWB to save order."))
        if not self.consignor:
            frappe.throw(_("require AWB to save order."))
        if not self.account_code:
            frappe.throw(_("require account code to save order."))
        if not self.consignee:
            frappe.throw(_("require consignee to save order."))
        if not self.phone_number:
            frappe.throw(_("require phone number to save order."))
        if not self.product_type:
            err("product type")
        if not self.product_description:
            err("product_description")
        if not self.delivery_location_type:
            err("delivery location type")
        if not self.order_type:
            err("order type.")
        if not self.payment_type:
            err("payment type")
        if not self.distribution_center:
            err("distribution center")

    def on_update(self):
        d = dict()
        d["billNumber"] = self.awb
        d["timestamp"] = datetime.datetime.fromtimestamp(time.time()).\
                strftime('%Y-%m-%d %H:%M:%S')
        d["accountCode"] = self.account_code
        d["distributionCenter"] = self.distribution_center
        d["phoneNumber"] = self.phone_number
        d["wsAuthenticationKey"] = "bd87d55b-d790-4556-86ec-2e934921dfd9"
        d["wsEmailAddress"] = "apeksha.d@loginextsolutions.com"
        print(("*" * 80) + "Making requests")
        headers = {"content-type": "application/json"}
        r = requests.post(
            "http://client.loginextsolutions.com/LogiNextService/TLMConnector/addNewBillJson",
            data = json.dumps(d), headers=headers)
        print(("*" * 80) + "Response") 
        print(r.text)
        print("*" * 80)


