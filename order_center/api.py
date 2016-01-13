import frappe
import os
import json

@frappe.whitelist(allow_guest=True)
def get_info_from_loginext():
    # frappe.local.request 
    #order = frappe.get_doc({
    #		"doctype": "Order",
    #		"customer": 
    #	})
    #order.insert()
    return "coreanimal says: %s" % frappe.local.request

@frappe.whitelist(allow_guest=True)
def clear_all_cache():
     frappe.clear_cache()
     return "cache cleard"

@frappe.whitelist(allow_guest=True)
def dispatch_start_trip():
    open(os.path.expanduser("~/erp_data/dispatch_start.json"), "a").write(
            frappe.local.request.data + "\n")

@frappe.whitelist(allow_guest=True)
def load_items():
    open(os.path.expanduser("~/erp_data/load_items.json"), "a").write(
            frappe.local.request.data + "\n")

@frappe.whitelist(allow_guest=True)
def pickup():
    open(os.path.expanduser("~/erp_data/pickup.json"), "a").write(
            frappe.local.request.data + "\n")

@frappe.whitelist(allow_guest=True)
def delivery_notification():
    open(os.path.expanduser("~/erp_data/delivery_notification.json"), "a").write(
            frappe.local.request.data + "\n")

@frappe.whitelist(allow_guest=True)
def not_deliverd_notification():
    open(os.path.expanduser("~/erp_data/not_deliverd_notification.json"), "a").write(
            frappe.local.request.data + "\n")

@frappe.whitelist(allow_guest=True)
def partial_delivery_notification():
    open(os.path.expanduser("~/erp_data/partial_delivery_notification.json"), 
            "a").write(frappe.local.request.data + "\n")

@frappe.whitelist(allow_guest=True)
def arrival_end_trip():
    open(os.path.expanduser("~/erp_data/arrival_end_trip.json"), 
            "a").write(frappe.local.request.data + "\n")

@frappe.whitelist(allow_guest=True)
def accept():
    open(os.path.expanduser("~/erp_data/accept.json"), 
            "a").write(frappe.local.request.data + "\n")


@frappe.whitelist(allow_guest=True)
def reject():
    open(os.path.expanduser("~/erp_data/reject.json"), 
            "a").write(frappe.local.request.data + "\n")

@frappe.whitelist(allow_guest=True)
def clustering_updates():
    open(os.path.expanduser("~/erp_data/clustering_updates.json"), 
            "a").write(frappe.local.request.data + "\n")

@frappe.whitelist(allow_guest=True)
def clustering_and_scheduling():
    open(os.path.expanduser("~/erp_data/clustering_and_scheduling.json"), 
            "a").write(frappe.local.request.data + "\n")
