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
def split_data(X, y, split=0.5):
    # Determine size of training data to use
    N = len(y)
    n = min(sum(y == 1), sum(y == 0))
    n_train = int(n*split)
    n_test = n - n_train
    # Randomly select positive training examples
    i_train_pos = np.array(
        random.sample(list(np.array(range(0, N))[y == 1]), n_train)
    )
    # Randomly select negative training examples
    i_train_neg = np.array(
        random.sample(list(np.array(range(0, N))[y == 0]), n_train)
    )
    # Randomly select positive test examples not in training data
    i_test_pos = np.array(
        random.sample(
            list(set(np.array(range(0, N))[y == 1]) - set(i_train_pos)), n_test
        )
    )
    # Randomly select negative test examples not in training data
    i_test_neg = np.array(
        random.sample(
            list(set(np.array(range(0, N))[y == 0]) - set(i_train_neg)), n_test
        )
    )
    # Concatenate to training and test datasets
    i_train = np.concatenate((i_train_pos, i_train_neg))
    i_test = np.concatenate((i_test_pos, i_test_neg))
    # Subset X to training and test datasets
    X_train = X[i_train]
    X_test = X[i_test]
    # Subset y to training and test datasets
    y_train = y[i_train]
    y_test = y[i_test]
    # Return the data
    return X_train, y_train, X_test, y_test

X_train_m, y_m_train, X_test_m, y_m_test = split_data(X, y_m)
X_train_a, y_a_train, X_test_a, y_a_test = split_data(X, y_a)

# Train SVM
classifier_m = svm.SVC(C=10.0)
classifier_m.fit(X_train_m, y_m_train)

classifier_a = svm.SVC(C=10.0)
classifier_a.fit(X_train_a, y_a_train)

# Assess performance of classifier

# ...on training data:
m_acc_train = classifier_m.score(X_train_m, y_m_train)
a_acc_train = classifier_a.score(X_train_a, y_a_train)

# ...on test data:
m_acc_test  = classifier_m.score(X_test_m, y_m_test)
a_acc_test  = classifier_a.score(X_test_a, y_a_test)
