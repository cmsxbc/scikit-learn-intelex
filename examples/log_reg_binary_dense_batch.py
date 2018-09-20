#*******************************************************************************
# Copyright 2014-2018 Intel Corporation
# All Rights Reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License"), the following terms apply:
#
# You may not use this file except in compliance with the License.  You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#*******************************************************************************

# daal4py logistic regression example for shared memory systems

import daal4py as d4p
import numpy as np

# let's try to use pandas' fast csv reader
try:
    import pandas
    read_csv = lambda f, c: pandas.read_csv(f, usecols=c, delimiter=',', header=None).values
except:
    # fall back to numpy loadtxt
    read_csv = lambda f, c: np.loadtxt(f, usecols=c, delimiter=',')


def main():
    nClasses = 2
    nFeatures = 20

    # read training data from file with 20 features per observation and 1 class label
    trainfile = "./data/batch/binary_cls_train.csv"
    train_data = read_csv(trainfile, range(nFeatures))
    train_labels = read_csv(trainfile, range(nFeatures, nFeatures + 1))
    train_labels.shape = (train_data.shape[0], 1)  # must be a 2d array

    # set parameters and train
    train_alg = d4p.logistic_regression_training(nClasses=nClasses, interceptFlag=True)
    train_result = train_alg.compute(train_data, train_labels)

    # read testing data from file with 20 features per observation
    testfile = "./data/batch/binary_cls_test.csv"
    predict_data = read_csv(testfile, range(nFeatures))
    predict_labels = read_csv(testfile, range(nFeatures, nFeatures + 1))
    predict_labels.shape = (predict_data.shape[0], 1)

    # set parameters and compute predictions
    predict_alg = d4p.logistic_regression_prediction(nClasses=nClasses)
    predict_result = predict_alg.compute(predict_data, train_result.model)

    # the prediction result provides prediction
    assert predict_result.prediction.shape == (predict_data.shape[0], train_labels.shape[1])

    return (train_result, predict_result, predict_labels)


if __name__ == "__main__":
    (train_result, predict_result, predict_labels) = main()
    print("\nLogistic Regression coefficients:\n", train_result.model.Beta)
    print("\nLogistic regression prediction results (first 10 rows):\n", predict_result.prediction[0:10])
    print("\nGround truth (first 10 rows):\n", predict_labels[0:10])
    print('All looks good!')