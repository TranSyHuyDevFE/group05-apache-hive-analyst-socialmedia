import pandas as pd
import os
from sentiment import SentimentAnalyzer

class SentimentProcessing:
    def __init__(self, input_dir=".", output_dir=".", text_column="content"):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.text_column = text_column

    def run(self):
        '''
          Doc file csv
          Xư ly cot content
          Save result to column 'sentiment'
        '''
        for filename in os.listdir(self.input_dir):
            if filename.endswith(".csv"):
                input_path = os.path.join(self.input_dir, filename)
                df = pd.read_csv(input_path)
                analyzer = SentimentAnalyzer()
                df = analyzer.analyze(df, text_column=self.text_column)
                df.to_csv(input_path, index=False)
                print(f"Updated {filename}:")
                print(df.head())

if __name__ == "__main__":
    # TODO: mark if file is processed , dont do it again, or not 
    main = SentimentProcessing(input_dir="../cleaned_data/comments", output_dir="../cleaned_data/comments")
    main.run()