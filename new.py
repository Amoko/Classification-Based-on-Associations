# coding: utf-8
import time
import cPickle as pickle

def read_data(path):
	with open(path + ".pickle", "rU") as fp:
		obj = pickle.load(fp)
	print len(obj), path + " elements load over.", time.ctime()
	return obj

def data_profile(matrix):
	F, M, LGBT = 0, 0, 0
	stat = {}
	N = len(matrix)
	for i in range(N):
		info = matrix[i][0]
		e = info.index("_")
		platform = info[e+1:-2]
		sex = info[-1]
		#print platform, sex
		if stat.get(platform):
			stat[platform] += 1
		else:
			stat[platform] = 1
		if sex == "F":
			F += 1
		elif sex == "M":
			M += 1
		else:
			LGBT += 1
	print F, M, LGBT, F + M + LGBT
	print stat, sum(stat.values())

def division(matrix):
	stat = {
	'GPL10558': 1234, 'GPL6102': 254, 'GPL6884': 580, 
	'GPL4133': 600, 'GPL6947': 1673, 'GPL6480': 654, 'GPL570': 5811}

	threshold, rest, flag = {}, {}, {}
	count1, count2 = 0, 0
	for key in stat:
		threshold[key] = int(stat[key] * 0.8)
		count1 += threshold[key]
		rest[key] = stat[key] - threshold[key]
		count2 += rest[key]
		flag[key] = 0
	print threshold, count1, 10806 * 0.8
	print rest, count2, 10806 *0.2
	print flag

	train, test = [], []
	for line in matrix:
		info = line[0]
		e = info.index("_")
		key = info[e+1:-2]
	
		if flag[key] < threshold[key]:
			train.append(line)
			flag[key] += 1
		else:
			test.append(line)
		#break
	print len(train), len(test), time.ctime()
	return train, test

def saving(train, test):
	with open("train.pickle", "w") as fp:
		pickle.dump(train, fp)
	with open("test.pickle", "w") as fp:
		pickle.dump(test, fp)

def pre():
	matrix = read_data("data")
	data_profile(matrix)
	train, test = division(matrix)
	saving(train, test)
	
# start with here
# rule: alpha(condset) to beta(class)
# alpha: A>B
# beta: female
def isalpha(line, c):
	flag = True
	for i in range(len(c)):
		if i == 0:
			continue
		if line[c[i-1]] < line[c[i]]:
			flag = False
			break
	return flag

def isbeta(line):
	sex = line[0][-1]
	#print sex
	if sex == "F":
		flag = True
	else:
		flag = False
	return flag
# ---storage form---
# condsets[position, ...]
# rules[condset, support, confidence]
# classifier[added_rule, acc, len(classifier), len(remain)]
def pruning():
	#condsets = read_data("condsets2")
	matrix = read_data("train")

	mini_sup = 0.3
	mini_conf = 0.51
	rules = []
	L = len(matrix[0])
	N = len(matrix)
	
	#for i in range(len(condsets)):
	for i in range(3000, 7000):
		if i%10 == 0:
			print i, len(rules), time.ctime()
		for j in range(i + 1, L):
			alpha = [i, j]
			count_rule, count_alpha = 0.0, 0.0
			for line in matrix:
				if isalpha(line, alpha):
					count_alpha += 1
					if isbeta(line):
						count_rule += 1
			support = count_rule / N
			confidence = count_rule / count_alpha
			#print support, confidence
			if support >= mini_sup and confidence >= mini_conf:
				#print alpha, support, confidence
				rules.append([alpha, support, confidence])
				'''
				if confidence > max_conf:
					max_conf = confidence
					print max_conf
				'''
	with open("rules2part2.pickle", "w") as fp:
		pickle.dump(rules, fp)

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
	pass

def accuracy(matrix, order):
	true = 0.0
	for line in matrix:
		default = "M"
		hit = False
		for alpha in order:
			if isalpha(line, alpha) and isbeta(line):
				true += 1
				hit = True
				break
		if not hit  and line[0][-1] == default:
			true += 1
	return true / len(matrix)

def classifier_builder():
	matrix = read_data("train")
	rules = read_data("rules2")
	N = len(matrix)

	#sort
	rules.sort(key = lambda x: (x[2], x[1]), reverse = True)
	print rules[0], "\n", rules[-1]
	print time.ctime()

	#building
	order, classifier = [], []
	hit, remain = [], matrix
	for rule in rules:
		alpha = rule[0]
		hit = [line for line in remain if isalpha(line, alpha) and isbeta(line)]
		if len(hit) >= 0.01 * N:
			for e in hit:
				remain.remove(e)
			order.append(alpha)
			acc = accuracy(matrix, order)
			temp = (rule, acc, len(order), len(remain))
			print temp
			classifier.append(temp)
		if remain == []:
			break
	with open("classifier2.pickle", "w") as fp:
		pickle.dump(classifier, fp)

def valaidate():
	matrix = read_data("test")
	classifier = read_data("classifier2")

	order, result = [], []
	hit, remain = [], matrix
	for item in classifier:
		alpha = item[0][0]
		hit = [line for line in remain if isalpha(line, alpha) and isbeta(line)]
		for e in hit:
			remain.remove(e)
		order.append(alpha)
		acc = accuracy(matrix, order)
		temp = (item[0], acc, len(order), len(remain))
		print temp
		result.append(temp)
	
	with open("result2.pickle", "w") as fp:
		pickle.dump(classifier, fp)

def merge():
	keys1 = read_data("rules2part1")
	keys2 = read_data("rules2part2")
	keys3 = read_data("rules2part3")
	
	for key in keys2:
		keys1.append(key)
	print len(keys1), keys1[-1]

	for key in keys3:
		keys1.append(key)
	print len(keys1), keys1[-1]

	with open("rules2.pickle", "w") as fp:
		pickle.dump(keys1, fp)

if __name__ == "__main__":
	print "Start.", time.ctime()
	merge()
	#rule_generator()
	classifier_builder()
	valaidate()
	#time.sleep(10)
	print "End.", time.ctime()