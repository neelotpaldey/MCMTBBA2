import streamlit as st
import pandas as pd

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="PUT Result 2026",
    page_icon="🎓",
    layout="centered"
)

SHEET_ID = "1-PZWQ4qddJag0_vb1dcvf9x29-rbFsnYhsdPsx6Hp6E"

# Sheet names exactly as in Google Sheet
COURSES = {
    "BBA": "BBA 2ND.SEM",
    "B.COM": "B.COM 2ND.SEM"
}

# ------------- LOAD DATA ----------------

@st.cache_data
def load_data(sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    df = pd.read_csv(url)
    df = df.dropna(subset=["NAME"])
    return df

# ---------------- HEADER ----------------

# Uncomment if banner available
# st.image("banner.png", use_container_width=True)

st.title("PUT EXAM RESULT 2026")

# ---------------- COURSE ----------------

course = st.selectbox(
    "Select Course",
    list(COURSES.keys())
)

df = load_data(COURSES[course])

# ---------------- STUDENT ----------------

student = st.selectbox(
    "Select Student",
    sorted(df["NAME"].tolist())
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

st.subheader("Subject-wise Marks")

subjects = df.columns[4:]

total = 0
count = 0

marks_table = []

for subject in subjects:

    mark = row[subject]

    if str(mark).strip().upper() == "AB":
        display = "AB"
    else:
        try:
            total += float(mark)
            count += 1
            display = int(mark)
        except:
            display = mark

    marks_table.append({
        "Subject": subject,
        "Marks": display
    })

marks_df = pd.DataFrame(marks_table)

st.dataframe(
    marks_df,
    use_container_width=True,
    hide_index=True
)

st.divider()

st.metric("Total Marks", total)

if count > 0:
    percentage = total / count
    st.metric("Average", f"{percentage:.2f}")

if st.button("🖨 Print Result"):
    st.markdown(
        """
        <script>
        window.print();
        </script>
        """,
        unsafe_allow_html=True
    )
