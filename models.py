
"""Основні класи: учні, класи, працівники та школа."""


class Student:
    """Один учень школи."""

    def __init__(
        self,
        last_name: str,
        first_name: str,
        patronymic: str,
        birth_year: int,
        gender: str,
        average_grade: float,
    ) -> None:
        if gender not in ("Ч", "Ж"):
            raise ValueError("Стать учня повинна бути 'Ч' або 'Ж'")

        if not 0 <= average_grade <= 12:
            raise ValueError("Середня оцінка повинна бути від 0 до 12")

        self.last_name = last_name
        self.first_name = first_name
        self.patronymic = patronymic
        self.birth_year = birth_year
        self.gender = gender
        self.average_grade = average_grade

    @property
    def full_name(self) -> str:
        return f"{self.last_name} {self.first_name} {self.patronymic}"


class SchoolClass:
    """Шкільний клас, наприклад 7-А."""

    def __init__(self, grade: int, letter: str) -> None:
        if not 1 <= grade <= 11:
            raise ValueError("Паралель повинна бути від 1 до 11")

        if not letter.strip():
            raise ValueError("Літера класу не може бути порожньою")

        self.grade = grade
        self.letter = letter.strip().upper()
        self.students: list[Student] = []

    @property
    def name(self) -> str:
        return f"{self.grade}{self.letter}"

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def promote(self) -> bool:
        if self.grade == 11:
            return False

        self.grade += 1
        return True


class Employee:
    """Батьківський клас усіх працівників."""

    position = "Працівник"

    def __init__(
        self, full_name: str, base_salary: float
    ) -> None:
        self.full_name = full_name
        self.base_salary = base_salary

    def calculate_salary(self) -> float:
        raise NotImplementedError("Формулу задає конкретна посада")


class Director(Employee):
    position = "Директор"

    def __init__(
        self,
        full_name: str,
        base_salary: float,
        pedagogical_years: int,
        management_years: int,
    ) -> None:
        super().__init__(full_name, base_salary)
        self.pedagogical_years = pedagogical_years
        self.management_years = management_years

    def calculate_salary(self) -> float:
        return (
            self.base_salary * self.pedagogical_years / 50
            + self.management_years * 500
        )


class Teacher(Employee):
    position = "Вчитель"

    def __init__(
        self,
        full_name: str,
        base_salary: float,
        pedagogical_years: int,
    ) -> None:
        super().__init__(full_name, base_salary)
        self.pedagogical_years = pedagogical_years

    def calculate_salary(self) -> float:
        return self.base_salary * self.pedagogical_years / 30


class Guard(Employee):
    position = "Охоронець"

    def __init__(
        self,
        full_name: str,
        base_salary: float,
        experience_years: int,
    ) -> None:
        super().__init__(full_name, base_salary)
        self.experience_years = experience_years

    def calculate_salary(self) -> float:
        return self.base_salary + self.experience_years * 250


class School:
    """Школа містить класи та працівників."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.classes: list[SchoolClass] = []
        self.employees: list[Employee] = []

    def find_class(
        self, grade: int, letter: str
    ) -> SchoolClass | None:
        for school_class in self.classes:
            if (
                school_class.grade == grade
                and school_class.letter == letter
            ):
                return school_class

        return None

    def add_class(self, school_class: SchoolClass) -> None:
        if self.find_class(
            school_class.grade, school_class.letter
        ) is not None:
            raise ValueError(f"Клас {school_class.name} вже існує")

        self.classes.append(school_class)

    @property
    def students(self) -> list[Student]:
        all_students: list[Student] = []

        for school_class in self.classes:
            for student in school_class.students:
                all_students.append(student)

        return all_students

    def promote_all_classes(self) -> int:
        updated_classes: list[SchoolClass] = []
        graduated = 0

        for school_class in self.classes:
            if school_class.promote():
                updated_classes.append(school_class)
            else:
                graduated += len(school_class.students)

        self.classes = updated_classes

        return graduated
