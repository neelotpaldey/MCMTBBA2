import streamlit as st
import pandas as pd

# -------------------------
# https://docs.google.com/spreadsheets/d/1-PZWQ4qddJag0_vb1dcvf9x29-rbFsnYhsdPsx6Hp6E/edit?usp=sharing
# -------------------------

SHEET_ID = "1-PZWQ4qddJag0_vb1dcvf9x29-rbFsnYhsdPsx6Hp6E"

sheet_urls = {
    "BBA":
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=BBA",

    "B.COM":
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet=B.COM",
}

st.set_page_config(page_title="PUT Result", layout="centered")

st.title("PUT EXAM RESULT 2026")

# -------------------------
# COURSE
# -------------------------

course = st.selectbox(
    "Course",
    list(sheet_urls.keys())
)

df = pd.read_csv(sheet_urls[course])

# Remove empty rows
df = df.dropna(subset=["NAME"])

# -------------------------
# STUDENT
# -------------------------

student = st.selectbox(
    "Student",
    df["NAME"].tolist()
)

row = df[df["NAME"] == student].iloc[0]

st.divider()

st.subheader("Student Details")

col1, col2 = st.columns(2)

with col1:
    st.write("**Name**")
    st.write(row["NAME"])

    st.write("**Admission No**")
    st.write(row["ADMISSION NO"])

with col2:
    st.write("**Father's Name**")
    st.write(row["FATHER'S NAME"])

st.divider()

st.subheader("Marks")

# Subject columns start after Father's Name
subject_columns = df.columns[4:]

marks = []

for subject in subject_columns:
    marks.append({
        "Subject": subject,
        "Marks": row[subject]
    })

marks_df = pd.DataFrame(marks)

st.table(marks_df)

st.divider()

if st.button("🖨 Print Result"):
    st.markdown(
        """
        <script>
        window.print();
        </script>
        """,
        unsafe_allow_html=True,
    )
