from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str


@dataclass
class DataValidationArtifact:
    data_validation_dir: str
    drift_report_file_path: str
    validation_status: bool
    message: str


@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str

@dataclass
class ClassificationMetricArtifact:
    f1_score: float
    precision_score: float
    recall_score: float
    accuracy_score: float
    roc_auc_score: float
    confusion_matrix: str
    classification_report: str

@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    metric_artifact: ClassificationMetricArtifact
