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