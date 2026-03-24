import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import os
from openai import OpenAI

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Health Insurance AI Pro", layout="centered")

# ---------- LOAD MODEL (CACHED) ----------
@st.cache_resource
def load_model():
    df = pd.read_csv("https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv")
    
    X = df[['age', 'bmi', 'children']]
    y = df['charges']

    model = LinearRegression()
    model.fit(X, y)

    return model, df

model, df = load_model()

# ---------- AI FUNCTION ----------
def get_ai_advice(premium, age, bmi):
    try:
        api_key = os.getenv("OPENAI_API_KEY")

        # Agar API key nahi hai to crash nahi karega
        if not api_key:
            return "⚠️ AI disabled (API key not set in Streamlit Secrets)"

        client = OpenAI(api_key=api_key)

        prompt = f"""
        You are a Health Insurance Advisor.

        User Details:
        Age: {age}
        BMI: {bmi}
        Premium: {premium}

        Explain:
        - Risk level
        - Why premium is high/low
        - Tips to reduce premium
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception as e:
        return "⚠️ AI error (check API key or quota)"

# ---------- UI ----------
st.title("💊 Health Insurance AI Pro")

st.markdown("### Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 18, 60)

with col2:
    bmi = st.number_input("BMI", 10.0, 50.0)

children = st.number_input("Children", 0, 5)

# ---------- BUTTON ----------
if st.button("🚀 Predict & Analyze"):
    
    # Prediction
    pred = model.predict([[age, bmi, children]])[0]

    # Premium
    st.markdown("## 💰 Estimated Premium")
    st.success(f"₹ {round(pred, 2)}")

    # ---------- RISK ----------
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

    # ---------- AI ----------
    st.markdown("## 🤖 AI Advisor")

    with st.spinner("AI is analyzing..."):
        advice = get_ai_advice(pred, age, bmi)

    st.write(advice)
