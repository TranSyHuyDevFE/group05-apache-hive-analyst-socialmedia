
from .data_reader import DataReader
from .video_details_process import VideoDetailsProcessor
from .utils.file_name import FileNameGenerator
import os
from .file_path import FilePaths

# Read from ./term/details_video_info.csv
# proecesss
# Save to ./term/details_video_info_processed.csv


class MainProcessDetailsVid:
    """
    Class to encapsulate the main processing logic for video details.
    """

    def __init__(self, paths: FilePaths):
        self.paths = paths
        self.io_handler = DataReader()
        self.processor = VideoDetailsProcessor()

    def run(self):
        """
        Execute the main processing logic.
        """
        print("Starting data preprocessing...")

        # Read input data
        data = self.io_handler.read_csv(self.paths.input_path)
        if data is None:
            print("Failed to read input data. Exiting...")
            return

        print("Input data preview:")
        print(data.head())

        # Process data
        processed_data = self.processor.process(data)
        if processed_data is None:
            print("Data processing failed. Exiting...")
            return

        print("Processed data preview:")
        print(processed_data.head())

        os.makedirs(self.paths.output_path, exist_ok=True)
        output_file = FileNameGenerator.generate("video_info_details") + ".csv"
        output_path = os.path.join(self.paths.output_path, output_file)

        # Save processed data
        self.io_handler.save_csv(processed_data, output_path)
        print(
            f"Data preprocessing completed successfully. Output saved to: {output_path}")


def main():
    """
    Main function for the data preprocessing script.
    """
    paths = FilePaths(
        input_path="./term/details_video_info.csv",
        output_path=None,  # Output path will be generated dynamically
    )
    main_process = MainProcessDetailsVid(paths)
    main_process.run()

