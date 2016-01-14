import frappe
import os
import json
import datetime
import uuid

@frappe.whitelist(allow_guest=True)
def test():
    return frappe.get_list("Customer", fields=["*"],
            filters={"customer_name":"Adius Xroe"})


@frappe.whitelist(allow_guest=True)
def get_default_account():
    return frappe.get_list("Account", fields=["name"],
            filters={"account_name":"Debtors"})[0]["name"]


@frappe.whitelist(allow_guest=True)
def build_item_code():
    warehouse = frappe.get_list("Warehouse", fields=["name"],
            filters={"warehouse_name":"Work In Progress"})[0]["name"]
    itemgroup = frappe.get_list("Item Group", fields=["name"],
            filters={"item_group_name":"All Item Groups"})[0]["name"]
    item = frappe.get_doc({
            "doctype": "Item",
            "item_code": str(uuid.uuid4()),
            "item_name": "Transportation",
            "item_group": itemgroup,
            "description": "Trasportation",
            "default_warehouse": warehouse
            })
    item.insert()
    frappe.db.commit()
    return item.name

@frappe.whitelist(allow_guest=True)
def get_income_account():
    return frappe.get_list("Account", fields=["name"],
            filters={"account_name":"Sales"})[0]["name"]

@frappe.whitelist(allow_guest=True)
def build_item(item, price):
    return { 
            "item_name":item,
            "description": "Transporting Item",
            "qty": 1.0,
            "rate":price,
            "income_account":get_income_account()
        }

@frappe.whitelist(allow_guest=True)
def build_item_ajax():
    return build_item("Penis", 300)


def get_default_territory():
    return frappe.get_list("Territory", fields=["name"],
            filters={"territory_name":"All Territories"})[0]["name"]


def get_default_customer_group():
    return frappe.get_list("Customer Group", fields=["name"],
            filters={"customer_group_name":"Commercial"})[0].name



def build_contact_for_customer(cust):
    contact = frappe.get_doc({"doctype":"Contact",
        "first_name":"Adius",
        "email_id":"adium@uw.edu",
        "customer":cust
    })
    contact.insert()
    frappe.db.commit()

def build_throw_away_customer():
    customer = frappe.get_doc({"doctype":"Customer",
        "customer_name":"Adius Xroe", 
        "customer_type":"Individual",
        "territory": get_default_territory(),
        "customer_group":get_default_customer_group()
        })
    customer.insert()
    frappe.db.commit()
    build_contact_for_customer(customer.name)
    return customer.name

@frappe.whitelist(allow_guest=True)
def create_sample_invoice():
    #consignor = frappe.get_list("Consignor", fields=["name1"])[0]
    due_date = datetime.datetime.now() + datetime.timedelta(days=42)
    due_date = due_date.strftime("%y-%m-%d")
    d = frappe.get_doc({
        "doctype":"Sales Invoice",
        "naming_series":"SINV-",
        "posting_date":frappe.utils.nowdate(),
        "due_date":due_date,
        "debit_to":get_default_account(),
        "items":[build_item("trasport oranges", 300.0)],
        "customer":build_throw_away_customer()
        })
    d.insert()
    frappe.db.commit()
    return d.name
    
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
    print("**" * 10)
    print(frappe.local.request.args["inputData"])
    print("**" * 10)
    open(os.path.expanduser("~/erp_data/clustering_and_scheduling.json"), 
            "a").write(frappe.local.request.data + "\n")
