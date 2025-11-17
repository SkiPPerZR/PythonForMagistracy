from db import Base, engine, SessionLocal
from repository import StudentRepository

Base.metadata.create_all(bind=engine)

def main():
    db = SessionLocal()
    repo = StudentRepository(db)

    # Указать корректный путь нахождения файла students.csv вместо ###

    repo.load_from_csv('###')

    print("\n=== СТУДЕНТЫ ФАКУЛЬТЕТА РЭФ ===")
    for s in repo.get_by_faculty("РЭФ"):
        print(s.last_name, s.first_name, s.course, s.grade)

    print("\n=== СПИСОК УНИКАЛЬНЫХ КУРСОВ ===")
    print(repo.get_unique_courses())

    print("\n=== СРЕДНИЙ БАЛЛ ПО ФАКУЛЬТЕТУ ФПМИ ===")
    print(repo.get_average_grade("ФПМИ"))

    print("\n=== ОЦЕНКИ НИЖЕ 30 ПО ПРЕДМЕТУ 'Мат. Анализ' ===")
    for s in repo.get_low_score_by_course("Мат. Анализ"):
        print(s.last_name, s.first_name, s.grade)


if __name__ == "__main__":
    main()