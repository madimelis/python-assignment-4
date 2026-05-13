import os
import csv
import json

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
    
class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        print("Not implemented — use a child class")

    def print_results(self):
        for i, s in enumerate(self.result.get("top10", []), start=1):
            print(f"{i}. {s['student_id']} | {s['country']} | {s['major']} | Score: {s['final_exam_score']} | GPA: {s['GPA']}")

    def __str__(self):
        return f"DataAnalyser: base class, {len(self.students)} students"

class TopStudentsAnalyser(DataAnalyser):
    def __init__(self, students):
        super().__init__(students)

    def analyse(self):
        valid_students = []
        for s in self.students:
            try:
                s['final_exam_score'] = float(s['final_exam_score'])
                s['GPA'] = float(s['GPA'])
                valid_students.append(s)
            except ValueError:
                print(f"Warning: could not convert value for student {s.get('student_id')} — skipping row.")

        sorted_students = sorted(valid_students, key=lambda x: x['final_exam_score'], reverse=True)
        self.result = {"top10": sorted_students[:10]}

    def print_results(self):
        print("=" * 30)
        print("Top 10 Students by Exam Score")
        print("=" * 30)
        super().print_results()
        print("=" * 30)

    def __str__(self):
        return f"TopStudentsAnalyser: Top Students Analysis, {len(self.students)} students"


class CountryAnalyser(DataAnalyser):
    def __init__(self, students):
        super().__init__(students)

    def analyse(self):
        country_count = {}

        for s in self.students:
            country = s['country']

            if country in country_count:
                country_count[country] += 1
            else:
                country_count[country] = 1

        sorted_countries = sorted(
            country_count.items(),
            key=lambda x: x[1],
            reverse=True
        )

        self.result = {
            "total_students": len(self.students),
            "total_countries": len(country_count),
            "top_3": sorted_countries[:3]
        }

    def print_results(self):
        print("=" * 30)
        print("COUNTRY ANALYSIS REPORT")
        print("=" * 30)

        print(f"Total students: {self.result['total_students']}")
        print(f"Total countries: {self.result['total_countries']}")

        print("\nTop 3 Countries:")

        for country, count in self.result['top_3']:
            print(f"{country}: {count} students")

        print("=" * 30)

    def __str__(self):
        return f"CountryAnalyser: Country Analysis, {len(self.students)} students"

class ResultSaver:
    def __init__(self, result, filepath, output_path):
        self.result = result
        self.filepath = filepath
        self.output_path = output_path

    def save_json(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.result, f, indent=4)
        print(f"Result saved to {self.filepath}")


class Report:
    def __init__(self, analyser, saver):
        self.analyser = analyser
        self.saver = saver

    def generate(self):
        print("Generating report...")
        self.analyser.analyse()
        self.saver.result = self.analyser.result
        self.analyser.print_results()
        self.saver.save_json()
        print("Report complete.")


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

class Report:
    def __init__(self, analyser, saver):
        self.analyser = analyser
        self.saver = saver

    def generate(self):
        print("Generating report...")
        self.analyser.analyse()
        self.saver.result = self.analyser.result
        
        self.saver.save_json()
        print("Report complete.")

def main():
    folder = r"C:\Users\Админ\OneDrive\Рабочий стол\python-assignment-4"
    file_manager = FileManager(folder, "students.csv")
    if not file_manager.check_file():
        print('Stopping program.')
        return
    file_manager.check_output_folder()

    dl = DataLoader(folder, "students.csv")
    dl.load()
    dl.preview_data()

    analysers = [
        TopStudentsAnalyser(dl.students),
        CountryAnalyser(dl.students)  
    ]

    print("Running all analysers:")
    print("-" * 30)

    for analyser in analysers:
        analyser.analyse()
        analyser.print_results()

    saver = ResultSaver(analysers[0].result, folder, 'output/result.json')
    report = Report(analysers[0], saver)
    report.generate()

if __name__ == "__main__":
    main()