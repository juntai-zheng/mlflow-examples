import argparse
import pandas
import train_linear
import utils

# Trains a single-machine scikit-learn Elastic Net model on the provided data file, 
# producing a pickled model file. Uses MLflow tracking APIs to log the input parameters, 
# the model file, and the model's training loss.

#Parsing arguments.
parser = argparse.ArgumentParser()
parser.add_argument("data_path", help="Path to parquet dataset file.",
                    type=str)
parser.add_argument("alpha", help="Alpha value for Elastic Net linear regressor.",
                    type=float)
parser.add_argument("l1_ratio", help="""L1 ratio for Elastic Net linear regressor. 
                        See http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.ElasticNet.html
                        for more details.""",
                    type=float)
parser.add_argument("test_percent", help="Percent of data to use as test data.",
                    type=float)
parser.add_argument("label_col", help="Name of label column.",
                    type=str)
parser.add_argument("--feat-cols", help="""List of feature column names. 
                                Input must be a single string with columns delimited by commas.""",
                    type=lambda s: [str(i) for i in s.split(',')])

args = parser.parse_args()

# Reading the parquet file into a pandas dataframe.
pandasData = pandas.read_parquet(args.data_path)

args = utils.linear_arg_handler(args, pandasData)

# Train the model based on the parameters provided.
train_linear.train(pandasData, args.label_col, args.feat_cols, 
                    args.test_percent, args.alpha, args.l1_ratio, args.data_path)
