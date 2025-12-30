from dataclasses import dataclass

@dataclass

class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str

@dataclass

class DataValidationArtifact:
    valid_train_file_path: str
    valid_test_file_path: str
    invalid_train_file_path: str
    invalid_test_file_path: str
    drift_report_file_path: str
    drift_status: bool
    no_of_cols_status: bool
    
@dataclass

class DataTransformationArtifact:
    train_file_path: str
    test_file_path: str
    preprocessor_obj_path: str


@dataclass
class ClassificationMetricArtifact:
    recall_score: float
    accuracy_score: float
    f1_score: float


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
    train_metric_artifact: ClassificationMetricArtifact
    test_metric_artifact: ClassificationMetricArtifact