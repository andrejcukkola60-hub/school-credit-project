
"""Підрахунок статистики школи."""

from collections import Counter, defaultdict
from statistics import mean

from models import School, SchoolClass


def sorted_classes(
    school: School
) -> list[SchoolClass]:
    return sorted(
        school.classes,
        key=lambda c: (c.grade, c.letter)
    )


def school_statistics(
    school: School
) -> dict[str, int | float | str]:

    pupils = school.students
    total = len(pupils)

    class_sizes = [
        (c.name, len(c.students))
        for c in school.classes
    ]

    boys = sum(
        student.gender == "Ч"
        for student in pupils
    )

    girls = sum(
        student.gender == "Ж"
        for student in pupils
    )

    max_size = max(
        (count for _, count in class_sizes),
        default=0
    )

    min_size = min(
        (count for _, count in class_sizes),
        default=0
    )

    return {
        "Кількість учнів": total,

        "Хлопці, %": round(
            boys / total * 100, 2
        ) if total else 0.0,

        "Дівчата, %": round(
            girls / total * 100, 2
        ) if total else 0.0,

        "Середня кількість у класі": round(
            total / len(class_sizes), 2
        ) if class_sizes else 0.0,

        "Максимум учнів": max_size,

        "Класи з максимумом": ", ".join(
            name for name, n in class_sizes
            if n == max_size
        ) if class_sizes else "—",

        "Мінімум учнів": min_size,

        "Класи з мінімумом": ", ".join(
            name for name, n in class_sizes
            if n == min_size
        ) if class_sizes else "—",
    }


def students_by_parallel(
    school: School
) -> dict[int, int]:

    counts: dict[int, int] = defaultdict(int)

    for school_class in school.classes:
        counts[school_class.grade] += len(
            school_class.students
        )

    return dict(sorted(counts.items()))


def average_students_by_vertical(
    school: School
) -> dict[str, float]:

    groups: dict[str, list[int]] = defaultdict(list)

    for school_class in school.classes:
        groups[school_class.letter].append(
            len(school_class.students)
        )

    return {
        letter: mean(counts)
        for letter, counts in sorted(groups.items())
    }


def students_by_birth_year(
    school: School
) -> dict[int, int]:

    counts = Counter(
        student.birth_year
        for student in school.students
    )

    return dict(sorted(counts.items()))
