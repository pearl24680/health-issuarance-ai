import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os
from openai import OpenAI

# Load dataset and train model (only once)
df = pd.read_csv("https://raw.githubusercontent.com/stedy/Machine-Learning-with-R-datasets/master/insurance.csv")

X = df[['age', 'bmi', 'children']]
y = df['charges']

model = LinearRegression()
model.fit(X, y)

# OpenAI API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_ai_advice(premium):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"My insurance premium is {premium}. Explain why and how to reduce it."}
        ]
    )
    return response.choices[0].message.content

# UI
st.title("💊 Health Insurance AI Advisor")

age = st.slider("Age", 18, 60)
bmi = st.number_input("BMI", 10.0, 50.0)
children = st.number_input("Children", 0, 5)

if st.button("Predict"):
    pred = model.predict([[age, bmi, children]])[0]

    st.success(f"💰 Estimated Premium: ₹{round(pred, 2)}")

    with st.spinner("AI is thinking..."):
        advice = get_ai_advice(pred)

    st.write("🤖 AI Advice:")
    st.write(advice)
