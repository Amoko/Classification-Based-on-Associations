# coding:utf-8
import xlrd
import re
import time
import matplotlib.pyplot as plt
import cPickle as pickle

def go():
	book = xlrd.open_workbook("GegeInfo.xlsx")
	sheet = book.sheet_by_index(0)

	targets_info = []
	ac = [0] * 120
	pc = {}
	reo = re.compile(r"\"[aA][gG][eE].{0,3}\d+\"")
	for i in range(sheet.nrows):
		gsm = sheet.cell(i, 0).value
		gpl = sheet.cell(i, 1).value
		labels = sheet.cell(i, 2).value

		mo = reo.search(labels)
		if mo and "shimada" not in labels:
			gpl = gpl.replace(";", "")
			age = re.search(r"\d+", mo.group(0)).group(0)
			ac[int(age)] += 1
			if gpl in pc:
				pc[gpl] += 1
			else:
				pc[gpl] = 1
			#print i, repr(gsm), repr(gpl), age
			item = [str(gsm), str(gpl), int(age)]
			print i, len(targets_info), item
			targets_info.append(item)

	with open("targets_info.pickle", "w") as fp:
		pickle.dump(targets_info, fp)

	plt.subplot(211)
	plt.bar(range(120), ac)
	plt.xlabel("Age")
	plt.ylabel("Number of samples")
	plt.grid()
	
	plt.subplot(212)
	plt.bar(range(len(pc)), pc.values(), color="rgbkymc")
	plt.xticks(range(len(pc)), pc.keys(), rotation='vertical')
	plt.xlabel("Platform")
	plt.ylabel("Number of samples")

	#plt.subplot(212)
	#patches = plt.pie(pc.values(), autopct='%1.1f%%', startangle=90)
	#plt.axis('equal')
	
	plt.suptitle("Overview " + time.ctime())
	#plt.show()

def check():
	with open("targets.pickle", "rU") as fp:
		obj = pickle.load(fp)
	for i in obj:
		print repr(i)
	print len(obj)

def overview():
	with open("st.pickle", "rU") as fp:
		st = pickle.load(fp)

	with open("sd.pickle", "rU") as fp:
		sd = pickle.load(fp)

	plt.subplot(211)
	plt.plot([e[2] for e in st])
	plt.grid()
	plt.title("t")

	plt.subplot(212)
	plt.plot([e[1] for e in sd])
	plt.grid()
	plt.title("d")

	plt.show()

def final():
	with open("targets_info.pickle", "rU") as fp:
		targets_info = pickle.load(fp)
	
	with open("GSM.pickle", "rU") as fp:
		GSM = pickle.load(fp)

	GSM_info = {}
	for gsm in GSM:

		for item in targets_info:
			if gsm == item[0]:
				GSM_info[item[0]] = [item[1], item[2]]
	print len(GSM_info)

	with open("GSM_info.pickle", "w") as fp:
		pickle.dump(GSM_info, fp)

def go2():
	with open("GSM_info.pickle", "rU") as fp:
		GSM_info = pickle.load(fp)
	ac = [0] * 105
	pc = {}
	for key in GSM_info:
		gpl = GSM_info[key][0]
		age = GSM_info[key][1]
		ac[age] += 1
		if gpl in pc:
			pc[gpl] += 1
		else:
			pc[gpl] = 1
		plt.subplot(211)

	print pc
	
	plt.bar(range(105), ac)
	plt.xlabel("Age")
	plt.ylabel("Number of samples")
	plt.grid()
	
	plt.subplot(212)
	plt.bar(range(len(pc)), pc.values(), color="rgbkymc")
	plt.xticks(range(len(pc)), pc.keys(), rotation='vertical')
	plt.xlabel("Platform")
	plt.ylabel("Number of samples")
	plt.show()

if __name__ == "__main__":
	#test()
	go2()
	#check()
	#final()