from NetworkSecurity.entity.artifact_entity import ClassificationMetricsArtifacts
from NetworkSecurity.expection.expection import NetworkSecurityExpection
from sklearn.metrics import f1_score,precision_score,recall_score
import sys


def get_classification_score(y_true,y_pred)->ClassificationMetricsArtifacts:
    try:
        model_f1_score=f1_score(y_true,y_pred)
        model_precision_score=precision_score(y_true,y_pred)
        model_recall_score=recall_score(y_true,y_pred)

        classification_metrics=ClassificationMetricsArtifacts(
            f1_score=model_f1_score,
            precision_score=model_precision_score,
            recall_score=model_recall_score
        )
        return classification_metrics
    
    except Exception as e:
        NetworkSecurityExpection(e,sys)