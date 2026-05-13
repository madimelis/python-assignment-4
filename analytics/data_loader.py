import os
import csv
class DataLoader:
    def __init__(self, folder, filename):
        self.folder = folder
        self.filename = filename
        self.students = []

    def load(self):
        print("Loading data...")
        
        try:
            with open(os.path.join(self.folder, self.filename), encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.students = [row for row in reader]
            
            print(f"Data loaded successfully: {len(self.students)} students")
            print(" ")
            return self.students

        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found. Please check the filename.")
            return self.students

        except Exception as e:
            print(f"Error: {e}")
            return []
    

    def preview_data(self, n = 5):
        print(f"First {n} rows:")
        print("-" * 30)
        for student in self.students[:n]:
            print(f"{student['student_id']} | {student['age']} | {student['gender']} | {student['country']} | GPA: {student['GPA']}")
        print("-" * 30)
        print(" ")