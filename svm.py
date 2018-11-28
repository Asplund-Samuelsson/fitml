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

y1 = np.array([int(l.rstrip()) for l in open(y_metal_file).readlines()])
y2 = np.array([int(l.rstrip()) for l in open(y_antibiotics_file).readlines()])

# Determine number of samples
n = X.shape[0]

# Print a header
print("\t".join([
    "classifier", "sample", "split", "C", "gamma", "train", "test", "cross"
]))

# Define function for splitting data into training and test sets
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

# Iterate over splits
for split in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]:
    # Iterate over C values
    for C in [0.001, 0.01, 0.1, 1, 10, 100, 1000]:
        # Iterate over gamma values
        for gamma in [0.0001, 0.001, 0.01, 0.1, 1, 10, 100]:
            # Iterate over samples
            for n in range(1, 11):
                # Split data
                X1_train, y1_train, X1_test, y1_test = split_data(X, y1, split)
                X2_train, y2_train, X2_test, y2_test = split_data(X, y2, split)
                # Train SVM classifiers
                classifier1 = svm.SVC(C=C, gamma=gamma).fit(X1_train, y1_train)
                classifier2 = svm.SVC(C=C, gamma=gamma).fit(X2_train, y2_train)
                # Assess performance...
                # ...on training data:
                acc_train1 = classifier1.score(X1_train, y1_train)
                acc_train2 = classifier2.score(X2_train, y2_train)
                # ...on test data:
                acc_test1  = classifier1.score(X1_test, y1_test)
                acc_test2  = classifier2.score(X2_test, y2_test)
                # ...on the other test data:
                acc_cross1 = classifier1.score(X2_test, y2_test)
                acc_cross2 = classifier2.score(X1_test, y1_test)
                # Print performance
                print("\t".join([str(x) for x in [
                    "metal", n, split, C, gamma,
                    acc_train1, acc_test1, acc_cross1
                ]]))
                print("\t".join([str(x) for x in [
                    "antibiotics", n, split, C, gamma,
                    acc_train2, acc_test2, acc_cross2
                ]]))
