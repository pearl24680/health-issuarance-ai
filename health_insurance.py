import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os
from openai import OpenAI

matplotlib.use('Agg')
# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Health Insurance AI Pro", layout="centered")

# ---------- LOAD DATA ----------
df = pd.read_csv("https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv")

X = df[['age', 'bmi', 'children']]
y = df['charges']

model = LinearRegression()
model.fit(X, y)

# ---------- OPENAI ----------
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_advice(premium, age, bmi):
    prompt = f"""
    You are a smart health insurance advisor.

    Age: {age}
    BMI: {bmi}
    Premium: {premium}

    Give:
    - Risk level
    - Explanation
    - Tips to reduce premium
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

# ---------- UI ----------
st.title("💊 Health Insurance AI Pro")

st.markdown("### Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 60)

with col2:
    bmi = st.number_input("BMI", 10.0, 50.0)

children = st.number_input("Children", 0, 5)

# ---------- PREDICTION ----------
if st.button("🚀 Predict & Analyze"):
    pred = model.predict([[age, bmi, children]])[0]

    # Premium Card
    st.markdown("## 💰 Estimated Premium")
    st.success(f"₹ {round(pred, 2)}")

    # ---------- RISK SCORE ----------
    risk = (bmi * 2 + age) / 2

    st.markdown("## 🔥 Risk Score")
    st.progress(min(int(risk), 100))

    if risk < 30:
        st.success("Low Risk ✅")
    elif risk < 60:
        st.warning("Medium Risk ⚠️")
    else:
        st.error("High Risk 🚨")

    # ---------- GRAPH ----------
    st.markdown("## 📊 Age vs Charges Graph")

    fig, ax = plt.subplots()
    ax.scatter(df['age'], df['charges'])
    ax.set_xlabel("Age")
    ax.set_ylabel("Charges")

    st.pyplot(fig)

    # ---------- AI CHAT ----------
    st.markdown("## 🤖 AI Advisor")

    with st.spinner("AI is thinking..."):
        advice = get_ai_advice(pred, age, bmi)

    st.chat_message("assistant").write(advice)
