import time
import cPickle as pickle

def read_data(path):
	with open(path + ".pickle", "rU") as fp:
		obj = pickle.load(fp)
	print len(obj), path + " elements load over.", time.ctime()
	return obj

def choose_t():
	targets = read_data("targets")
	path1 = "GeneExpressionTable.filter.txt"
	path2 = "ChosenTargets.txt"
	f1 = open(path1, "rU")
	f2 = open(path2, "w")
	i = 0
	for line in f1:
		temp = line
		line = line.split()
		gsm = line[0]
		if gsm in targets:
			na = line.count("NA")
			print i, gsm, na, len(line) - na
			f2.write(temp)
		i += 1
	f1.close()
	f2.close()

def sort_by_target():
	path1 = "ChosenTargets.txt"
	path2 = "DataAfterS1.txt"
	with open(path1, "rU") as fp:
		data = fp.readlines()
	
	stat = []
	for i in range(len(data)):
		line = data[i]
		line = line.split()
		gsm = line[0]
		na = line.count("NA")
		item = [i, gsm, na]
		stat.append(item)
		#print len(stat), item
	stat.sort(key=lambda x: x[2])

	'''
	with open("st.pickle", "w") as fp:
		pickle.dump(stat, fp)
	return
	'''
	
	f2 = open(path2, "w")
	i = 0
	for item in stat:
		line = data[item[0]]
		f2.write(line)
	f2.close()

def sort_by_dimen():
	path1 = "DataAfterS1.txt"
	path2 = "DataAfterS2.txt"
	with open(path1, "rU") as fp:
		data = fp.readlines()
	print "load over.", time.ctime()
	
	na = [0] * 20660
	for j in range(len(data)):
		line = data[j]
		line = line.split()
		for i in range(1, 20660):
			if line[i] == "NA":
				na[i] += 1
		if j%1000 == 0:
			print j, line[0], time.ctime()
	stat = []
	for i in range(1, 20660):
		stat.append([i, na[i]])
	stat.sort(key=lambda x: x[1])

	'''
	with open("sd.pickle", "w") as fp:
		pickle.dump(stat, fp)
	return
	'''

	f2 = open(path2, "w")
	for j in range(len(data)):
		line = data[j]
		line = line.split()
		nl = []
		nl.append(line[0])
		for item in stat:
			nl.append(line[item[0]])
		
		for item in nl:
			f2.write(str(item) + "\t")
		f2.write("\n")
		if j%1000 == 0:
			print j, line[0], time.ctime()
	f2.close()

def groth_row(matrix, line, columns):
	for c in columns:
		if line[c] == "NA":
			return matrix, False
	matrix.append(line)
	return matrix, True

def groth_column(matrix, columns, c):
	for line in matrix:
		if line[c] == "NA":
			return columns, False 
	columns.append(c)
	return columns, True

def final():
	path1 = "DataAfterS2.txt"
	#path2 = "Data.txt"
	with open(path1, "rU") as fp:
		data = fp.readlines()
	print "load over.", time.ctime()

	r, c = 0, 0
	matrix, columns = [], []
	line = data[0]
	line = line.split()
	matrix.append(line)
	columns.append(0)
	while(r < 28200 and c < 20600):
		#growth a row
		while(True and r < 28200):
			r += 1
			line = data[r]
			line = line.split()
			matrix, success = groth_row(matrix, line, columns)
			if success == True:
				break
			else:
				#print r, "groth row failed"
				pass
		
		#groth a column
		while(True and c < 20660):
			c += 1
			columns, success = groth_column(matrix, columns, c)
			if success == True:
				break
			else:
				#print c, "groth column failed"
				pass
		
		if r % 1000 == 0:
			print r, c, len(matrix), len(columns), time.ctime()
	print r, c, len(matrix), len(columns), time.ctime()
	return matrix, columns

def convert(matrix, columns):
	for i in range(len(matrix)):
		line = matrix[i]
		nl = []
		nl.append(str(line[0]))
		for j in range(1, len(columns)):
			item = float(line[columns[j]])
			nl.append(item)
		matrix[i] = nl
	
	with open("data.pickle", "w") as fp:
		pickle.dump(matrix, fp)


def division(matrix):
	GSM_info = read_data("GSM_info")
	stat = {'GPL6884': 1067, 'GPL6102': 103, 'GPL10558': 843, 'GPL6947': 2174, 'GPL6480': 787, 'GPL570': 7789}

	threshold, rest, flag = {}, {}, {}
	count1, count2 = 0, 0
	for gpl in stat:
		threshold[gpl] = int(stat[gpl] * 0.8)
		count1 += threshold[gpl]
		rest[gpl] = stat[gpl] - threshold[gpl]
		count2 += rest[gpl]
		flag[gpl] = 0
	print threshold, count1, 12763 * 0.8
	print rest, count2, 12763 *0.2
	print flag

	train, test = [], []
	for line in matrix:
		gsm = line[0]
		gpl = GSM_info[gsm][0]
	
		if flag[gpl] < threshold[gpl]:
			train.append(line)
			flag[gpl] += 1
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
	train, test = division(matrix)
	saving(train, test)	

if __name__ == "__main__":
	print "Start.", time.ctime()
	#choose_t()
	#sort_by_target()
	#sort_by_dimen()
	#matrix, columns = final()
	#convert(matrix, columns)
	pre()
	print "End.", time.ctime()
