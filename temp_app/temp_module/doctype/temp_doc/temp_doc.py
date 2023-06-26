# Copyright (c) 2023, human and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Temp_Doc(Document):
	pass


@frappe.whitelist(allow_guest=1)
def new_module():
	print("$"*1000)
	all =frappe.get_all("Item");
	
	data =frappe.get_all("Item",filters={'name':all[3]['name']},fields=["*"]);
	return data;



@frappe.whitelist(allow_guest=1)
def get_all_items():
	items=frappe.get_all("Item")
	total_items=len(items)
	data=[]
	for i in range(total_items):
		cat=frappe.get_all("Item",filters={'name':items[i]['name']},fields=["item_name"]);
		data.append(cat);
	return data

@frappe.whitelist(allow_guest=1,methods=['GET'])
def get_wishlist_items():
	# return frappe.session.user;
	# if not frappe.db.exists("Wishlist", frappe.session.user):
	# 	return "User Not Avaliable ..."
	# alldata=frappe.db.get_values("Wishlist",filters={"name":"Administrator"});
	# alldata=frappe.db.get_list("Wishlist Item", filters={"parent": "Administrator",
    #             "parentfield": "items",
    #             "parenttype": "Wishlist"} ,fieldname="item_code",order_by="creation")
	alldata=frappe.db.get_list("Wishlist Item", filters={"parent": "Administrator",
                "parentfield": "items",
                "parenttype": "Wishlist"} ,fields=["item_code"])

	

	print(type(alldata))
	# alldata=frappe.db.get_list("Wishlist",filters={"name":"Administrator"})
	print(alldata)
	# alldata=frappe.get_doc("Wishlist","Administrator");
	# if(len(alldata)==0):
	# 	return "No items are  added in list ... ";
	# user_name=[]
	# for i in range(len(alldata)):
	# 	user_name.append(list(alldata[i]))
	
	# print(user_name)
	# all_item=sum(user_name, [])
	# print(all_item)
	data=[]
	for i in range(len(alldata)):
		data.append(alldata[i]['item_code'])

	print(data)
	sumo=[]
	for items in data:
		print(items)
		val,demo=frappe.db.get_value("Item Price",filters={'item_code':items},fieldname=['price_list_rate','item_name'])
		doc=frappe.db.get_value("Item",filters={'name':items},fieldname=['item_name','item_code','item_group','image','country_of_origin','naming_series','owner'],as_dict=1);

		doc['item_rate']=val
		doc['add_checking_purpose']=demo
		sumo.append(doc);
		# sumo.append(val);

	# price=frappe.get_all("Item Price");
	# for j in range(len(price)):
	# 	jack=frappe.get_all("Item Price",filters={'name': price[j]['name']},fields=["item_code"]);
	# 	if(jack[0]['item_code'] in all_item):
	# 		res=frappe.get_all("Item Price",filters={'name':price[j]['name']},fields=['item_name','price_list_rate']);
	# 		sumo.append(res)

	
		
	return sumo


@frappe.whitelist(allow_guest=1)
def del_wishlist_items(item_code_user):
	alldata=frappe.db.get_values("Wishlist Item", filters={"parent": "Administrator", "parentfield": "items","parenttype": "Wishlist"} ,fieldname=["item_code"],order_by="creation")
	if(len(alldata)==0):
		return "No itemss are added in list ... ";
	user_name=[]
	for i in range(len(alldata)):
		user_name.append(list(alldata[i]))
	all_item=sum(user_name, [])
	if item_code_user not in all_item:
		return "Item Unavliable"
	
	frappe.db.delete("Wishlist Item", filters={"item_code": item_code_user, "parent": "Administrator"})
	frappe.db.commit()
	return "Item Deleted Successfully"


@frappe.whitelist(allow_guest=1)
def add_wishlist_items(item_code_user):
	if frappe.db.exists("Wishlist Item", {"item_code": item_code_user, "parent": "Administrator"}):
		return "Item already in WishList ..."
	web_item_data = frappe.db.get_value(
		"Website Item",
		filters={"item_code": item_code_user},fieldname=[
							"website_image",
							"website_warehouse",
							"name",
							"web_item_name",
							"item_name",
							"item_group",
							"route",
						],
						as_dict=1,
					)

	web_item_data["item_code"]= item_code_user
	web_item_data["website_item"]=web_item_data.get("name")
	wishlist = frappe.get_doc("Wishlist", "Administrator")
	
	item = wishlist.append("items", web_item_data)
	
	item.insert()
	# wishlist.save()

	# to save the document 
	frappe.db.commit()
	# item.save(ignore_permissions=True)

	# return item
	return "Item Added in Wishlist ...."	







