import csv
import os
from typing import Optional


class CSVHeaderRemover:
    def __init__(self, output_dir: str = "data/processed"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def process_csv(self, csv_file_path: str, output_filename: Optional[str] = None) -> str:
        csv_data = self._read_csv(csv_file_path)
        processed_data = self._remove_header(csv_data)
        if not output_filename:
            base_name = os.path.basename(csv_file_path)
            if not base_name.endswith('.csv'):
                base_name += '.csv'
            output_filename = f"no_header_{base_name}"

        output_path = self._save_csv(processed_data, output_filename)
        return output_path

    def _read_csv(self, file_path: str) -> list:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.reader(file)
                return list(csv_reader)

        except Exception as e:
            raise ValueError(f"Failed to read CSV from {file_path}: {e}")

    def _remove_header(self, csv_data: list) -> list:
        if not csv_data:
            raise ValueError("CSV data is empty")

        if len(csv_data) == 1:
            print("Warning: CSV contains only header row, result will be empty")
            return []

        return csv_data[1:]  # Skip first row (header)

    def _save_csv(self, data: list, filename: str) -> str:
        output_path = os.path.join(self.output_dir, filename)

        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerows(data)

            print(f"Processed CSV saved to: {output_path}")
            return output_path

        except IOError as e:
            raise IOError(f"Failed to save CSV to {output_path}: {e}")


# if __name__ == "__main__":
#     remover = CSVHeaderRemover()
#     csv_file_path = "./comments_25_07_2025.csv"  # Replace with actual file path
#     output_file = remover.process_csv(csv_file_path)
