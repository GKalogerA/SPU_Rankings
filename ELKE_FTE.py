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

# Load data
database0 = pd.read_csv(fte_file, encoding="utf-8")
database1 = pd.read_csv(research_file, encoding="utf-8")
database2 = pd.read_csv(industry_file, encoding="utf-8")

df0 = pd.DataFrame(database0)
data0 = np.array(df0)

N0 = len(np.transpose(data0)[0])

date_start = datetime.datetime(2023,9,1)
date_end = datetime.datetime(2024,8,31)

days=[]

# -----------------------
# Functions
# -----------------------

def FTE_Count_QS(a):
    FT=a.count(1)
    PT=a.count(0)
    return FT+PT/3

def FTE_Count_GRUP(a,b):
    FT=a.count(1)
    PT=np.zeros(len(a))
    for i in range(len(a)):
        PT[i]=(1-a[i])*b[i]
    return FT+sum(PT)

def FTE_Count(a):
    if a>=0.75:
        return 1
    return 0

# -----------------------
# Main calculation
# -----------------------

for i in range(N0):

    df_start=datetime.datetime.strptime(data0[i][3],"%m/%d/%Y")
    df_end=datetime.datetime.strptime(data0[i][4],"%m/%d/%Y")

    x=np.timedelta64(df_start-date_start,"D").astype(int)
    y=np.timedelta64(date_end-df_end,"D").astype(int)
    tot=np.timedelta64(df_end-df_start,"D").astype(int)

    check1=np.timedelta64(df_end-date_start,"D").astype(int)
    check2=np.timedelta64(df_start-date_end,"D").astype(int)

    duration = 1 if data0[i][11] <= 12 else data0[i][11]/12

    if x>=0 and y<=0:
        day=(365-x)
    elif x>=0 and y>0:
        day=tot
    elif x<0 and y>0:
        day=np.timedelta64(df_end-date_start,"D").astype(int)
    elif x<0 and y<0:
        day=365
    elif check1<0 or check2>0:
        day=0

    data0[i][13]=data0[i][10]/(data0[i][9]*1720*duration)*(day/365)
    data0[i][15]=day
    data0[i][14]=FTE_Count(data0[i][13])

    days.append(tot)

# -----------------------
# Subject classification
# -----------------------

Subjects=[
'Arts and Humanities','Clinical and Health','Life Sciences',
'Engineering','Computer Science','Physical Sciences',
'Business','Education','Other','Total'
]

set_AH=['ΑΡΧΙΤΕΚΤΟΝΩΝ ΜΗΧΑΝΙΚΩΝ','ΦΙΛΟΛΟΓΙΑΣ','ΦΙΛΟΣΟΦΙΑΣ']
set_CH=['ΙΑΤΡΙΚΗΣ','ΛΟΓΟΘΕΡΑΠΕΙΑΣ','ΝΟΣΗΛΕΥΤΙΚΗΣ']
set_LS=['ΒΙΟΛΟΓΙΑΣ','ΓΕΩΠΟΝΙΑΣ']
set_EN=['ΗΛΕΚΤΡΟΛΟΓΩΝ ΜΗΧΑΝΙΚΩΝ','ΠΟΛΙΤΙΚΩΝ ΜΗΧΑΝΙΚΩΝ']
set_CS=['ΜΗΧΑΝΙΚΩΝ ΗΛΕΚΤΡΟΝΙΚΩΝ ΥΠΟΛΟΓΙΣΤΩΝ']
set_PS=['ΦΥΣΙΚΗΣ','ΧΗΜΕΙΑΣ']
set_BS=['ΟΙΚΟΝΟΜΙΚΩΝ ΕΠΙΣΤΗΜΩΝ']
set_ED=['ΕΠΙΣΤΗΜΩΝ ΤΗΣ ΕΚΠΑΙΔΕΥΣΗΣ']

AH=[]; CH=[]; LS=[]; EN=[]; CS=[]; PS=[]; BS=[]; ED=[]; TOT=[]
AH_FTE=[]; CH_FTE=[]; LS_FTE=[]; EN_FTE=[]; CS_FTE=[]; PS_FTE=[]; BS_FTE=[]; ED_FTE=[]; TOT_FTE=[]

for i in range(N0):

    if data0[i][7] in set_AH:
        AH.append(data0[i][14]); AH_FTE.append(data0[i][13])

    if data0[i][7] in set_CH:
        CH.append(data0[i][14]); CH_FTE.append(data0[i][13])

    if data0[i][7] in set_LS:
        LS.append(data0[i][14]); LS_FTE.append(data0[i][13])

    if data0[i][7] in set_EN:
        EN.append(data0[i][14]); EN_FTE.append(data0[i][13])

    if data0[i][7] in set_CS:
        CS.append(data0[i][14]); CS_FTE.append(data0[i][13])

    if data0[i][7] in set_PS:
        PS.append(data0[i][14]); PS_FTE.append(data0[i][13])

    if data0[i][7] in set_BS:
        BS.append(data0[i][14]); BS_FTE.append(data0[i][13])

    if data0[i][7] in set_ED:
        ED.append(data0[i][14]); ED_FTE.append(data0[i][13])

    TOT.append(data0[i][14])
    TOT_FTE.append(data0[i][13])

u=np.zeros(10)
v=np.zeros(10)
w=np.zeros(10)

w[0]=sum(AH_FTE)
w[1]=sum(CH_FTE)
w[2]=sum(LS_FTE)
w[3]=sum(EN_FTE)
w[4]=sum(CS_FTE)
w[5]=sum(PS_FTE)
w[6]=sum(BS_FTE)
w[7]=sum(ED_FTE)
w[8]=sum(TOT_FTE)
w[9]=sum(w[:8])

v[0]=FTE_Count_GRUP(AH,AH_FTE)
v[1]=FTE_Count_GRUP(CH,CH_FTE)
v[2]=FTE_Count_GRUP(LS,LS_FTE)
v[3]=FTE_Count_GRUP(EN,EN_FTE)
v[4]=FTE_Count_GRUP(CS,CS_FTE)
v[5]=FTE_Count_GRUP(PS,PS_FTE)
v[6]=FTE_Count_GRUP(BS,BS_FTE)
v[7]=FTE_Count_GRUP(ED,ED_FTE)
v[8]=FTE_Count_GRUP(TOT,TOT_FTE)
v[9]=sum(v[:8])

u[0]=FTE_Count_QS(AH)
u[1]=FTE_Count_QS(CH)
u[2]=FTE_Count_QS(LS)
u[3]=FTE_Count_QS(EN)
u[4]=FTE_Count_QS(CS)
u[5]=FTE_Count_QS(PS)
u[6]=FTE_Count_QS(BS)
u[7]=FTE_Count_QS(ED)
u[8]=FTE_Count_QS(TOT)
u[9]=sum(u[:8])

results=pd.DataFrame({
'Subjects':Subjects,
'FTE_QS':u,
'FTE_GRUP':v,
'FTE_SUM':w
})

# -----------------------
# Display Results
# -----------------------

st.subheader("FTE Results")
st.dataframe(results)

# -----------------------
# Download Excel
# -----------------------

buffer = BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    results.to_excel(writer, index=False, sheet_name="FTE Results")

st.download_button(
    label="Download Results as Excel",
    data=buffer,
    file_name="FTE_results.xlsx",
    mime="application/vnd.ms-excel"
)
