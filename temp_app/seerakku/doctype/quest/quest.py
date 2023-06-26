# Copyright (c) 2023, human and contributors
# For license information, please see license.txt

import frappe,hashlib

from frappe.model.document import Document

class quest(Document):
	def before_save(self):
		for data in self.quest:
			
			# generate hash for each quest 
			data.id=hashlib.md5(data.question.encode()).hexdigest()

@frappe.whitelist(allow_guest=1)
def get():
	doc_data= frappe.get_doc("quest" ,"Transport")
	# fetch that particular value 
	return doc_data.quest[0].question;


@frappe.whitelist(allow_guest=1)
def json():
	all_data=frappe.get_all("quest");
	dict={}
	for data in all_data:
		doc_name=data['name']
		res=frappe.get_doc("quest",doc_name)
		all_question=[]
		for i in range(len(res.quest)):
			final_dict={}
			val={}
			all=res.quest[i];
			final_dict['id']=all.id;
			final_dict['quest']=all.question
			if(all.get("option_1")):
				val['o1']=all.get("option_1")
			if(all.get("option_2")):
				val['o2']=all.get("option_2")
			if(all.get("option_3")):
				val['o3']=all.get("option_3")
			if(all.get("option_4")):
				val['o4']=all.get("option_4")
			if(all.get("option_5")):
				val['o5']=all.get("option_5")
			if(all.get("option_6")):
				val['o6']=all.get("option_6")
			if(all.get("option_7")):
				val['o7']=all.get("option_7")
			final_dict['values']=val
			all_question.append(final_dict)
		dict[doc_name]=all_question
	return dict


@frappe.whitelist(allow_guest=1)
def check():
	return frappe.get_doc("quest" ,"Transport")


