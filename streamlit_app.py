import streamlit as st
import requests
import json

# Конфигурация Watson Orchestrate
ORCHESTRATE_API_KEY = "9BoWYXsiNAwF1V7ljv8nN5c8lxg7Dq4SFBy-8Axvc2jX"
ORCHESTRATE_URL = "https://api.us-south.watson-orchestrate.cloud.ibm.com/instances/21192705-1d5a-4bfe-b8f5-11699516e970"

st.set_page_config(page_title="HR Агент", page_icon="🤖", layout="centered")

# Заголовок
st.title("🤖 HR Агент")
st.markdown("Задайте любой вопрос HR агенту")

# Инициализация истории чата
if "messages" not in st.session_state:
    st.session_state.messages = []

# Отображение истории чата
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Функция для отправки запроса в Watson Orchestrate
def send_to_orchestrate(user_message):
    headers = {
        "Authorization": f"Bearer {ORCHESTRATE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input": {
            "text": user_message
        }
    }
    
    try:
        response = requests.post(
            f"{ORCHESTRATE_URL}/v1/messages",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result.get("output", {}).get("text", "Извините, не получил ответ")
        else:
            return f"Ошибка API: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Ошибка соединения: {str(e)}"

# Поле ввода сообщения
if prompt := st.chat_input("Напишите ваш вопрос..."):
    # Добавляем сообщение пользователя в историю
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Отображаем сообщение пользователя
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Получаем ответ от Watson Orchestrate
    with st.chat_message("assistant"):
        with st.spinner("Думаю..."):
            response = send_to_orchestrate(prompt)
            st.markdown(response)
    
    # Добавляем ответ ассистента в историю
    st.session_state.messages.append({"role": "assistant", "content": response})

# Кнопка очистки чата в сайдбаре
with st.sidebar:
    st.header("⚙️ Настройки")
    
    if st.button("🗑️ Очистить чат", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.markdown("""
    ### 📝 Информация
    
    **Подключено к:**
    - IBM Watson Orchestrate
    - Инстанс: watsonx-Hackathon
    
    **Примеры вопросов:**
    - Какие документы нужны для найма?
    - Как проходит онбординг?
    - Какой график отпусков?
    """)
    
    # Показываем количество сообщений
    st.caption(f"💬 Сообщений в чате: {len(st.session_state.messages)}")

# Футер
st.divider()
st.caption("🤖 HR Агент | Powered by IBM Watson Orchestrate")
