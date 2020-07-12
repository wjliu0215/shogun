#!/usr/bin/env python
from numpy import array,hstack
from numpy.random import seed, rand
from tools.load import LoadMatrix
lm=LoadMatrix()

traindat = lm.load_numbers('../data/fm_train_real.dat')
testdat = lm.load_numbers('../data/fm_test_real.dat')
label_traindat = lm.load_labels('../data/label_train_twoclass.dat')

parameter_list = [[traindat,testdat,label_traindat]]

def transfer_multitask_l12_logistic_regression (fm_train=traindat,fm_test=testdat,label_train=label_traindat):
	from shogun import BinaryLabels, Task, TaskGroup
	try:
		from shogun import MultitaskL12LogisticRegression
	except ImportError:
		print("MultitaskL12LogisticRegression not available")
		exit(0)
	import shogun as sg

	features = sg.create_features(hstack((traindat,traindat)))
	labels = BinaryLabels(hstack((label_train,label_train)))

	n_vectors = features.get_num_vectors()
	task_one = Task(0,n_vectors//2)
	task_two = Task(n_vectors//2,n_vectors)
	task_group = TaskGroup()
	task_group.append_task(task_one)
	task_group.append_task(task_two)

	mtlr = MultitaskL12LogisticRegression(0.1,0.1,task_group)
	mtlr.set_tolerance(1e-2) # use 1e-2 tolerance
	mtlr.set_max_iter(10)
	mtlr.train(features,labels)
	mtlr.set_current_task(0)
	out = mtlr.apply_regression(features).get_labels()

	return out

if __name__=='__main__':
	print('TransferMultitaskL12LogisticRegression')
	transfer_multitask_l12_logistic_regression(*parameter_list[0])
