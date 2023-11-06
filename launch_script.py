import platform; print(platform.platform())
import sys; print("Python", sys.version)
import numpy; print("NumPy", numpy.__version__)
import scipy; print("SciPy", scipy.__version__)

import pandas as pd
from joblib import load

import os
import numpy as np


def inference():

    # Load, read and normalize training data
    testing = "./test.csv"
    data_test = pd.read_csv(testing)
    print("Shape of the test data")
    print(data_test.shape)
    assert len(data_test.columns)==8, 'data_train and data_test have different shapes!'
    
    classifier = load('dbscan_orig_model.joblib')
    cluster_labels = classifier.predict(data_test)
    print(f'Num of clusters: {len(set(cluster_labels)) - (1 if -1 in cluster_labels else 0)}')