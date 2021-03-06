import seaborn as sb

#Exercise 1

a = 0.99 #Sensitivity, remains fixed for both exercises
b = 0.99 #Specificty
pop_inf = 0.05
pop_uninf = 1-pop_inf

TP = a*pop_inf / (a*pop_inf + (1-b)*pop_uninf )
print("For exercise 1, the answer is: ",TP)


#Exercise 2
allowed_b = [0.99, 0.999, 0.9999, 0.99999]
test_populations = {"Weil am Rhein":30009,
					"Basel":177595,
					"Hong Kong Island": 1270876,
					"Hong Kong Core": 3156500}
cities = ["Weil am Rhein", "Basel", "Hong Kong Island", "Hong Kong Core"]

def calc_tp(b,pop_inf=0.05):
	if pop_inf < 0.0001 or pop_inf > 0.5:
		print("Please give a population infection prevalence within the bounds 0.001% and 50%")
	if not (b in allowed_b):
		print("Please give a sensitivity within the allowed bounds") 
	pop_uninf = 1-pop_inf
	return( a*pop_inf / (a*pop_inf + (1-b)*pop_uninf ) )

print("\nExercise 2\n The probability that Fred is infected depends while he is visiting various cities depicted below depends with differing specifity of the tests is given through the True Positive (TP)")
for city in cities:
	pop_inf_total = pop_inf * test_populations[city]
	print(f"\n{city}:\nPopulation: {test_populations[city]},\tPopulation infected: 5% ({round(pop_inf_total)} rounded)\n")
	for i in allowed_b:
		TP = calc_tp(i)
		print(f"Sensitvity: {a}, Specificity:{i},\t TP: {TP}\t Total cases of TP (rounded to nearest int): {round(TP*pop_inf_total)}")
