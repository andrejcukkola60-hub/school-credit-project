
"""Сценарій 1: статистика школи та графіки."""

import matplotlib.pyplot as plt
import streamlit as st

from analytics import (
    average_students_by_vertical,
    school_statistics,
    sorted_classes,
    students_by_birth_year,
    students_by_parallel,
)

from bootstrap import build_school


# Налаштування сторінки
st.set_page_config(
    page_title="Статистика школи",
    layout="wide"
)

st.title("Статистика школи")

st.caption(
    "Залікова робота з програмування. Демонстраційні дані."
)


# Ініціалізація школи
if "school" not in st.session_state:
    st.session_state.school = build_school()

    st.session_state.before = school_statistics(
        st.session_state.school
    )

    st.session_state.promoted = False
    st.session_state.graduated = 0


school = st.session_state.school
stats = school_statistics(school)


# Виведення статистики
st.subheader("Основні показники")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Учнів у школі",
    stats["Кількість учнів"]
)

c2.metric(
    "Хлопці",
    f'{stats["Хлопці, %"]}%'
)

c3.metric(
    "Дівчата",
    f'{stats["Дівчата, %"]}%'
)

c4.metric(
    "Середнє на клас",
    stats["Середня кількість у класі"]
)

st.write(
    f'Максимум: **{stats["Максимум учнів"]}** — '
    f'{stats["Класи з максимумом"]}'
)

st.write(
    f'Мінімум: **{stats["Мінімум учнів"]}** — '
    f'{stats["Класи з мінімумом"]}'
)


# Таблиця класів
st.subheader("Таблиця класів")

st.dataframe(
    [
        {
            "Клас": c.name,
            "Паралель": c.grade,
            "Вертикаль": c.letter,
            "Кількість учнів": len(c.students)
        }
        for c in sorted_classes(school)
    ],
    hide_index=True,
    use_container_width=True
)


# ГРАФІК 1
# Кількість учнів за паралелями

st.subheader("Графік 1. Учні за паралелями")

by_parallel = students_by_parallel(school)

fig1, ax1 = plt.subplots()

ax1.bar(
    list(by_parallel),
    list(by_parallel.values())
)

ax1.set_xlabel("Паралель")
ax1.set_ylabel("Кількість учнів")
ax1.set_xticks(list(by_parallel))

st.pyplot(fig1)
plt.close(fig1)


# ГРАФІК 2
# Середня кількість учнів за вертикалями

st.subheader(
    "Графік 2. Середня кількість учнів за вертикалями"
)

by_vertical = average_students_by_vertical(school)

fig2, ax2 = plt.subplots()

ax2.bar(
    list(by_vertical),
    list(by_vertical.values())
)

ax2.set_xlabel("Вертикаль (літера класу)")
ax2.set_ylabel("Середня кількість учнів")

st.pyplot(fig2)
plt.close(fig2)


# ГРАФІК 3
# Кількість учнів за роком народження

st.subheader(
    "Графік 3. Кількість учнів за роком народження"
)

by_year = students_by_birth_year(school)

fig3, ax3 = plt.subplots()

ax3.plot(
    list(by_year),
    list(by_year.values()),
    marker="o"
)

ax3.set_xlabel("Рік народження")
ax3.set_ylabel("Кількість учнів")

ax3.tick_params(
    axis="x",
    rotation=45
)

st.pyplot(fig3)
plt.close(fig3)


# ГРАФІК 4
# Scatter-графік оцінок учнів

st.subheader(
    "Графік 4. Середня оцінка кожного учня за класами"
)

classes = sorted_classes(school)

x_points: list[int] = []
y_points: list[float] = []

for index, school_class in enumerate(classes):

    for student in school_class.students:
        x_points.append(index)
        y_points.append(student.average_grade)


fig4, ax4 = plt.subplots(figsize=(11, 4))

ax4.scatter(
    x_points,
    y_points,
    alpha=0.65
)

ax4.set_xticks(range(len(classes)))

ax4.set_xticklabels(
    [c.name for c in classes],
    rotation=75
)

ax4.set_xlabel("Клас")
ax4.set_ylabel("Середня оцінка учня")
ax4.set_ylim(0, 12.5)

fig4.tight_layout()

st.pyplot(fig4)
plt.close(fig4)


# ПЕРЕВЕДЕННЯ КЛАСІВ

st.subheader(
    "Переведення на наступний навчальний рік"
)

if not st.session_state.promoted:

    if st.button(
        "Перевести всі класи",
        type="primary"
    ):
        st.session_state.graduated = (
            school.promote_all_classes()
        )

        st.session_state.promoted = True

        st.rerun()

else:
    st.success(
        f'Випускників зі старих 11-х класів: '
        f'{st.session_state.graduated}'
    )

    previous = st.session_state.before
    current = school_statistics(school)

    st.table(
        [
            {
                "Показник": key,
                "До": previous[key],
                "Після": current[key]
            }
            for key in previous
        ]
    )

    st.info(
        "Паралелі 1 більше немає. "
        "Колишні 11-ті класи випустилися, "
        "а 10-ті стали 11-ми."
    )


# Скидання даних

if st.button(
    "Почати заново (прочитати CSV ще раз)"
):

    for key in (
        "school",
        "before",
        "promoted",
        "graduated"
    ):
        del st.session_state[key]

    st.rerun()
