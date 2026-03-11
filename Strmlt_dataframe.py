import streamlit as st
import pandas as pd

#'''streamlit run Strmlt_dataframe.py --server.maxMessageSize 1000'''


Res_prod = ['10FG','10RM','10RP','10SA','66FG','66RM','66RP','66SA']
status = ['Active']

st.title("Part Listing Cost Analysis")
@st.cache_data
def get_un_data():
    data = pd.read_csv('TacoInc_PartListingWithCost1 - Copy.csv',low_memory=False)
    df = pd.DataFrame(data)

    # list_drop = [list(df.head())[i] if list(df.head())[i].startswith("Column") for i in range(len(df.columns))]
    # df.drop(columns=list_drop, inplace=True)
    df.fillna(0, inplace=True)
    df1 = df[df['ClassID'].isin(Res_prod) & df['PartActive'].isin(status)]
    df2 = df1[df1['PrevYR_Used']>0]
    return df2


df = get_un_data()
st.dataframe(df)

st.header("Figures", divider=True)
multi = '''Select the numeric parameter that you'd like to plot. Top items are plotted.'''

st.markdown(multi)

parameter = st.multiselect("Choose parameter", list(df.head()), ["PartCost_CurTotUnitCost_c", "PartCost_CurMtlUnitCost_c","PrevYR_Used"])

colors = ["#FF0000", "#0000FF","#00FF00","#FF0000", "#0000FF","#00FF00","#FF0000", "#0000FF","#00FF00","#FF0000",
          "#0000FF","#00FF00","#FF0000", "#0000FF","#00FF00","#FF0000", "#0000FF","#00FF00"]

Top = st.slider("How many parts?", 0, 30, 25)
st.markdown("---")
st.subheader(f"Top {Top} are shown:")

for i,item in enumerate(parameter):
    print(i,item)
    df1=df.sort_values(by=item, ascending=False).head(Top)#df.nlargest(n=20, columns=item) #df.sort_values(by=item, inplace=True, ascending=False)
    st.bar_chart(df1,x="PartNum",y=item, stack=None,color=colors[i])

st.markdown("---")
st.subheader(f"Bottom {Top} are shown:")
for i,item in enumerate(parameter):
    print(i,item)
    df1=df.sort_values(by=item, ascending=False).tail(Top)#df.nlargest(n=20, columns=item) #df.sort_values(by=item, inplace=True, ascending=False)
    st.bar_chart(df1,x="PartNum",y=item, stack=None,color=colors[i])


