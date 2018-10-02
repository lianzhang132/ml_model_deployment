from pyspark.ml import Pipeline
from pyspark.ml import PipelineModel
from pyspark import SparkConf, SparkContext

import socket

# set the driver host to local ip address
ip = socket.gethostbyname(socket.gethostname())
SparkContext.setSystemProperty('spark.driver.host', ip)
conf = SparkConf().setAppName(
    'spark-deployment').setMaster('spark://spark-master:7077')
sc = SparkContext(conf=conf)

class PySparkModel(object):
    """
    Model template. You can load your model parameters in __init__ from a location accessible at runtime
    """

    def __init__(self):
        """
        Add any initialization parameters. These will be passed at runtime from the graph definition parameters defined in your seldondeployment kubernetes resource manifest.
        """
        self.server = "ad95fe885c37011e8aee806444a30499-1181034928.us-west-2.elb.amazonaws.com"
        self.pipeline = None
        self.model = None

    def predict(self, X, features_names):

        if self.pipeline is None:
            self.pipeline = Pipeline.read().load(
                "hdfs://{}:9000/tmp/classification-pipeline".format(self.server))
            self.model = PipelineModel.read().load(
                "hdfs://{}:9000/tmp/classification-model".format(self.server))
        # Make predictions.
        # TODO convert array to pandas data frame
        data = X
        predictions = self.model.transform(data)
        return predictions