import streamlit as st
import pandas as pd
import numpy as np
import datetime
from io import BytesIO

st.title("ELKE FTE Analysis Tool")

st.write("Upload the required CSV files to compute FTE statistics.")

# Upload files
fte_file = st.file_uploader("Upload FTE File", type="csv")
research_file = st.file_uploader("Upload Research Projects File", type="csv")
industry_file = st.file_uploader("Upload Industry Projects File", type="csv")

if not all([fte_file, research_file, industry_file]):
    st.info("Please upload all three files to continue.")
    st.stop()

# -----------------------
# Load data
# -----------------------

database0 = pd.read_csv(fte_file, encoding="utf-8")
database1 = pd.read_csv(research_file, encoding="utf-8")
database2 = pd.read_csv(industry_file, encoding="utf-8")

df0 = pd.DataFrame(database0)
data0 = np.array(df0)

df1 = pd.DataFrame(database1)
data1 = np.array(df1)

df2 = pd.DataFrame(database2)
data2 = np.array(df2)

N0 = len(np.transpose(data0)[0])

n1 = len(data1[0])  # Πλήθος κελιών
N1 = len(np.transpose(data1)[0])  # Πλήθος έργων

n2 = len(data2[0])  # Πλήθος κελιών
N2 = len(np.transpose(data2)[0])  # Πλήθος έργων

date_start = datetime.datetime(2023, 9, 1)
date_end = datetime.datetime(2024, 8, 31)

days = []

# -----------------------
# Functions
# -----------------------

def FTE_Count_QS(a):
    FT = a.count(1)
    PT = a.count(0)
    return FT + PT / 3


def FTE_Count_GRUP(a, b):
    FT = a.count(1)
    PT = np.zeros(len(a))
    for i in range(len(a)):
        PT[i] = (1 - a[i]) * b[i]
    return FT + sum(PT)


def FTE_Count(a):
    if a >= 0.75:
        return 1
    return 0


# -----------------------
# Main calculation
# -----------------------

for i in range(N0):

    df_start = datetime.datetime.strptime(data0[i][3], "%m/%d/%Y")
    df_end = datetime.datetime.strptime(data0[i][4], "%m/%d/%Y")

    x = np.timedelta64(df_start - date_start, "D").astype(int)
    y = np.timedelta64(date_end - df_end, "D").astype(int)
    tot = np.timedelta64(df_end - df_start, "D").astype(int)

    check1 = np.timedelta64(df_end - date_start, "D").astype(int)
    check2 = np.timedelta64(df_start - date_end, "D").astype(int)

    duration = 1 if data0[i][11] <= 12 else data0[i][11] / 12

    if x >= 0 and y <= 0:
        day = (365 - x)
    elif x >= 0 and y > 0:
        day = tot
    elif x < 0 and y > 0:
        day = np.timedelta64(df_end - date_start, "D").astype(int)
    elif x < 0 and y < 0:
        day = 365
    elif check1 < 0 or check2 > 0:
        day = 0

    data0[i][13] = data0[i][10] / (data0[i][9] * 1720 * duration) * (day / 365)
    data0[i][15] = day
    data0[i][14] = FTE_Count(data0[i][13])

    days.append(tot)

# -----------------------
# Subject classification
# -----------------------

Subjects = [
    "Arts and Humanities",
    "Clinical and Health",
    "Life Sciences",
    "Engineering",
    "Computer Science",
    "Physical Sciences",
    "Business",
    "Education",
    "Other",
    "Total",
]

set_AH = [
    "ΑΡΧΙΤΕΚΤΟΝΩΝ ΜΗΧΑΝΙΚΩΝ",
    "ΦΙΛΟΛΟΓΙΑΣ",
    "ΦΙΛΟΣΟΦΙΑΣ",
    "ΔΙΑΧ/ΣΗΣ ΠΟΛΙΤΙΣΜΙΚΟΥ ΠΕΡ/ΝΤΟΣ & ΝΕΩΝ ΤΕ",
    "ΙΣΤΟΡΙΑΣ - ΑΡΧΑΙΟΛΟΓΙΑΣ",
]

set_CH = ["ΙΑΤΡΙΚΗΣ", "ΛΟΓΟΘΕΡΑΠΕΙΑΣ", "ΝΟΣΗΛΕΥΤΙΚΗΣ", "ΦΑΡΜΑΚΕΥΤΙΚΗΣ", "ΦΥΣΙΚΟΘΕΡΑΠΕΙΑΣ"]

set_LS = [
    "ΑΕΙΦΟΡΙΚΗΣ ΓΕΩΡΓΙΑΣ",
    "ΑΛΙΕΙΑΣ ΚΑΙ ΥΔΑΤΟΚΑΛΛΙΕΡΓΕΙΩΝ",
    "ΒΙΟΛΟΓΙΑΣ",
    "ΓΕΩΠΟΝΙΑΣ",
    "ΕΠΙΣΤΗΜΗΣ ΚΑΙ ΤΕΧΝΟΛΟΓΙΑΣ ΤΡΟΦΙΜΩΝ",
    "ΖΩΙΚΗΣ ΠΑΡΑΓΩΓΗΣ ΑΛΙΕΙΑΣ ΚΑΙ ΥΔΑΤΟΚΑΛΛΙΕΡΓΕΙΩΝ",
    "ΜΗΧΑΝΙΚΩΝ ΠΕΡΙΒΑΛΛΟΝΤΟΣ (ΔΙΑΧΕΙΡΙΣΗΣ ΠΕΡΙΒΑΛΛΟΝΤΟΣ ΚΑΙ ΦΥΣΙΚΩΝ ΠΟΡΩΝ)",
    "ΒΙΟΛΟΓΙΑΣ",
]

set_EN = [
    "ΗΛΕΚΤΡΟΛΟΓΩΝ ΜΗΧΑΝΙΚΩΝ ΚΑΙ ΤΕΧΝΟΛΟΓΙΑΣ ΥΠΟΛΟΓΙΣΤΩΝ",
    "ΕΠΙΣΤΗΜΗΣ ΥΛΙΚΩΝ",
    "ΜΗΧΑΝΟΛΟΓΩΝ ΚΑΙ ΑΕΡΟΝΑΥΠΗΓΩΝ ΜΗΧΑΝΙΚΩΝ",
    "ΠΟΛΙΤΙΚΩΝ ΜΗΧΑΝΙΚΩΝ",
    "ΧΗΜΙΚΩΝ ΜΗΧΑΝΙΚΩΝ",
]

set_CS = ["ΜΗΧΑΝΙΚΩΝ ΗΛΕΚΤΡΟΝΙΚΩΝ ΥΠΟΛΟΓΙΣΤΩΝ ΚΑΙ ΠΛΗΡΟΦΟΡΙΚΗΣ"]

set_PS = ["ΓΕΩΛΟΓΙΑΣ", "ΤΜΗΜΑ ΦΥΣΙΚΗΣ", "ΦΥΣΙΚΗΣ", "ΧΗΜΕΙΑΣ", "ΜΑΘΗΜΑΤΙΚΟ"]

set_BS = [
    "ΟΙΚΟΝΟΜΙΚΩΝ ΕΠΙΣΤΗΜΩΝ",
    "ΔΙΟΙΚΗΣΗΣ ΕΠΙΧΕΙΡΗΣΕΩΝ",
    "ΔΙΟΙΚΗΤΙΚΗΣ ΕΠΙΣΤΗΜΗΣ ΚΑΙ ΤΕΧΝΟΛΟΓΙΑΣ",
]

set_ED = [
    "ΕΠΙΣΤΗΜΩΝ ΤΗΣ ΕΚΠΑΙΔΕΥΣΗΣ ΚΑΙ ΚΟΙΝΩΝΙΚΗΣ ΕΡΓΑΣΙΑΣ",
    "ΕΠΙΣΤΗΜΩΝ ΤΗΣ ΕΚΠΑΙΔΕΥΣΗΣ ΚΑΙ ΤΗΣ ΑΓΩΓΗΣ ΣΤΗΝ ΠΡΟΣΧΟΛΙΚΗ ΗΛΙΚΙΑ",
]

set_OTHER = ["ΑΛΛΟ"]

# (rest of your code continues exactly the same...)

# -----------------------
# Display Results
# -----------------------

st.subheader("THE Results")
st.dataframe(results)
st.dataframe(df3)
st.dataframe(df4)

# -----------------------
# Download Excel
# -----------------------

buffer = BytesIO()

with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
    results.to_excel(writer, index=False, sheet_name="FTE Results")
    df3.to_excel(writer, sheet_name="Research Income", index=False)
    df4.to_excel(writer, sheet_name="Industry Income", index=False)

st.download_button(
    label="Download Results as Excel",
    data=buffer,
    file_name="THE_results.xlsx",
    mime="application/vnd.ms-excel",
)
