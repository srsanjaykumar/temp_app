# Copyright (c) 2023, human and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class userdata(Document):
	pass


@frappe.whitelist(allow_guest=1)
def user_data(username):
	doc = frappe.new_doc('userdata');
	doc.user_name=username
	doc.insert(ignore_permissions=True);
	doc.save();
	frappe.db.commit();
	dict={}
	dict['user_id']=doc.name

	return dict



@frappe.whitelist(allow_guest=1)
def user_value(user_id,quest_id,value):
# def user_value():
	alldoc=[]
	doc_name=frappe.get_list("userdata")
	for data in doc_name:
		alldoc.append(data['name'])
	if user_id not in alldoc:
		return "User ID is Not Avaliable ....."
	all_quest_id=[]
	all_id=frappe.get_list("ALLQuestions",fields=['uid'])
	for ids in all_id:
		all_quest_id.append(ids['uid'])
	if quest_id not in all_quest_id:
		return "Question ID is Not Avaliable ....."
	options= frappe.get_doc("userdata",user_id)
	optionid=[]
	print(len(options.selected_options))
	for i in range(len(options.selected_options)):
		optionid.append(options.selected_options[i].qid)
	if quest_id not in optionid:
		dummy={}
		dummy[quest_id]=value
		docdata=frappe.get_doc("userdata",user_id)
		opt=docdata.append("selected_options",dummy);
		opt.save();
		frappe.db.commit();
		options.reload()
		options.selected_options[len(options.selected_options)-1].qid=quest_id
		options.selected_options[len(options.selected_options)-1].values=value
		options.save()
		frappe.db.commit();
		options.reload()
		# return options
		omega={}
		omega['name']=options.name;
		omega['user_name']=options.user_name;
		datas={};
		for hu in range(len(options.selected_options)):
			datas[options.selected_options[hu].qid]=options.selected_options[hu].values
		omega['data']=datas
		return omega
	
	return "Question ID Already Exist in User ID"



@frappe.whitelist(allow_guest=1)
def calculation(user_id):
	alldoc=[]
	doc_name=frappe.get_list("userdata")
	for data in doc_name:
		alldoc.append(data['name'])
	if user_id not in alldoc:
		return "User ID is Not Avaliable ....."
	
	options= frappe.get_doc("userdata",user_id)

	question_id,question_values=filt_values(options)
	dictionary={}
	for i in range(len(question_id)):
		dictionary[question_id[i]]=question_values[i]
	return change(question_id,question_values,dictionary)


	# this code will take too much of lines 
	# return calc(question_id,question_values)


@frappe.whitelist(allow_guest=1)
def change(quest_id,quest_values,pair):

	# category names
	cat_doc_name=[]
	# period values 
	period_dict={}

	# getting  period values ,category names
	cat_doc= frappe.get_list('Category1')
	for data in cat_doc:
		cat_doc_name.append(data['name'])
		period_dict[data['name']]= frappe.get_doc('Category1',data['name']).cat_period
	
	trans_arr=[]

	final_dict={}
	# iterate category
	for i in range(len(cat_doc_name)):
		cat=cat_doc_name[i]
		if cat != "Transport":
			total_sumation=0
			for j in range(len(quest_id)):
				doc_name=frappe.get_list("ALLQuestions",filters={'uid':quest_id[j]})
				docs= frappe.get_doc("ALLQuestions",doc_name)
				category=docs.category
				if cat == category:
					
					for k in range(len(docs.options)):
						# check the options are equal or not 
						if docs.options[k].proc_name == pair[quest_id[j]]:
							option1=docs.options[k].proc_option
							# it will be yes or no type it will  skip the question 
							if len(option1)== 0:
								continue
							# if the category have no period value 
							if int(period_dict[cat])==0:
								value=float(option1)
								footprint=frappe.get_doc("Footprint1",docs.footprint).carbon_foot
								doc_final_value=value*float(footprint)
							#  Category have a period value 
							else:
								value=float(period_dict[cat])*float(option1)
								footprint=frappe.get_doc("Footprint1",docs.footprint).carbon_foot
								doc_final_value=value*float(footprint)
							#  adding value of each category 
							total_sumation=total_sumation+doc_final_value
				elif category == "Transport":
					if quest_id[j] not in trans_arr:
						trans_arr.append(quest_id[j])
			# finally we add the value in dictionary format				#  
			final_dict[cat]=total_sumation
	if(len(trans_arr)!=0):
			fir=0
			val=0
			val1=0	
			# iterating two doctypes and get the values 
			for i in range(len(trans_arr)):
				doc_name=frappe.get_list("ALLQuestions",filters={'uid':trans_arr[i]})
				docs= frappe.get_doc("ALLQuestions",doc_name)
				for j in range(len(docs.options)):
					if docs.options[j].proc_name == pair[trans_arr[i]]:
						if i==0:
							fir=docs.options[j].foot_print
						if i==1:
							fir=fir*float(docs.options[j].proc_option)*float(frappe.get_doc("Footprint1",docs.footprint).carbon_foot)
						if i==2:
							value=float(1)*float(docs.options[j].proc_option)
							val=fir+value*float(frappe.get_doc("Footprint1",docs.footprint).carbon_foot)
						if i==3:
							value=float(1)*float(docs.options[j].proc_option)
							val1=val+value*float(frappe.get_doc("Footprint1",docs.footprint).carbon_foot)
					
			final_dict['Transport']=val1

				
	return final_dict


@frappe.whitelist(allow_guest=1)
def filt_values(options):
	question_id=[]
	question_values=[]
	print(len(options.selected_options))
	for i in range(len(options.selected_options)):
		question_id.append(options.selected_options[i].qid)
		question_values.append(options.selected_options[i].values)
	circle=question_values.count("No")
	for i in range(circle):
		for j in range(len(question_values)):
			if question_values[j] =="No":
				del(question_values[j])
				del(question_id[j])
				del(question_values[j-1])
				del(question_id[j-1])
				break
	
	return question_id,question_values






