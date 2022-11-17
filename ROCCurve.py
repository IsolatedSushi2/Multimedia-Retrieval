import sklearn.metrics

def plotRocCurve(predictions, labels, distances=None):
    metrics.roc_curve(predictions, 1/distances, labels)
