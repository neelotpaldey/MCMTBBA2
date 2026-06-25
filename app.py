import streamlit as st
import pandas as pd
from urllib.parse import quote

# -------------------- CONFIG --------------------

st.set_page_config(
    page_title="PUT EXAM RESULT 2026",
    page_icon="🎓",
    layout="centered"
)

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
        f"https://docs.google.com/spreadsheets/d/"
        f"{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    )

    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    df = df.dropna(subset=["NAME"])

    return df


# -------------------- HEADER --------------------

st.title("PUT EXAM RESULT 2026")

# -------------------- COURSE --------------------

course = st.selectbox(
    "Select Course",
    list(COURSES.keys())
)

try:
    df = load_data(COURSES[course])

except Exception as e:
    st.error("Unable to read Google Sheet.")
    st.error(str(e))
    st.stop()

# -------------------- STUDENT --------------------

student = st.selectbox(
    "Select Student",
    sorted(df["NAME"].astype(str).tolist())
)

row = df[df["NAME"] == student].iloc[0]

# -------------------- DETAILS --------------------

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

subjects = df.columns[4:]

marks = []

total = 0

count = 0

for subject in subjects:

    value = row[subject]

    display = value

    if pd.isna(value):
        display = "-"

    elif str(value).strip().upper() == "AB":
        display = "AB"

    else:
        try:
            value = float(value)
            total += value
            count += 1

            if value.is_integer():
                display = int(value)
            else:
                display = value

        except:
            display = value

    marks.append(
        {
            "Subject": subject,
            "Marks": display
        }
    )

st.table(pd.DataFrame(marks))

# -------------------- RESULT --------------------

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.metric("Total Marks", total)

with c2:
    if count > 0:
        st.metric("Average", f"{total/count:.2f}")

# -------------------- PRINT --------------------

st.divider()

st.button("🖨 Print Result")

st.markdown(
    """
    <script>
    const btn = window.parent.document.querySelector('button[kind="secondary"]');
    if(btn){
        btn.onclick=function(){
            window.print();
        }
    }
    </script>
    """,
    unsafe_allow_html=True
)
