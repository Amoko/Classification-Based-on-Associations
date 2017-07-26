# coding: utf-8
import time
import cPickle as pickle

def read_data(path):
	with open(path + ".pickle", "rU") as fp:
		obj = pickle.load(fp)
	print len(obj), path + " elements load over.", time.ctime()
	return obj
	
# start with here
# rule: alpha(condset) to beta(class)
# alpha: A>B
# beta: A[0, 20) B[20, 40) C[40, 60) D[60, +)
def isalpha(line, c):
	flag = True
	for i in range(len(c)):
		if i == 0:
			continue
		if line[c[i-1]] < line[c[i]]:
			flag = False
			break
	return flag


def which_beta(line, GSM_info):
	gsm = line[0]
	age = GSM_info[gsm][1]
	#print age
	if age < 20:
		label = "A"
	elif age < 40:
		label = "B"
	elif age < 60:
		label = "C"
	else:
		label = "D"

	return label

# ---storage form---
# alpha[position, ...]
# rule[alpha, beta, support, confidence]
# classifier[added_rule, acc, len(classifier), len(remain)]
def pruning():
	#condsets = read_data("condsets2")
	matrix = read_data("train")
	GSM_info = read_data("GSM_info")

	mini_sup = 0.05
	mini_conf = 0.5
	rules = []
	L = len(matrix[0])
	N = len(matrix)
	
	#for i in range(len(condsets)):
	for i in range(200, 300):
		if i%10 == 0:
			print i, len(rules), time.ctime()
		for j in range(i + 1, L):
			alpha = [i, j]
			count_alpha = 0.0
			d = {"A":0.0, "B":0.0, "C":0.0, "D":0.0}
			for line in matrix:
				if isalpha(line, alpha):
					count_alpha += 1
					beta = which_beta(line, GSM_info)
					d[beta] += 1
			beta = max(d, key=d.get)
			count_rule = d[beta]
			support = count_rule / N
			confidence = count_rule / count_alpha
			#print d, support, confidence
			if support >= mini_sup and confidence >= mini_conf:
				temp = [alpha, beta, support, confidence]
				print temp
				rules.append(temp)
		#rules.sort(key = lambda x: (x[3], x[2]), reverse = True)
		#rules = rules[0: 10000]

	with open("rules2part200.300.pickle", "w") as fp:
		pickle.dump(rules, fp)

def merge():
	keys1 = read_data("rules2part1.1050")
	keys2 = read_data("rules2part1050.L")
	#keys3 = read_data("rules2part9000.L")
	
	for key in keys2:
		keys1.append(key)
	print len(keys1), keys1[-1]
	'''
	for key in keys3:
		keys1.append(key)
	print len(keys1), keys1[-1]
	'''
	with open("rules2part1.L.pickle", "w") as fp:
		pickle.dump(keys1, fp)

def connect():
	rules = read_data("rules2")
	#time.sleep(30)

	L = len(rules)
	condsets = []
	for i in range(L):
		if i%1000 == 0:
			print i, len(condsets), time.ctime()
		A= rules[i][0]
		piece = A[1:]
		for j in range(i + 1, L):
			B = rules[j][0]
			if piece == B[:-1]:
				alpha = list(A)
				alpha.append(B[-1])
				print alpha
				condsets.append(alpha)

	with open("condsets6.pickle", "w") as fp:
		pickle.dump(condsets, fp)

def rule_generator():
	#connect()
	pruning()
	#merge()

	'''
	rules = read_data("rules2")
	c = [x[-1] for x in rules]
	print len(c), max(c)
	d = {"A":0.0, "B":0.0, "C":0.0, "D":0.0}
	for x in rules:
		d[x[1]] += 1
	print d
	'''
	'''
	GSM_info = read_data("GSM_info")
	matrix = read_data("train")

	d = {"A":0.0, "B":0.0, "C":0.0, "D":0.0}
	for line in matrix:
		beta = which_beta(line, GSM_info)
		d[beta] += 1
	print d
	for key in d:
		print key, d[key] / sum(d.values())
	'''

def accuracy(matrix, order, GSM_info):
	true = 0.0
	default = "D"
	for line in matrix:
		hit = False
		for rule in order:
			alpha, beta = rule[0], rule[1]
			if isalpha(line, alpha) and which_beta(line, GSM_info) == beta:
				true += 1
				hit = True
				break
		if not hit  and which_beta(line, GSM_info) == default:
			true += 1
	return true / len(matrix)

def classifier_builder():
	matrix = read_data("train")
	GSM_info = read_data("GSM_info")
	rules = read_data("rules2part1.1050")

	N = len(matrix)

	#sort
	rules.sort(key = lambda x: (x[2], x[1]), reverse = True)
	print rules[0], "\n", rules[-1]
	print time.ctime()

	'''
	#how many should it hit?
	T = 0
	for line in matrix:
		if isbeta(line, GSM_info):
			T += 1
	print T
	'''

	#building
	order, classifier = [], []
	hit, remain = [], matrix
	for rule in rules:
		alpha, beta = rule[0], rule[1]
		hit = [line for line in remain if isalpha(line, alpha) and which_beta(line, GSM_info) == beta]
		if len(hit) > 0:
		#if len(hit) >= 0.01 * N:
			for e in hit:
				remain.remove(e)
			order.append(rule)
			acc = accuracy(matrix, order, GSM_info)
			temp = (rule, acc, len(order), len(remain))
			print temp
			classifier.append(temp)
		'''
		if T - (N - len(remain)) < 0.01 * N:
			break
		'''
	print "Builded over."
	with open("classifier2part1.1050.pickle", "w") as fp:
		pickle.dump(classifier, fp)

def valaidate():
	matrix = read_data("test")
	GSM_info = read_data("GSM_info")
	classifier = read_data("classifier2part1.1050")

	order, result = [], []
	hit, remain = [], matrix
	for item in classifier:
		alpha, beta = item[0][0], item[0][1]
		hit = [line for line in remain if isalpha(line, alpha) and which_beta(line, GSM_info) == beta]
		for e in hit:
			remain.remove(e)
		order.append(alpha)
		acc = accuracy(matrix, order, GSM_info)
		temp = (item[0], acc, len(order), len(remain))
		print temp
		result.append(temp)
	
	with open("result2part1.1050.pickle", "w") as fp:
		pickle.dump(result, fp)


if __name__ == "__main__":
	print "Start.", time.ctime()
	rule_generator()
	#classifier_builder()
	#valaidate()
	#time.sleep(10)
	print "End.", time.ctime()
