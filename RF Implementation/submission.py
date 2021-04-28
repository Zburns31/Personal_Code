import csv
import numpy as np  # http://www.numpy.org
import ast
from datetime import datetime
from math import log, floor, ceil
import random
import numpy as np
import itertools


class Utility(object):

    # This method computes entropy for information gain
    def entropy(self, class_y):
        # Input:
        #   class_y         : list of class labels (0's and 1's)

        # TODO: Compute the entropy for a list of classes
        #
        # Example:
        #    entropy([0,0,0,1,1,1,1,1,1]) = 0.918 (rounded to three decimal places)

        entropy = 0
        ### Implement your code here
        #############################################
        base = 2
        count = len(class_y)
        # Get unique labels so we can find probability for each one
        unique_labels = list(set(class_y))

        # Get probability for each class label
        prob_vec = [class_y.count(label) / len(class_y) for label in unique_labels]

        # Calculate entropy
        entropy = -sum([prob * log(prob, base) for prob in prob_vec])
        #############################################
        return entropy

    def partition_classes(self, X, y, split_attribute, split_val):
        # Inputs:
        #   X               : data containing all attributes
        #   y               : labels
        #   split_attribute : column index of the attribute to split on
        #   split_val       : a numerical value to divide the split_attribute

        # TODO: Partition the data(X) and labels(y) based on the split value - BINARY SPLIT.
        #
        # Split_val should be a numerical value
        # For example, your split_val could be the mean of the values of split_attribute
        #
        # You can perform the partition in the following way
        # Numeric Split Attribute:
        #   Split the data X into two lists(X_left and X_right) where the first list has all
        #   the rows where the split attribute is less than or equal to the split value, and the
        #   second list has all the rows where the split attribute is greater than the split
        #   value. Also create two lists(y_left and y_right) with the corresponding y labels.

        """
        Example:



        X = [[3, 10],                 y = [1,
             [1, 22],                      1,
             [2, 28],                      0,
             [5, 32],                      0,
             [4, 32]]                      1]



        Here, columns 0 and 1 represent numeric attributes.



        Consider the case where we call the function with split_attribute = 0 and split_val = 3 (mean of column 0)
        Then we divide X into two lists - X_left, where column 0 is <= 3  and X_right, where column 0 is > 3.



        X_left = [[3, 10],                 y_left = [1,
                  [1, 22],                           1,
                  [2, 28]]                           0]



        X_right = [[5, 32],                y_right = [0,
                   [4, 32]]                           1]

        """

        X_left = []
        X_right = []

        y_left = []
        y_right = []
        ### Implement your code here
        #############################################

        # Need to check for numeric or string types first
        for i in range(len(X)):
            # check if feature values are strings
            if isinstance(X[i][split_attribute], str):
                # Check if string value is equal, if it is, assign to left node
                if X[i][split_attribute] == split_val:
                    X_left.append(X[i])
                    y_left.append(y[i])
                else:  # string value not equal, assign to right node
                    X_right.append(X[i])
                    y_right.append(y[i])

            else:  # numeric features
                if X[i][split_attribute] <= split_val:
                    X_left.append(X[i])
                    y_left.append(y[i])
                else:
                    X_right.append(X[i])
                    y_right.append(y[i])
        #############################################
        return (X_left, X_right, y_left, y_right)

    def information_gain(self, previous_y, current_y):
        # Inputs:
        #   previous_y: the distribution of original labels (0's and 1's)
        #   current_y:  the distribution of labels after splitting based on a particular
        #               split attribute and split value

        # TODO: Compute and return the information gain from partitioning the previous_y labels
        # into the current_y labels.
        # You will need to use the entropy function above to compute information gain
        # Reference: http://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15381-s06/www/DTs.pdf

        """
        Example:

        previous_y = [0,0,0,1,1,1]
        current_y = [[0,0], [1,1,1,0]]

        info_gain = 0.45915
        """

        info_gain = 0
        ### Implement your code here
        #############################################

        # Need to compare entropy of before splitting and the after for the left/right branches
        entropy_before_split = self.entropy(previous_y)
        entropy_left = self.entropy(current_y[0])
        entropy_right = self.entropy(current_y[1])

        # Calculate number of total elements and the number of elements in each split
        num_elements = len(list(itertools.chain.from_iterable(current_y)))
        num_elements_left = len(current_y[0])
        num_elements_right = len(current_y[1])

        # Calculate entropy using weighted average after the split has occured
        entropy_split = (num_elements_left / num_elements) * entropy_left + (
            num_elements_right / num_elements
        ) * entropy_right

        # Calculate information gain
        info_gain = entropy_before_split - entropy_split

        #############################################
        return info_gain

    def best_split(self, X, y):
        # Inputs:
        #   X       : Data containing all attributes
        #   y       : labels
        #   TODO    : For each node find the best split criteria and return the split attribute,
        #             spliting value along with  X_left, X_right, y_left, y_right (using partition_classes)
        #             in the dictionary format {'split_attribute':split_attribute, 'split_val':split_val,
        #             'X_left':X_left, 'X_right':X_right, 'y_left':y_left, 'y_right':y_right, 'info_gain':info_gain}
        """

        Example:

        X = [[3, 10],                 y = [1,
             [1, 22],                      1,
             [2, 28],                      0,
             [5, 32],                      0,
             [4, 32]]                      1]

        Starting entropy: 0.971

        Calculate information gain at splits: (In this example, we are testing all values in an
        attribute as a potential split value, but you can experiment with different values in your implementation)

        feature 0:  -->    split_val = 1  -->  info_gain = 0.17
                           split_val = 2  -->  info_gain = 0.01997
                           split_val = 3  -->  info_gain = 0.01997
                           split_val = 4  -->  info_gain = 0.32
                           split_val = 5  -->  info_gain = 0

                           best info_gain = 0.32, best split_val = 4


        feature 1:  -->    split_val = 10  -->  info_gain = 0.17
                           split_val = 22  -->  info_gain = 0.41997
                           split_val = 28  -->  info_gain = 0.01997
                           split_val = 32  -->  info_gain = 0

                           best info_gain = 0.4199, best split_val = 22


       best_split_feature: 1
       best_split_val: 22

       'X_left': [[3, 10], [1, 22]]
       'X_right': [[2, 28],[5, 32], [4, 32]]

       'y_left': [1, 1]
       'y_right': [0, 0, 1]
        """

        split_attribute = 0
        split_val = 0
        X_left, X_right, y_left, y_right = [], [], [], []
        ### Implement your code here
        #############################################
        max_info_gain = 0
        num_features = len(X[0])

        for feature in range(num_features):
            # Filter data to only include feature i
            data = [i[feature] for i in X]

            for val in set(data):

                X_left, X_right, y_left, y_right = self.partition_classes(
                    X, y, split_attribute=feature, split_val=val
                )

                info_gain = self.information_gain(y, [y_left, y_right])
                #                 print(f"Info gain: {info_gain} for feature: {feature}, value: {val}")
                #                 print(f"Left split:{X_left} and right split: {X_right}")

                if info_gain > max_info_gain:
                    max_info_gain = info_gain
                    best_split_attribute = feature
                    best_split_val = val
                    best_X_left = X_left
                    best_X_right = X_right
                    best_y_left = y_left
                    best_y_right = y_right

        return {
            "split_attribute": best_split_attribute,
            "split_val": best_split_val,
            "X_left": best_X_left,
            "X_right": best_X_right,
            "y_left": best_y_left,
            "y_right": best_y_right,
            "info_gain": max_info_gain,
        }
        #############################################


class DecisionTree(object):
    def __init__(self, max_depth):
        # Initializing the tree as an empty dictionary or list, as preferred
        self.tree = {}
        self.max_depth = max_depth

    def learn(self, X, y, par_node={}, depth=0):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in Utility class to train the tree

        # par_node is a parameter that is useful to pass additional information to call
        # the learn method recursively. Its not mandatory to use this parameter

        # Use the function best_split in Utility class to get the best split and
        # data corresponding to left and right child nodes

        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        ### Implement your code here
        #############################################
        self.tree = self.construct_decision_tree(X, y, par_node=par_node, depth=depth)

    def construct_decision_tree(self, X, y, par_node, depth):
        # Utility helper class to for calculating split points
        utility = Utility()

        # base case 1: no data
        if len(y) == 0:
            return None

        # base case 2: tree stops at previous level
        if par_node is None:
            return None

        # base case 3: if all labels are of one class
        if all(x == y[0] for x in y):
            return y[0]

        # base case 4: if max_depth is reached
        if depth >= self.max_depth:
            return self.get_majority(y)

        # base case 5: if 1 or 0 values remaining, we can't split on this
        # Need to return
        if len(y) <= 1:
            return self.get_majority(y)

        if len(y) <= 1:
            return self.get_majority(y)

        if len(X[0]) <= 1:
            return self.get_majority(y)

        # Check to see if root node will perfectly segment classes
        split_dict = utility.best_split(X, y)

        if len(split_dict["X_left"]) == 0 or len(split_dict["X_right"]) == 0:
            return self.get_majority(y)

        else:  # Tree construction

            # Set Root node of tree with split_attribute and split_value
            par_node["Node"] = {
                "split_attribute": split_dict["split_attribute"],
                "split_val": split_dict["split_val"],
            }

            # Construct Left and Right subtrees
            # Left tree: if val <= split_val
            par_node["Left_Tree"] = self.construct_decision_tree(
                X=split_dict["X_left"], y=split_dict["y_left"], par_node={}, depth=depth + 1
            )
            # Right tree: if val > split_val
            par_node["Right_Tree"] = self.construct_decision_tree(
                X=split_dict["X_right"], y=split_dict["y_right"], par_node={}, depth=depth + 1
            )

            return par_node

    def get_majority(self, labels):
        # return majority class label
        return max(labels, key=labels.count)

        #############################################

    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        ### Implement your code here
        #############################################
        # Get current DT from instance attribute
        node = self.tree

        while isinstance(
            node, dict
        ):  # Iterate until we hit a left/right tree with an integer value
            feat = node["Node"]
            split_attribute = feat["split_attribute"]
            split_val = feat["split_val"]

            if record[split_attribute] <= split_val:
                node = node["Left_Tree"]
            else:
                node = node["Right_Tree"]

        return node
        #############################################


# This starter code does not run. You will have to add your changes and
# turn in code that runs properly.

"""
Here,
1. X is assumed to be a matrix with n rows and d columns where n is the
number of total records and d is the number of features of each record.
2. y is assumed to be a vector of labels of length n.
3. XX is similar to X, except that XX also contains the data label for each
record.
"""

"""
This skeleton is provided to help you implement the assignment.You must
implement the existing functions as necessary. You may add new functions
as long as they are called from within the given classes.

VERY IMPORTANT!
Do NOT change the signature of the given functions.
Do NOT change any part of the main function APART from the forest_size parameter.
"""


class RandomForest(object):
    num_trees = 0
    decision_trees = []

    # the bootstrapping datasets for trees
    # bootstraps_datasets is a list of lists, where each list in bootstraps_datasets is a bootstrapped dataset.
    bootstraps_datasets = []

    # the true class labels, corresponding to records in the bootstrapping datasets
    # bootstraps_labels is a list of lists, where the 'i'th list contains the labels corresponding to records in
    # the 'i'th bootstrapped dataset.
    bootstraps_labels = []

    def __init__(self, num_trees):
        # Initialization done here
        self.num_trees = num_trees
        self.decision_trees = [DecisionTree(max_depth=10) for i in range(num_trees)]
        self.bootstraps_datasets = []
        self.bootstraps_labels = []

    def _bootstrapping(self, XX, n):
        # Reference: https://en.wikipedia.org/wiki/Bootstrapping_(statistics)
        #
        # TODO: Create a sample dataset of size n by sampling with replacement
        #       from the original dataset XX.
        # Note that you would also need to record the corresponding class labels
        # for the sampled records for training purposes.

        sample = []  # sampled dataset
        labels = []  # class labels for the sampled records
        ### Implement your code here
        #############################################

        # Select n random indices from XX (dataset)
        random_samples = np.random.choice(len(XX), size=n)

        # Remove labels from dataset which are located in the last position of the list
        sample = [XX[i][:-1] for i in random_samples]

        # Get labels which are the last column in each sublist
        labels = [XX[i][-1] for i in random_samples]

        #############################################
        return (sample, labels)

    def bootstrapping(self, XX):
        # Initializing the bootstap datasets for each tree
        for i in range(self.num_trees):
            data_sample, data_label = self._bootstrapping(XX, len(XX))
            self.bootstraps_datasets.append(data_sample)
            self.bootstraps_labels.append(data_label)

    def fitting(self):
        # TODO: Train `num_trees` decision trees using the bootstraps datasets
        # and labels by calling the learn function from your DecisionTree class.
        ### Implement your code here
        #############################################

        for i in range(len(self.decision_trees)):
            print(f"Building Decision Tree {i}")
            self.decision_trees[i].learn(self.bootstraps_datasets[i], self.bootstraps_labels[i])

        #############################################

    def voting(self, X):
        y = np.array([], dtype=int)

        for record in X:
            # Following steps have been performed here:
            #   1. Find the set of trees that consider the record as an
            #      out-of-bag sample.
            #   2. Predict the label using each of the above found trees.
            #   3. Use majority vote to find the final label for this recod.
            votes = []

            for i in range(len(self.bootstraps_datasets)):
                dataset = self.bootstraps_datasets[i]

                if record not in dataset:
                    OOB_tree = self.decision_trees[i]
                    effective_vote = OOB_tree.classify(record)
                    votes.append(effective_vote)

            counts = np.bincount(votes)

            dt_votes = []
            if len(counts) == 0:
                # TODO: Special case
                #  Handle the case where the record is not an out-of-bag sample
                #  for any of the trees.
                # NOTE - you can add few lines of codes above (but inside voting) to make this work
                ### Implement your code here
                #############################################
                # If record used by all DT's in sampling, lets use the majority
                print("Special Case: Using majority vote across DT's")

                # Loop through each decision tree and get the prediction and store it
                # so we can take the majority decision
                for tree in self.decision_trees:
                    dt_votes.append(tree.classify(record))

                # get counts for each class and take the maximum value
                vote_counts = np.bincount(dt_votes)
                y = np.append(y, np.argmax(vote_counts))

                #############################################
            else:
                y = np.append(y, np.argmax(counts))

        return y

    def user(self):
        """
        :return: string
        your GTUsername, NOT your 9-Digit GTId
        """
        ### Implement your code here
        #############################################
        return "zburns6"
        #############################################


# TODO: Determine the forest size according to your implementation.
# This function will be used by the autograder to set your forest size during testing
# VERY IMPORTANT: Minimum forest_size should be 10
def get_forest_size():
    forest_size = 10
    return forest_size


# TODO: Determine random seed to set for reproducibility
# This function will be used by the autograder to set the random seed to obtain the same results you achieve locally
def get_random_seed():
    random_seed = 42
    return random_seed
