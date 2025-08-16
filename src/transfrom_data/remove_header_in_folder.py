import os
import glob
from typing import List
from remove_header import CSVHeaderRemover


class CSVFolderProcessor:

    def __init__(self, transformed_folder_name: str = "transformed"):
        self.transformed_folder_name = transformed_folder_name

    def process_folder(self, input_directory: str) -> List[str]:
        if not os.path.exists(input_directory):
            raise FileNotFoundError(
                f"Input directory not found: {input_directory}")

        if not os.path.isdir(input_directory):
            raise ValueError(f"Path is not a directory: {input_directory}")

        csv_files = self._find_csv_files(input_directory)

        if not csv_files:
            raise ValueError(
                f"No CSV files found in directory: {input_directory}")

        output_directory = os.path.join(
            input_directory, self.transformed_folder_name)
        header_remover = CSVHeaderRemover(output_dir=output_directory)
        processed_files = []

        print(f"Found {len(csv_files)} CSV files to process...")

        for i, csv_file in enumerate(csv_files, 1):
            try:
                print(
                    f"Processing file {i}/{len(csv_files)}: {os.path.basename(csv_file)}")
                original_filename = os.path.basename(csv_file)
                output_path = header_remover.process_csv(
                    csv_file, original_filename)
                processed_files.append(output_path)

            except Exception as e:
                print(f"Error processing {csv_file}: {e}")
                continue

        print(
            f"Successfully processed {len(processed_files)} out of {len(csv_files)} files")
        print(f"Transformed files saved to: {output_directory}")

        return processed_files

    def _find_csv_files(self, directory: str) -> List[str]:
        csv_pattern = os.path.join(directory, "*.csv")
        csv_files = glob.glob(csv_pattern)
        return sorted(csv_files)


# if __name__ == "__main__":
#     processor = CSVFolderProcessor()
#     input_dir = "./comments"
#     processed_files = processor.process_folder(input_dir)
