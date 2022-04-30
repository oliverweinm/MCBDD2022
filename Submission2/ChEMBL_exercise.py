"""
Tis code uses the offical Python client library developed and supported by the ChEMBL group in order to access data and cheminformatics.
Client URL: https://github.com/chembl/chembl_webresource_client


Structure for the all_approved_drugs_since_2012_dict (example):
{
	"ACLIDINIUM BROMIDE": molecule.filter()_query_response, [List containing all UniProt accession numbers for the (protein) target], []
}

"""

from chembl_webresource_client.new_client import new_client
#from uniprot import retrieve
from xmltodict import parse
from requests import get
import sys
from statistics import median


print("\n")

molecule = new_client.molecule
activity = new_client.activity
target = new_client.target

all_approved_drugs = molecule.filter(max_phase=4).order_by('first_approval','pref_name')

all_approved_drugs_since_2012_dict = {}
keyword_count_dict = {}

def keywords_for_uniprot_id(accession):
	requestURL = "".join(["https://www.ebi.ac.uk/proteins/api/proteins/",accession_number])
	r = get(requestURL, headers={ "Accept" : "application/xml"})
	response_decoded_dict = parse(r.text)
	keywords = dict()
	try:
		for key in response_decoded_dict["entry"]["keyword"]:
			keywords[key["@id"]] = key["#text"]
			if (key["#text"] in keyword_count_dict):
				keyword_count_dict[key["#text"]] += 1
			else:
				keyword_count_dict[key["#text"]] = 1
	except Exception as e2:
		#print("--------------------------------------------------------")
		return("0")
	return(keywords)

median_values = []
for drug in all_approved_drugs:
	approval_date = drug["first_approval"]
	if approval_date != None and approval_date >= 2012: #take away approval_date < 2015 after debugging state is done
		all_approved_drugs_since_2012_dict[drug['pref_name']] = [drug,[],{}]
		all_activities_for_molecule = activity.filter(molecule_chembl_id=drug["molecule_chembl_id"], pchembl_value__isnull=False)
		if len(all_activities_for_molecule) > 0:
			for activity_i in all_activities_for_molecule:
				try:
					accession_number = target.filter(target_chembl_id=activity_i["target_chembl_id"]).only('target_components')[0]["target_components"][0]["accession"]
					all_approved_drugs_since_2012_dict[drug['pref_name']][1].append(accession_number)
				except Exception as exc:
					continue
					#target_res = target.filter(target_chembl_id=activity_i["target_chembl_id"])[0]
					#print(f"   Encountered exception on activity for {activity_i['target_chembl_id']} -> target_type: {target_res['target_type']}")
			#print(f"{drug['first_approval']} | {drug['pref_name']} | Number of activities for this molecule: {len(all_activities_for_molecule)} | {len(all_approved_drugs_since_2012_dict[drug['pref_name']][1])} accession numbers")
			median_values.append(len(all_approved_drugs_since_2012_dict[drug['pref_name']][1]))
			keywords = keywords_for_uniprot_id(' '.join( all_approved_drugs_since_2012_dict[drug["pref_name"]][1]) )
			all_approved_drugs_since_2012_dict[drug['pref_name']][2] = keywords
		else:
			all_approved_drugs_since_2012_dict[drug['pref_name']][1].append(None)


median_value = median(median_values)

#print(median_values)

most_frequent_keyword_1 = max(keyword_count_dict, key=keyword_count_dict.get)
keyword_count_dict.pop(most_frequent_keyword_1)
most_frequent_keyword_2 = max(keyword_count_dict, key=keyword_count_dict.get)
keyword_count_dict.pop(most_frequent_keyword_2)
most_frequent_keyword_3 = max(keyword_count_dict, key=keyword_count_dict.get)
keyword_count_dict.pop(most_frequent_keyword_3)
most_frequent_keyword_4 = max(keyword_count_dict, key=keyword_count_dict.get)
keyword_count_dict.pop(most_frequent_keyword_4)
most_frequent_keyword_5 = max(keyword_count_dict, key=keyword_count_dict.get)

print("---------------------------------------Stats-------------------------------------------------------")
print(f"Number of approved drugs in the query response: {len(all_approved_drugs)}")
print(f"Number of approved drugs since (and including) the year 2012: {len(all_approved_drugs_since_2012_dict)}")
print(f"Median of number of protein targets associacted with a drug (approved since the eyar 2012): {median_value}")
print(f"Average number of protein targets associated per drug: {sum(median_values)/len(all_approved_drugs_since_2012_dict)}")
print(f"Most frequent keywords in the dictionary: {most_frequent_keyword_1,most_frequent_keyword_2,most_frequent_keyword_3, most_frequent_keyword_4, most_frequent_keyword_5}")
print("--------------------------------------------------------------------------------------------------")


