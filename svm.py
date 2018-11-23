# Import libraries
import numpy as np
import random
from sklearn import svm

# Define infiles
X_file = "/home/johannes/proj/crse/results/2018-11-22/feba_X.csv"
y_metal_file = "/home/johannes/proj/crse/results/2018-11-22/feba_y_metal.txt"
y_antibiotics_file = "/home/johannes/proj/crse/results/2018-11-22/feba_y_antibiotics.txt"

# Load data into numpy arrays
X = np.array([
    [float(x) for x in line.rstrip().split(",")] \
    for line in open(X_file).readlines()
])

y_m = np.array([int(l.rstrip()) for l in open(y_metal_file).readlines()])
y_a = np.array([int(l.rstrip()) for l in open(y_antibiotics_file).readlines()])

# Determine number of samples
n = X.shape[0]

# Split into training and test data
i_train   = np.array(random.sample(range(0, n), int(n/2)))
i_test    = np.array(list(set(range(0, n)) - set(i_train)))

X_train   = X[i_train]
X_test    = X[i_test]

y_m_train = y_m[i_train]
y_a_train = y_a[i_train]

y_m_test  = y_m[i_test]
y_a_test  = y_a[i_test]

# Train SVM
classifier_m = svm.SVC()
classifier_m.fit(X_train, y_m_train)

classifier_a = svm.SVC()
classifier_a.fit(X_train, y_a_train)

# Assess performance of classifier

# ...on training data:
m_acc_train = classifier_m.score(X_train, y_m_train) # 93.5%
a_acc_train = classifier_a.score(X_train, y_a_train) # 89.8%

# ...on test data:
m_acc_test  = classifier_m.score(X_test, y_m_test) # 93.6%
a_acc_test  = classifier_a.score(X_test, y_a_test) # 87.3%

# This should be compared to the accuracy by chance
m_acc_chance = 1 - sum(y_m) / len(y_m) # 92.9%
a_acc_chance = 1 - sum(y_a) / len(y_a) # 85.2%
