# Copyright (c) 2023, human and contributors
# For license information, please see license.txt

import frappe,hashlib
from frappe.model.document import Document
from frappe import _
class ALLQuestions(Document):
	def before_insert(self):
		# frappe.throw(_(self.question))
		if(self.question):
			quest=self.question
			dummy=hashlib.sha256(quest.encode('utf-8')).hexdigest()[:8]
			self.name=dummy
			self.uid=dummy
		else:
			frappe.throw(_("Please Fill the Question "))
	# def onload(self):
	# 	# print(self.__dict__)
	# 	print("*"*500);
	# 	# print(frappe.get_list("ALLQuestions",filters={"name":"39294bd450"},fields=["*"]));
	# 	data=frappe.get_doc("ALLQuestions","39294bd450")
	# 	print(data.question)
	# 	dummy=hashlib.md5(self.question.encode()).hexdigest()
	# 	self.uid=dummy
	# 	print(dummy)
	# 	for info in self.options:
	# 		info.proc_name=self.question
	# 	for info in data.options:
	# 		print(info.proc_name);	
	def before_save(self):
		quest=self.question		
		self.uid=hashlib.sha256(quest.encode('utf-8')).hexdigest()[:8]
		# print(dummy)
		# for info in self.options:
		# 	info.proc_name=self.question


@frappe.whitelist(allow_guest=1)
def get():
	# order_by="creation"  => it will work depend on the fitle creation time 
	allCategoryNames=frappe.get_all("Category1",order_by="creation")
	dict={}
	for category in allCategoryNames:
		cat_name=category['name']
		catdoc=frappe.get_list("ALLQuestions",filters={"category":cat_name},order_by="creation");
		doc_each_quest=[]
		for cat in catdoc:
			doc_make_id={}
			part_doc=frappe.get_doc("ALLQuestions",cat['name'])
			doc_make_id['id']=part_doc.uid
			doc_make_id['question']=part_doc.question
			length=len(part_doc.options)
			num_of_option=[]
			for i in range(length):
				num_of_option.append("o"+str(i+1))
			opt={}
			for j in range(length):
				opt[num_of_option[j]]=part_doc.options[j].proc_name
			doc_make_id['values']=opt
			doc_each_quest.append(doc_make_id)
		dict[cat_name]=doc_each_quest
	return dict
