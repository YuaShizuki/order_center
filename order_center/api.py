import frappe
import os
import json
import datetime
import uuid

@frappe.whitelist(allow_guest=True)
def clustering_and_scheduling():
    for trip in json.loads(frappe.local.request.values["inputData"]):
        build_trip(trip)

def build_trip(dat):
    d = frappe.get_doc({
        "doctype":"DRS",
        "trip_name":dat["tripName"],
        "status":"Clustering And Scheduling",
        "driver_name":dat["driverName"],
        "vehicle":dat["vehicle"],
        "shipment_details":parse_shipment_details(dat["shipmentDetails"])
    })
    d.insert()
    frappe.db.commit()

def parse_shipment_details(shdetails):
    result = []
    for shipment in shdetails:
        d = dict()
        d["latitude"] = shipment["latitude"]
        d["longitude"] = shipment["longitude"]
        d["awb"] = shipment["clientShipmentId"]
        d["delivery_order"] = shipment["deliveryOrder"]
        d["Status"] = "Unknown"
        result.append(d)
    return result

@frappe.whitelist(allow_guest=True)
def dispatch_start_trip():
    start_trip(json.loads(frappe.local.request.values["inputData"]))

def start_trip(trip):
    t = frappe.get_list("DRS", fields=["*"],
            filters={"trip_name":trip["tripName"]})[0]
    tx = frappe.get_doc("DRS", t["name"])
    tx.status = "Start Trip"
    tx.save()

@frappe.whitelist(allow_guest=True)
def load_items():
    val = frappe.local.request.values["inputData"]
    awb = json.loads(val)["clientShipmentId"]
    t = frappe.get_list("Shipment Details", fields=["*"],
                filters={"awb":awb})[0]
    tx = frappe.get_doc("Shipment Details", t["name"])
    tx.status = "Loaded"
    tx.save()

@frappe.whitelist(allow_guest=True)
def pickup():
    val = frappe.local.request.values["inputData"]
    awb = json.loads(val)["clientShipmentId"]
    t = frappe.get_list("Shipment Details", fields=["*"],
                filters={"awb":awb})[0]
    tx = frappe.get_doc("Shipment Details", t["name"])
    tx.status = "Picked Up"
    tx.save()

@frappe.whitelist(allow_guest=True)
def delivery_notification():
    for parcel in json.loads(frappe.local.request.values["inputData"]):
        set_deliverd(parcel, "Delivered")

def set_deliverd(parcel, status):
    awb = parcel["clientShipmentId"]
    t = frappe.get_list("Shipment Details", fields=["*"],
                filters={"awb":awb})[0]
    tx = frappe.get_doc("Shipment Details", t["name"])
    tx.status = status
    tx.latitude = parcel["latitude"]
    tx.longitude = parcel["longitude"]
    tx.save()

@frappe.whitelist(allow_guest=True)
def not_deliverd_notification():
    for parcel in json.loads(frappe.local.request.values["inputData"]):
        set_deliverd(parcel, "Not Delivered")

@frappe.whitelist(allow_guest=True)
def partial_delivery_notification():
    for parcel in json.loads(frappe.local.request.values["inputData"]):
        set_deliverd(parcel, "Partial Delivery")

#---------------------------------------------THROW-----------------------------
@frappe.whitelist(allow_guest=True)
def clear_all_cache():
     frappe.clear_cache()
     return "cache cleard"

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

#CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([('inputData', u'[{"tripName":"TRIP-32","deliveryMediumName":"MEHUL","driverName":"","vehicle":"","shipmentDetails":[{"latitude":19.199272,"longitude":72.857732,"clientShipmentId":"222222201","deliveryOrder":4},{"latitude":19.199272,"longitude":72.857732,"clientShipmentId":"112000003","deliveryOrder":5},{"latitude":19.1076375,"longitude":72.8655789,"clientShipmentId":"test_order","deliveryOrder":6}]}]')])])
