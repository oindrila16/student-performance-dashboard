import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO

df = pd.read_csv("dataset.csv")

st.title("Student Performance Dashboard")
st.markdown("Analyze student marks with interactive visuals")

#KPI CARDS
avg_math = df["Math"].mean()
max_math = df["Math"].max()
min_math = df["Math"].min()

st.subheader("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Average Math", round(avg_math, 2))
col2.metric("Max Math", max_math)
col3.metric("Min Math", min_math)

#Average marks per student
df["Average"] = df[["Math", "Physics", "Chemistry"]].mean(axis=1)

fig = px.bar(df, x="Name", y="Average", color="Gender", title="Average Score by Student")

st.plotly_chart(fig)


#Pie Chart
gender_count = df["Gender"].value_counts().reset_index()
gender_count.columns = ["Gender", "Count"]

fig2 = px.pie(gender_count, names="Gender", values="Count", title="Gender Distribution")

st.plotly_chart(fig2)


#Subject-wise Performance
subject_avg = df[["Math", "Physics", "Chemistry"]].mean().reset_index()
subject_avg.columns = ["Subject", "Average"]

fig3 = px.bar(subject_avg, x="Subject", y="Average", title="Average Marks per Subject")

st.plotly_chart(fig3)


#FILTER
gender_filter = st.selectbox("Select Gender", ["All", "M", "F"])

if gender_filter != "All":
    filtered_df = df[df["Gender"] == gender_filter]
else:
    filtered_df = df

st.write(filtered_df)


#LOGIN
def login():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "admin":
            st.session_state["logged_in"] = True
        else:
            st.error("Invalid credentials")

if "logged_in" not in st.session_state:
    login()
    st.stop()


#LOAD DATA
df = pd.read_csv("dataset.csv")
df["Average"] = df[["Math", "Physics", "Chemistry"]].mean(axis=1)


#CSV Download
csv = df.to_csv(index=False)

st.download_button(
    label="Download CSV Report",
    data=csv,
    file_name="student_report.csv",
    mime="text/csv"
)


#PDF Download
from fpdf import FPDF

def generate_pdf(dataframe):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=10)

    for i, row in dataframe.iterrows():
        line = f"{row['Name']} | Avg: {row['Average']}"
        pdf.cell(200, 10, txt=line, ln=True)

    return pdf.output(dest="S").encode("latin-1")

pdf_data = generate_pdf(df)

st.download_button(
    label="Download PDF Report",
    data=pdf_data,
    file_name="report.pdf",
    mime="application/pdf"
)



#CORRELATION HEATMAP
st.subheader("Correlation Heatmap")

corr = df[["Math", "Physics", "Chemistry", "Average"]].corr()

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig)



#SCORE PREDICTION
X = df[["Math", "Physics", "Chemistry"]]
y = df["Average"]

model = LinearRegression()
model.fit(X, y)


st.subheader("Predict Student Score")

math = st.number_input("Math Score", 0, 100, 50)
physics = st.number_input("Physics Score", 0, 100, 50)
chemistry = st.number_input("Chemistry Score", 0, 100, 50)

if st.button("Predict"):
    prediction = model.predict([[math, physics, chemistry]])
    st.success(f"Predicted Average Score: {prediction[0]:.2f}")