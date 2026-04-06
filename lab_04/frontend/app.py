import streamlit as st
import requests
import pandas as pd
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend-service:8000")

st.title("Трекер задач отдела аналитики")

st.header("Добавить новую задачу")

with st.form("task_form"):
    title = st.text_input("Заголовок")
    description = st.text_area("Описание")
    status = st.selectbox("Статус", ["в работе", "готово"])
    priority = st.selectbox("Приоритет", ["низкий", "средний", "высокий"])
    submitted = st.form_submit_button("Добавить задачу")

    if submitted:
        try:
            payload = {
                "title": title,
                "description": description,
                "status": status,
                "priority": priority
            }
            response = requests.post(f"{BACKEND_URL}/tasks", json=payload)

            if response.status_code == 200:
                st.success("Задача успешно добавлена")
            else:
                st.error("Ошибка при добавлении задачи")
        except Exception as e:
            st.error(f"Ошибка соединения с backend: {e}")

st.header("Список задач")

if st.button("Обновить данные"):
    try:
        response = requests.get(f"{BACKEND_URL}/tasks")
        if response.status_code == 200:
            data = response.json()
            if data:
                df = pd.DataFrame(data)
                st.dataframe(df)
            else:
                st.info("Пока задач нет")
        else:
            st.error("Не удалось получить данные")
    except Exception as e:
        st.error(f"Ошибка соединения с backend: {e}")
