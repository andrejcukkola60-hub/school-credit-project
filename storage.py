
"""Завантаження даних із CSV та збереження зарплат."""

import csv
from pathlib import Path

from models import School, SchoolClass, Student

DATA_DIR = Path(__file__).resolve().parent / "data"


def load_school_data(school: School) -> None:
    # Зчитуємо шкільні класи
    with (DATA_DIR / "classes.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        for row in csv.DictReader(file):
            school.add_class(
                SchoolClass(
                    int(row["grade"]),
                    row["letter"].strip()
                )
            )

    # Зчитуємо учнів
    with (DATA_DIR / "students.csv").open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        for row in csv.DictReader(file):
            school_class = school.find_class(
                int(row["class_grade"]),
                row["class_letter"].strip()
            )

            if school_class is None:
                raise ValueError(
                    "У CSV вказаний клас, якого немає в classes.csv"
                )

            student = Student(
                last_name=row["last_name"].strip(),
                first_name=row["first_name"].strip(),
                patronymic=row["patronymic"].strip(),
                birth_year=int(row["birth_year"]),
                gender=row["gender"].strip(),
                average_grade=float(row["average_grade"]),
            )

            school_class.add_student(student)


def save_salaries(
    school: School, filename: Path
) -> None:
    columns = [
        "Посада",
        "ПІБ",
        "Базова ставка",
        "Зарплата"
    ]

    with filename.open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=columns
        )

        writer.writeheader()

        for employee in school.employees:
            writer.writerow({
                "Посада": employee.position,
                "ПІБ": employee.full_name,
                "Базова ставка": f"{employee.base_salary:.2f}",
                "Зарплата": f"{employee.calculate_salary():.2f}",
            })
