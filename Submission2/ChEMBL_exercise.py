"""
Tis code uses the offical Python client library developed and supported by the ChEMBL group in order to access data and cheminformatics.
Client URL: https://github.com/chembl/chembl_webresource_client
"""
from chembl_webresource_client.new_client import new_client

available_resources = [resource for resource in dir(new_client) if not resource.startswith('_')]
print(available_resources)

print("\n")

molecule = new_client.molecule
activity = new_client.activity
target = new_client.target

all_approved_drugs = molecule.filter(max_phase=4).order_by('first_approval','pref_name')

all_approved_drugs_since_2012 = []
all_approved_drugs_since_2012_dict = {}

first_returned_drug = all_approved_drugs[0]

print(type(all_approved_drugs))
print(type(first_returned_drug))

"""
for key in first_returned_drug.keys():
	print("     ")
	print(key)
	print(first_returned_drug[key])
"""


for drug in all_approved_drugs:
	#print(drug["first_approval"])
	#print(type(drug["first_approval"]))
	approval_date = drug["first_approval"]
	if approval_date != None:
		if approval_date >= 2012:
			#all_approved_drugs_since_2012.append(drug)
			all_approved_drugs_since_2012_dict[drug['pref_name']] = [drug,[]]
			#all_approved_drugs_since_2012_dict[drug["accession"]] = []
			all_activities_for_molecule = activity.filter(molecule_chembl_id=drug["molecule_chembl_id"], pchembl_value__isnull=False)
			if len(all_activities_for_molecule) > 0:
				for activity_i in all_activities_for_molecule:
					try:
						accession_number = target.filter(target_chembl_id=activity_i["target_chembl_id"]).only('target_components')[0]["target_components"][0]["accession"]
						#print(accession_number)
						all_approved_drugs_since_2012_dict[drug['pref_name']][1].append(accession_number)
					except Exception:
						target_res = target.filter(target_chembl_id=activity_i["target_chembl_id"])[0]
						print(f"   Encountered exception on activity for {activity_i['target_chembl_id']} -> target_type: {target_res['target_type']}")
						#print(target_res)
			else:
				all_approved_drugs_since_2012_dict[drug['pref_name']][1].append(None)
			#print(f"{drug['first_approval']} | {drug['pref_name']} | {len(drug['pref_name'][1])} accession nums")
			print(f"{drug['first_approval']} | {drug['pref_name']} | {len(all_approved_drugs_since_2012_dict[drug['pref_name']][1])} accession numbers")
			print(f"Number of activities for this molecule: {len(all_activities_for_molecule)}")

print("---------------------------------------Stats-------------------------------------------------------")
print(f"Number of approved drugs in the query response: {len(all_approved_drugs)}")
print(f"Number of approved drugs since (and including) the year 2012: {len(all_approved_drugs_since_2012_dict)}")
print("--------------------------------------------------------------------------------------------------")

"""
first_approved_drug = all_approved_drugs_since_2012[0]

for key in first_approved_drug.keys():
	print("     ")
	print(key)
	print(first_approved_drug[key])

all_activities_for_molecule = activity.filter(molecule_chembl_id=first_approved_drug["molecule_chembl_id"], pchembl_value__isnull=False)[0]


for key in all_activities_for_molecule:
	print(type(key))
	print(key)
	print(all_activities_for_molecule[key])

target_accession = target.filter(target_chembl_id=all_activities_for_molecule["target_chembl_id"]).only('target_components')[0]["target_components"][0]["accession"]
print(type(target_accession))
print(target_accession)

for key in target_accession:
	print(type(key))
	print(key)
	print(target_accession[key])
"""