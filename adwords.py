import sys
import csv
import math
from random import shuffle
import random

def getQueries():
	queries = []
	for i in open("queries.txt"):
		queries.append(i.replace("\n",""))
	return queries	
	
def getBidders():
	bidders = []
	for row in csv.reader(open("bidder_dataset.csv")):   
		bidders.append(row)    
	return bidders		  	

def getAdvertiser(query,bidders):
	advertisers = [i for i in bidders if i[1] == query]
	return advertisers

def getAdvertiserWithBudgets(advertisers,budget):
	advertiserMap = []
	for val in advertisers:
		if budget[val[0]] >= float(val[2]):
			advertiserMap.append(val)
	return advertiserMap

# algorithms
#greedy
def greedy(advertiserMap):
	m = max(i[2] for i in advertiserMap)
	list = [i for i in advertiserMap if i[2] == m]
	return list	[0]	

#msvv
def msvvAlgo(advertiserMap,budget,initialBudget):
	max = 0.0
	list = []
	for i in advertiserMap:
		psi = (initialBudget[i[0]]-budget[i[0]])/initialBudget[i[0]]
		equation = 1 - math.exp(psi-1)
		if (float(i[2]) * equation) > max:
			max = (float(i[2]) * equation)
			list = i
	return list

#balance	
def balanceAlgo(advertiserMap,budget):
	max = 0
	for i in advertiserMap:
		if budget[i[0]] > max:
			max = budget[i[0]]
			list = i
	return list

def main(argv):
	choice = str(argv)
	map = {"greedy":1,"msvv":2,"balance":3}
	algo = map.get(choice)

	if not algo:
		print "Please select an algorithm(greedy/msvv/balance)."
	else:
		print	choice
		queries = getQueries()
		bidders = getBidders()    

		budget = {}
		for i in bidders[1:]:
			if(i[3]):
				budget[i[0]] = float(i[3])
		initialBudget = budget.copy()		
		optimalSum = sum(budget.values())
		revenue = 0.0
		for q in queries:
			advertisers = getAdvertiser(q,bidders)
			advertiserMap = getAdvertiserWithBudgets(advertisers,budget)
			if len(advertiserMap) >= 1:
				if algo == 1:
					listBidder = greedy(advertiserMap)
				elif algo == 2:
					listBidder = msvvAlgo(advertiserMap,budget,initialBudget)
				elif algo == 3:
					listBidder = balanceAlgo(advertiserMap,budget)
				revenue = revenue + float(listBidder[2])
				budget[listBidder[0]] = budget[listBidder[0]] - float(listBidder[2])
		print "Revenue 			:" + str(revenue)

		revenueList = []
		random.seed(0)
		for i in range(0,100):
			revenue = 0.0
			shuffle(queries)
			budget = initialBudget.copy()
			for q in queries:
				advertisers = getAdvertiser(q,bidders)
				advertiserMap = getAdvertiserWithBudgets(advertisers,budget)
				if len(advertiserMap) >= 1:
					if algo == 1:
						listBidder = greedy(advertiserMap)
					elif algo == 2:
						listBidder = msvvAlgo(advertiserMap,budget,initialBudget)
					elif algo == 3:
						listBidder = balanceAlgo(advertiserMap,budget)
					revenue = revenue + float(listBidder[2])
					budget[listBidder[0]] = budget[listBidder[0]] - float(listBidder[2])
			revenueList.append(revenue)
		print "Competitive Ratio 	:" + str(min(revenueList)/optimalSum)

if __name__ == "__main__":
	if(len(sys.argv) == 2):  
		main(sys.argv[1])
	else :
		print "Invalid no. of arguments"