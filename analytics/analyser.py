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

        for country, count in self.result["top_3"]:
            print(f"{country}: {count}")

        print("=" * 30)