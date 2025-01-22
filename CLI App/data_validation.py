from datetime import datetime
import os


class DataValidator:
    @staticmethod
    def validate_date(date_str: str) -> bool:
        try:
            datetime.strptime(date_str, "%B %Y")
            return True
        except ValueError:
            return False

    @staticmethod
    def validate_file(file_path: str) -> bool:
        return os.path.exists(file_path) and file_path.endswith((".xlsx", ".xls"))

    @staticmethod
    def validate_float(value: any) -> bool:
        try:
            float(value)
            return True
        except (ValueError, TypeError):
            return False
