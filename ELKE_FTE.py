import streamlit as st
import pandas as pd
import numpy as np
import datetime
from io import BytesIO

st.title("ELKE FTE Analysis Tool")

st.write("Upload the required CSV files to compute FTE statistics.")

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

# Upload files
fte_file = st.file_uploader("Upload FTE File", type="csv")
research_file = st.file_uploader("Upload Research Projects File", type="csv")
industry_file = st.file_uploader("Upload Industry Projects File", type="csv")

if not any([fte_file, research_file, industry_file]):
    st.info("Please upload at least one file to continue.")
    st.stop()

# -----------------------
# Subject classification
# -----------------------

Subjects=[
'Arts and Humanities','Clinical and Health','Life Sciences',
'Engineering','Computer Science','Physical Sciences',
'Business','Education','Other','Total'
]

set_AH=['ΑΡΧΙΤΕΚΤΟΝΩΝ ΜΗΧΑΝΙΚΩΝ','ΦΙΛΟΛΟΓΙΑΣ','ΦΙΛΟΣΟΦΙΑΣ','ΔΙΑΧ/ΣΗΣ ΠΟΛΙΤΙΣΜΙΚΟΥ ΠΕΡ/ΝΤΟΣ & ΝΕΩΝ ΤΕ','ΙΣΤΟΡΙΑΣ - ΑΡΧΑΙΟΛΟΓΙΑΣ']
set_CH=['ΙΑΤΡΙΚΗΣ','ΛΟΓΟΘΕΡΑΠΕΙΑΣ','ΝΟΣΗΛΕΥΤΙΚΗΣ','ΦΑΡΜΑΚΕΥΤΙΚΗΣ','ΦΥΣΙΚΟΘΕΡΑΠΕΙΑΣ']
set_LS=['ΑΕΙΦΟΡΙΚΗΣ ΓΕΩΡΓΙΑΣ','ΑΛΙΕΙΑΣ ΚΑΙ ΥΔΑΤΟΚΑΛΛΙΕΡΓΕΙΩΝ','ΒΙΟΛΟΓΙΑΣ','ΓΕΩΠΟΝΙΑΣ','ΕΠΙΣΤΗΜΗΣ ΚΑΙ ΤΕΧΝΟΛΟΓΙΑΣ ΤΡΟΦΙΜΩΝ','ΖΩΙΚΗΣ ΠΑΡΑΓΩΓΗΣ ΑΛΙΕΙΑΣ ΚΑΙ ΥΔΑΤΟΚΑΛΛΙΕΡΓΕΙΩΝ','ΜΗΧΑΝΙΚΩΝ ΠΕΡΙΒΑΛΛΟΝΤΟΣ (ΔΙΑΧΕΙΡΙΣΗΣ ΠΕΡΙΒΑΛΛΟΝΤΟΣ ΚΑΙ ΦΥΣΙΚΩΝ ΠΟΡΩΝ)','ΒΙΟΛΟΓΙΑΣ']
set_EN=['ΗΛΕΚΤΡΟΛΟΓΩΝ ΜΗΧΑΝΙΚΩΝ ΚΑΙ ΤΕΧΝΟΛΟΓΙΑΣ ΥΠΟΛΟΓΙΣΤΩΝ','ΕΠΙΣΤΗΜΗΣ ΥΛΙΚΩΝ','ΜΗΧΑΝΟΛΟΓΩΝ ΚΑΙ ΑΕΡΟΝΑΥΠΗΓΩΝ ΜΗΧΑΝΙΚΩΝ','ΠΟΛΙΤΙΚΩΝ ΜΗΧΑΝΙΚΩΝ','ΧΗΜΙΚΩΝ ΜΗΧΑΝΙΚΩΝ']
set_CS=['ΜΗΧΑΝΙΚΩΝ ΗΛΕΚΤΡΟΝΙΚΩΝ ΥΠΟΛΟΓΙΣΤΩΝ ΚΑΙ ΠΛΗΡΟΦΟΡΙΚΗΣ']
set_PS=['ΓΕΩΛΟΓΙΑΣ','ΤΜΗΜΑ ΦΥΣΙΚΗΣ','ΦΥΣΙΚΗΣ','ΧΗΜΕΙΑΣ','ΜΑΘΗΜΑΤΙΚΟ']
set_BS=['ΟΙΚΟΝΟΜΙΚΩΝ ΕΠΙΣΤΗΜΩΝ','ΔΙΟΙΚΗΣΗΣ ΕΠΙΧΕΙΡΗΣΕΩΝ','ΔΙΟΙΚΗΤΙΚΗΣ ΕΠΙΣΤΗΜΗΣ ΚΑΙ ΤΕΧΝΟΛΟΓΙΑΣ']
set_ED=['ΕΠΙΣΤΗΜΩΝ ΤΗΣ ΕΚΠΑΙΔΕΥΣΗΣ ΚΑΙ ΚΟΙΝΩΝΙΚΗΣ ΕΡΓΑΣΙΑΣ','ΕΠΙΣΤΗΜΩΝ ΤΗΣ ΕΚΠΑΙΔΕΥΣΗΣ ΚΑΙ ΤΗΣ ΑΓΩΓΗΣ ΣΤΗΝ ΠΡΟΣΧΟΛΙΚΗ ΗΛΙΚΙΑ']
set_OTHER=['ΑΛΛΟ']

AH=[]; CH=[]; LS=[]; EN=[]; CS=[]; PS=[]; BS=[]; ED=[]; TOT=[]
AH_FTE=[]; CH_FTE=[]; LS_FTE=[]; EN_FTE=[]; CS_FTE=[]; PS_FTE=[]; BS_FTE=[]; ED_FTE=[]; TOT_FTE=[]

AH_Res=[]
CH_Res=[]
LS_Res=[]
EN_Res=[]
CS_Res=[]
PS_Res=[]
BS_Res=[]
ED_Res=[]
OTHER_Res=[]
AH_Ind=[]
CH_Ind=[]
LS_Ind=[]
EN_Ind=[]
CS_Ind=[]
PS_Ind=[]
BS_Ind=[]
ED_Ind=[]
TOT_Ind=[]

# Load data
database0 = pd.read_csv(fte_file, encoding="utf-8") if fte_file else None
database1 = pd.read_csv(research_file, encoding="utf-8") if research_file else None
database2 = pd.read_csv(industry_file, encoding="utf-8") if industry_file else None
if database0 is not None:
   df0 = pd.DataFrame(database0)
   data0 = np.array(df0)
   N0 = len(np.transpose(data0)[0])
   date_start = datetime.datetime(2023,9,1)
   date_end = datetime.datetime(2024,8,31)
   days=[]

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

if database1 is None:
    uu = np.zeros(10)

if database2 is None:
    vv = np.zeros(10)

if database1 is not None:
   df1=pd.DataFrame(database1)
   data1=np.array(df1)
   n1=len(data1[0])#Πλήθος κελιών
   N1=len(np.transpose(data1)[0])#Πλήθος έργων

if database2 is not None:
   df2=pd.DataFrame(database2)
   data2=np.array(df2)
   n2=len(data2[0])#Πλήθος κελιών
   N2=len(np.transpose(data2)[0])#Πλήθος έργων

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

   for i in range(N1):
   # df_start1=datetime.datetime.strptime(data1[i][4],"%m/%d/%Y")#Αν θέλουμε να "χωρίσουμε" ημερομηνίες
   # df_end1=datetime.datetime.strptime(data1[i][5],"%m/%d/%Y")#Αν θέλουμε να "χωρίσουμε" ημερομηνίες
   # x1=np.timedelta64(df_start1-date_start,"D").astype(int)#Αν θέλουμε να "χωρίσουμε" ημερομηνίες
   # y1=np.timedelta64(date_end-df_end1,"D").astype(int)#Αν θέλουμε να "χωρίσουμε" ημερομηνίες
   # tot1=np.timedelta64(df_end1-df_start1,"D").astype(int)#Αν θέλουμε να "χωρίσουμε" ημερομηνίες
   # check11=np.timedelta64(df_end1-date_start,"D").astype(int)#Αν θέλουμε να "χωρίσουμε" ημερομηνίες
   # check21=np.timedelta64(df_start1-date_end,"D").astype(int)#Αν θέλουμε να "χωρίσουμε" ημερομηνίες
    #if check11<0 or check21>0:#Αν θέλουμε να "χωρίσουμε" ημερομηνίες
    #    data1[i][2]=0#Αν θέλουμε να "χωρίσουμε" ημερομηνίες
    #else:#Αν θέλουμε να "χωρίσουμε" ημερομηνίες
        #Διαχωρίζει καθε συμβαλλόμενο στην σχολή του ως προς το FTE
       if data1[i][1] in set_AH:
           AH_Res.append(data1[i][2])
       if data1[i][1] in set_CH:
           CH_Res.append(data1[i][2])
       if data1[i][1] in set_LS:
           LS_Res.append(data1[i][2])
       if data1[i][1] in set_EN:
           EN_Res.append(data1[i][2])
       if data1[i][1] in set_CS:
           CS_Res.append(data1[i][2])
       if data1[i][1] in set_PS:
           PS_Res.append(data1[i][2])
       if data1[i][1] in set_BS:
           BS_Res.append(data1[i][2])
       if data1[i][1] in set_ED:
           ED_Res.append(data1[i][2])
       if data1[i][1] in set_OTHER:
           OTHER_Res.append(data1[i][2])
   for j in range(N2):
    #df_start2=datetime.datetime.strptime(data2[j][4],"%m/%d/%Y")
    #df_end2=datetime.datetime.strptime(data2[j][5],"%m/%d/%Y")
    #x2=np.timedelta64(df_start2-date_start,"D").astype(int)
    #y2=np.timedelta64(date_end-df_end2,"D").astype(int)
    #tot2=np.timedelta64(df_end2-df_start2,"D").astype(int)
    #check12=np.timedelta64(df_end2-date_start,"D").astype(int)
    #check22=np.timedelta64(df_start2-date_end,"D").astype(int)
    #if check12<0 or check22>0:
    #    data2[j][2]=0
    #else:
        #Διαχωρίζει καθε συμβαλλόμενο στην σχολή του ως προς το FTE
       TOT_Ind.append(data2[j][2])
       if data2[j][1] in set_AH:
           AH_Ind.append(data2[j][2])
       if data2[j][1] in set_CH:
           CH_Ind.append(data2[j][2])
       if data2[j][1] in set_LS:
           LS_Ind.append(data2[j][2])
       if data2[j][1] in set_EN:
           EN_Ind.append(data2[j][2])
       if data2[j][1] in set_CS:
           CS_Ind.append(data2[j][2])
       if data2[j][1] in set_PS:
           PS_Ind.append(data2[j][2])
       if data2[j][1] in set_BS:
           BS_Ind.append(data2[j][2])
       if data2[j][1] in set_ED:
           ED_Ind.append(data2[j][2])
    
   print(TOT_Ind)
   uu=np.zeros(10)
   vv=np.zeros(10)
   vv[0]=sum(AH_Ind)
   vv[1]=sum(CH_Ind)
   vv[2]=sum(LS_Ind)
   vv[3]=sum(EN_Ind)
   vv[4]=sum(CS_Ind)
   vv[5]=sum(PS_Ind)
   vv[6]=sum(BS_Ind)
   vv[7]=sum(ED_Ind)
   vv[8]=sum(TOT_Ind)
   vv[9]=sum(vv[:8])
   uu[0]=sum(AH_Res)
   uu[1]=sum(CH_Res)
   uu[2]=sum(LS_Res)
   uu[3]=sum(EN_Res)
   uu[4]=sum(CS_Res)
   uu[5]=sum(PS_Res)
   uu[6]=sum(BS_Res)
   uu[7]=sum(ED_Res)
   uu[8]=sum(OTHER_Res)
   uu[9]=sum(uu[:9])
#print(CH,CH.count(1),CH.count(0),len(CH))
   Income_Subjects={'Subjects':Subjects,'Income':[uu[0],uu[1],uu[2],uu[3],uu[4],uu[5],uu[6],uu[7],uu[8],uu[9]]}
   Industry_Subjects={'Subjects':Subjects,'Income':[vv[0],vv[1],vv[2],vv[3],vv[4],vv[5],vv[6],vv[7],vv[8],vv[9]]}

results=pd.DataFrame({
'Subjects':Subjects,
'FTE_QS':u,
'FTE_GRUP':v,
'FTE_SUM':w
})
df3=pd.DataFrame(Income_Subjects)
df4=pd.DataFrame(Industry_Subjects)
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
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    results.to_excel(writer, index=False, sheet_name="FTE Results")
    df3.to_excel(writer,sheet_name='Research Income',index=False)
    df4.to_excel(writer,sheet_name='Industry Income',index=False)
st.download_button(
    label="Download Results as Excel",
    data=buffer,
    file_name="THE_results.xlsx",
    mime="application/vnd.ms-excel"
)














