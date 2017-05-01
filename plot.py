import matplotlib.pyplot as plt
import cPickle as pickle
import time

with open("classifier2part1.1350.pickle", "rU") as fp:
	accs1 = pickle.load(fp)

with open("result2part1.1350.pickle", "rU") as fp:
	accs2 = pickle.load(fp)

def plot():
	plt.subplot(221)
	plt.xlabel("Rules number of current classifier")
	plt.ylabel("Accuracy")
	plt.title("train")
	plt.grid(True)
	plt.plot([e[2] for e in accs1], [e[1] for e in accs1], "ko")
	plt.plot([e[2] for e in accs1], [e[1] for e in accs1], "r-")

	plt.subplot(223)
	plt.xlabel("Rules number of current classifier")
	plt.ylabel("Samples number")
	plt.title("train")
	plt.fill_between([e[2] for e in accs1], [e[3] for e in accs1], 10208, label="covered")
	plt.fill_between([e[2] for e in accs1], 0, [e[3] for e in accs1], label="uncovered")
	plt.legend()

	plt.subplot(222)
	plt.xlabel("Rules number of current classifier")
	plt.ylabel("Accuracy")
	plt.title("test")
	plt.grid(True)
	plt.plot([e[2] for e in accs2], [e[1] for e in accs2], "ko")
	plt.plot([e[2] for e in accs2], [e[1] for e in accs2], "r-")

	plt.subplot(224)
	plt.xlabel("Rules number of current classifier")
	plt.ylabel("Samples number")
	plt.title("test")
	plt.fill_between([e[2] for e in accs2], [e[3] for e in accs2], 2555, label="covered")
	plt.fill_between([e[2] for e in accs2], 0, [e[3] for e in accs2], label="uncovered")
	plt.legend()

	plt.suptitle("demo " + time.ctime())
	plt.show()

def check():
	for item in accs2:
		print item

def test():
	plt.figure(1)
	plt.show()
	plt.figure(2)
	plt.show()

#test()
#check()
plot()
