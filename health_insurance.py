import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os
from groq import Groq

# 🔑 ---------- ADD YOUR API KEY HERE ----------
os.environ["GROQ_API_KEY"] = "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"

# ---------- CONFIG ----------
st.set_page_config(page_title="Health Insurance AI Pro", layout="centered")

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    df = pd.read_csv("https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv")
    
    X = df[['age', 'bmi', 'children']]
    y = df['charges']

    model = LinearRegression()
    model.fit(X, y)

    return model, df

model, df = load_model()

# ---------- SESSION ----------
if "history" not in st.session_state:
    st.session_state.history = []

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------- AI ----------
def chat_with_ai(user_input):
    try:
        api_key = os.getenv("GROQ_API_KEY")
        client = Groq(api_key=api_key)

        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a health insurance advisor."},
                {"role": "user", "content": user_input}
            ]
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"⚠️ Error: {e}"

# ---------- UI ----------
st.title("💊 Health Insurance AI Pro")

st.markdown("### Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 60)

with col2:
    bmi = st.number_input("BMI", 10.0, 50.0)

children = st.number_input("Children", 0, 5)

# ---------- PREDICT ----------
if st.button("🚀 Predict & Analyze"):

    pred = model.predict([[age, bmi, children]])[0]

    risk_score = (bmi * 2 + age) / 2

    if risk_score < 30:
        risk_level = "Low"
    elif risk_score < 60:
        risk_level = "Medium"
    else:
        risk_level = "High"

    user_data = {
        "Age": age,
        "BMI": bmi,
        "Children": children,
        "Premium": round(pred, 2),
        "Risk": risk_level
    }

    st.session_state.history.append(user_data)

    st.success(f"💰 Premium: ₹{round(pred, 2)}")
    st.progress(min(int(risk_score), 100))
    st.write(f"🔥 Risk Level: {risk_level}")

    # Graph
    fig, ax = plt.subplots()
    ax.scatter(df['age'], df['charges'])
    ax.set_xlabel("Age")
    ax.set_ylabel("Charges")
    st.pyplot(fig)

# ---------- CHAT ----------
st.markdown("## 🤖 Chat with AI")

user_input = st.chat_input("Ask anything about insurance...")

if user_input:
    st.session_state.chat.append(("User", user_input))
    reply = chat_with_ai(user_input)
    st.session_state.chat.append(("AI", reply))

# Display chat
for role, msg in st.session_state.chat:
    if role == "User":
        st.chat_message("user").write(msg)
    else:
        st.chat_message("assistant").write(msg)

# ---------- HISTORY ----------
st.markdown("## 📜 Prediction History")
st.table(st.session_state.history)
