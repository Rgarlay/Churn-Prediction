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
    