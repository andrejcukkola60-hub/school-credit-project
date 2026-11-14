
"""Створення об'єкта школи."""

from models import Director, Guard, School, Teacher
from storage import load_school_data


def build_school() -> School:
    school = School("Навчальна школа № 1")

    # Завантажуємо класи та учнів
    load_school_data(school)

    # Додаємо директора
    school.employees.append(
        Director(
            "Коваленко Олена Петрівна",
            69000,
            25,
            10
        )
    )

    # Додаємо вчителів
    school.employees.append(
        Teacher(
            "Мельник Андрій Сергійович",
            50000,
            15
        )
    )

    school.employees.append(
        Teacher(
            "Петренко Ірина Миколаївна",
            67000,
            22
        )
    )

    school.employees.append(
        Teacher(
            "Шевченко Роман Іванович",
            1000,
            8
        )
    )

    # Додаємо охоронця
    school.employees.append(
        Guard(
            "Бондар Василь Олексійович",
            11000,
            12
        )
    )

    return school
