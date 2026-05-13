import os
import json
class ResultSaver:
    def __init__(self, result, folder, output_path):
        self.result = result
        self.folder = folder
        self.output_path = output_path

    def save_json(self):
            try:
                with open(os.path.join(self.folder, self.output_path), 'w', encoding='utf-8') as f:
                    json.dump(self.result, f, indent=4)
                print(f"Result saved to {self.output_path}")
            except Exception as e:
                print(f"Error saving file: {e}")