from trend_videos_process import TrendVideosProcessor
import pandas as pd
import os
from utils.file_name import FileNameGenerator
from file_path import FilePaths


class MainProcessTrendVideos:
    def __init__(self, paths: FilePaths):
        self.paths = paths
        self.processor = TrendVideosProcessor()

    def run(self):
        print("Starting trend videos data preprocessing...")
        # Read input data
        try:
            data = pd.read_csv(self.paths.input_path)
        except Exception as e:
            print(f"Failed to read input data: {e}")
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
        # Generate output file name with prefix and date in HCM timezone
        output_dir = "/workspaces/py_env_research/group05-apache-hive-analyst-socialmedia/cleaned_data"
        os.makedirs(output_dir, exist_ok=True)
        output_file = FileNameGenerator.generate("video") + ".csv"
        output_path = os.path.join(output_dir, output_file)
        # Save processed data
        processed_data.to_csv(output_path, index=False)
        print(f"Trend videos data preprocessing completed successfully. Output saved to: {output_path}")

def main():
    paths = FilePaths(
        input_path="./term/trend_videos.csv",
        output_path=None,
    )
    main_process = MainProcessTrendVideos(paths)
    main_process.run()

if __name__ == "__main__":
    main()
