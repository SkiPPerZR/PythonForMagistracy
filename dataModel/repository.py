import csv
from sqlalchemy.orm import Session
from models import Student


class StudentRepository:

    def __init__(self, db: Session):
        self.db = db
    # INSERT
    def load_from_csv(self, filename="students.csv"):
        with open(filename, encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=",")
            for row in reader:
                student = Student(
                    last_name=row["Фамилия"],
                    first_name=row["Имя"],
                    faculty=row["Факультет"],
                    course=row["Курс"],
                    grade=int(row["Оценка"])
                )
                self.db.add(student)
        self.db.commit()

    # SELECT METHODS

    def get_by_faculty(self, faculty: str):
        return self.db.query(Student).filter(Student.faculty == faculty).all()

    def get_unique_courses(self):
        return sorted({s.course for s in self.db.query(Student).all()})

    def get_average_grade(self, faculty: str):
        students = self.get_by_faculty(faculty)
        if not students:
            return 0
        return sum(s.grade for s in students) / len(students)

    def get_low_score_by_course(self, course: str):
        return (
            self.db.query(Student)
            .filter(Student.course == course, Student.grade < 30)
            .all()
        )
