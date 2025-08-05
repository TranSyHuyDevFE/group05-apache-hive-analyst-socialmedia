from .data_reader import DataReader
from .utils.file_name import FileNameGenerator
from .user_details_process import UserDetailsProcessor
import os
from .file_path import FilePaths


class MainProcessUserDetails:
    def __init__(self, paths: FilePaths):
        self.paths = paths
        self.io_handler = DataReader()
        self.processor = UserDetailsProcessor()

    def run(self):
        print("Starting user details preprocessing...")
        data = self.io_handler.read_csv(self.paths.input_path)
        if data is None:
            print("Failed to read input data. Exiting...")
            return
        print("Input data preview:")
        print(data.head())
        processed_data = self.processor.process(data)
        if processed_data is None:
            print("Data processing failed. Exiting...")
            return
        print("Processed data preview:")
        print(processed_data.head())
        os.makedirs(self.paths.output_path, exist_ok=True)
        output_file = FileNameGenerator.generate("user_info_details") + ".csv"
        output_path = os.path.join(self.paths.output_path, output_file)
        self.io_handler.save_csv(processed_data, output_path)
        print(
            f"User details preprocessing completed successfully. Output saved to: {output_path}")


def main():
    paths = FilePaths(
        input_path="./term/user_info.csv",
        output_path=None,  # Output path will be generated dynamically
    )
    main_process = MainProcessUserDetails(paths)
    main_process.run()


