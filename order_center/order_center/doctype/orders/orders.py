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
        if not self.number_of_items:
            err("number of items")
        if not self.delivery_cutoff:
            err("delivery cutoff")
        if not self.quantity_of_items:
            err("quantity of items")
        if not self.total_value:
            err("total value")
        if not self.account_name:
            err("account name")
        if not self.pincode:
            err("pincode")
        if not self.address_line_1:
            err("address line 1")
        if not self.address_line_2:
            err("address line 2")
        if not self.city:
            err("city")
        if not self.country:
            err("country")
        if not self.vehicle_type:
            err("vehicle type")
        if not self.is_partial_delivery_allowed_fl:
            err("is partial delivery allowed fl")
        if not self.service_time_in_mins:
            err("service time in mins")
        if not self.preferred_mode_of_transport:
            err("preferred mode of transport")
        if not self.weight:
            err("weight")
        else:
            try:
                float(self.weight)
            except Exception:
                frappe.throw(_("Weight has to be a number"))

    def on_update(self):
        api = ("http://client.loginextsolutions.com/LogiNextService/"
                "TLMConnector/addNewBillJson")
        d = dict()
        d["billNumber"] = self.awb
        d["timestamp"] = datetime.datetime.fromtimestamp(time.time()).\
                strftime('%Y-%m-%d %H:%M:%S')
        d["accountCode"] = self.account_code
        d["distributionCenter"] = self.distribution_center
        d["phoneNumber"] = self.phone_number
        d["wsAuthenticationKey"] = "bd87d55b-d790-4556-86ec-2e934921dfd9"
        d["wsEmailAddress"] = "apeksha.d@loginextsolutions.com"
        d["deliveryLocationType"] = self.delivery_location_type
        d["paymentType"] = self.payment_type
        
        d["deliveryCutoff"] = self.delivery_cutoff
        d["numberOfItems"] = self.number_of_items
        d["quantityOfItems"] = self.quantity_of_items
        d["totalValue"] = self.total_value
        d["urgency"] = self.urgency
        d["accountName"] = self.account_name
        d["pincode"] = self.pincode
        d["addressline1"] = self.address_line_1
        d["addressline2"] = self.address_line_2
        d["city"] = self.city
        d["country"] = self.country
        d["vehicleType"] = self.vehicle_type
        d["isPartialDeliveryAllowedFl"] = self.is_partial_delivery_allowed_fl
        d["serviceTimeInMins"] = self.service_time_in_mins
        d["preferredModeOfTransport"] = self.preferred_mode_of_transport
        self.genInvoice()
        headers = {"content-type": "application/json"}
        print("*********** LOGINEXT ********************")
        print(json.dumps(d))
        print("*********** LOGINEXT ********************")
        r = requests.post(api, data = json.dumps(d), headers=headers)
        try:
            resp = json.loads(r.text)
            if resp["statusCode"] != "201":
                 frappe.throw(
                         _("Error recived response from loginext server: %s" % 
                            r.text))
        except Exception:
            raise frappe.throw(_("Error parsing json! %s" % r.text))


    def get_default_account(self):
        return frappe.get_list("Account", fields=["name"],
                filters={"account_name":"Debtors"})[0]["name"]


    def get_income_account(self):
        return frappe.get_list("Account", fields=["name"],
            filters={"account_name":"Sales"})[0]["name"]


    def build_item(self, item, price):
        return { 
                "item_name":item,
                "description": "Transporting Item",
                "qty": 1.0,
                "rate":price,
                "income_account":self.get_income_account()
            }

    def get_default_territory(self):
        return frappe.get_list("Territory", fields=["name"], 
                filters={"territory_name":"All Territories"})[0]["name"]


    def get_default_customer_group(self):
        return frappe.get_list("Customer Group", fields=["name"],
                filters={"customer_group_name":"Commercial"})[0].name


    def build_contact_for_customer(self, cust, email):
        contact = frappe.get_doc({"doctype":"Contact",
            "first_name":cust.customer_name,
            "email_id":email,
            "customer":cust.name
        })
        contact.insert()
        frappe.db.commit()


    def build_customer(self, consname, email):
        customer = None
        customer = self.check_if_customer_exists(consname)
        if customer:
            return customer.name
        customer = frappe.get_doc({"doctype":"Customer",
            "customer_name":consname, 
            "customer_type":"Individual",
            "territory": self.get_default_territory(),
            "customer_group":self.get_default_customer_group()
        })
        customer.insert()
        frappe.db.commit()
        self.build_contact_for_customer(customer, email)
        return customer.name

    def check_if_customer_exists(self, consname):
        customer = frappe.get_list("Customer", fields=["*"],
                filters={"customer_name":consname})
        if not customer:
            return None
        return customer[0]

    def genInvoice(self):
        cons = frappe.get_list("Consignor", fields=["*"],
                filters={"name":self.consignor})[0]
        due_date = datetime.datetime.now() + datetime.timedelta(days=42)
        due_date = due_date.strftime("%y-%m-%d")
        d = frappe.get_doc({
            "doctype":"Sales Invoice",
            "naming_series":"SINV-",
            "posting_date":frappe.utils.nowdate(),
            "due_date":due_date,
            "debit_to":self.get_default_account(),
            "items":[self.build_item(self.product_type,
                float(self.weight) * cons["rate"])],
            "customer":self.build_customer(cons["name1"], cons["email"])
            })
        d.insert()
        frappe.db.commit()


