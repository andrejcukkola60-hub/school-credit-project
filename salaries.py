
"""Сценарій 2: розрахунок зарплат працівників."""

from pathlib import Path

from bootstrap import build_school
from storage import save_salaries


def main() -> None:

    school = build_school()

    print("ЗАРПЛАТИ ПРАЦІВНИКІВ ШКОЛИ")
    print("-" * 75)

    for employee in school.employees:

        salary = employee.calculate_salary()

        print(
            f"{employee.position:10} | "
            f"{employee.full_name:35} | "
            f"{salary:.2f} грн"
        )

    file_path = (
        Path(__file__).resolve().parent / "salaries.csv"
    )

    save_salaries(school, file_path)

    print(
        f"\nФайл з результатами збережено: {file_path}"
    )


if __name__ == "__main__":
    main()
