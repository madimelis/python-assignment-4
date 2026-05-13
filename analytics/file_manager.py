import os
class FileManager:
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        file_path = os.path.join(self.folder, self.filename)
        if not os.path.exists(file_path):
            print(f"Error: {self.filename} not found")
            return False
        print(f"File found: {self.filename}")
        print(" ")
        return True
    
    def check_output_folder(self, folder = "output"):
        print("Checking output folder...")
        output_path = os.path.join(self.folder, folder)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")
        print(" ")
        return True