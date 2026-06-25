import streamlit as st
import pandas as pd
from urllib.parse import quote

# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="PUT EXAM RESULT 2026",
    page_icon="🎓",
    layout="centered"
)

# -------------------- GOOGLE SHEET --------------------

SHEET_ID = "1-PZWQ4qddJag0_vb1dcvf9x29-rbFsnYhsdPsx6Hp6E"

COURSES = {
    "BBA": "BBA 2ND.SEM",
    "B.COM": "B.COM 2ND.SEM"
}

# -------------------- LOAD DATA --------------------

@st.cache_data
def load_data(sheet_name):
    sheet_name = quote(sheet_name)

    url = (
        f"https://docs.google.com/spreadsheets/d/{SHEET_ID}"
        f"/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    )

    df = pd.read_csv(url)

    # Remove extra spaces from column names
    df.columns = df.columns.str.strip()

    # Remove empty rows
    df = df.dropna(subset=["NAME"])

    return df

# -------------------- TITLE --------------------

st.title("🎓 PUT EXAM RESULT 2026")

# -------------------- COURSE --------------------

course = st.selectbox(
    "Select Course",
    list(COURSES.keys())
)

try:
    df = load_data(COURSES[course])
except Exception:
    st.error("Unable to load Google Sheet.")
    st.info("Please make sure the sheet is shared as 'Anyone with the link → Viewer'.")
    st.stop()

# -------------------- STUDENT --------------------

student = st.selectbox(
    "Select Student",
    sorted(df["NAME"].astype(str).tolist())
)

row = df[df["NAME"] == student].iloc[0]

# -------------------- STUDENT DETAILS --------------------

st.divider()

st.subheader("Student Details")

c1, c2 = st.columns(2)

with c1:
    st.write("**Name**")
    st.write(row["NAME"])

    st.write("**Admission No**")
    st.write(row["ADMISSION NO"])

with c2:
    st.write("**Father's Name**")
    st.write(row["FATHER'S NAME"])

# -------------------- MARKS --------------------

st.divider()

st.subheader("Subject-wise Marks")

subjects = list(df.columns[4:])

marks = []

total = 0
count = 0

for subject in subjects:

    value = row[subject]

    if pd.isna(value):
        display = "-"

    elif str(value).strip().upper() == "AB":
        display = "Absent"

    else:
        try:
            num = float(value)
            total += num
            count += 1

            if num.is_integer():
                display = int(num)
            else:
                display = round(num, 2)

        except:
            display = value

    marks.append({
        "Subject": subject,
        "Marks": display
    })

marks_df = pd.DataFrame(marks)

st.table(marks_df)

# -------------------- RESULT --------------------

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.metric("Total Marks", int(total))

with c2:
    if count > 0:
        st.metric("Average", f"{total/count:.2f}")
    else:
        st.metric("Average", "0.00")

# -------------------- PRINT --------------------

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
