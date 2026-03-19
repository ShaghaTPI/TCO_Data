import altair
import streamlit as st
import pandas as pd
import altair as alt

#'''streamlit run Strmlt_dataframe.py --server.maxMessageSize 1000'''
main_path = 'C:\\Users\\ShaRez\\OneDrive - Taco Inc\\Desktop\\PyCharmMiscProject\\Data files\\'
tab1, tab2 = st.tabs(["📈 Data Analysis", "🗃 Cost Reduction"])

with tab1:


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
              "#24b41f","#1fb435","#1fb451", "#fffd80","#ff2b2b","#faca2b", "#0068c9","#3cff00"]

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
        st.bar_chart(df1,x="PartNum",y=item, stack=None,color=colors[-1-i])


# _________________________________________________________
import subprocess

with tab2:

    st.markdown("---")
    st.subheader(f"Cost Reduction Analysis:")

    parameter_cost = st.multiselect("Choose parameter", list(df.head()),
                               ["PartCost_CurTotUnitCost_c", "PartCost_CurMtlUnitCost_c"])

    parameter_qty = st.multiselect("Choose parameter", list(df.head()),
                               ["PrevYR_Used"],max_selections=1)
    price_range = st.slider(
        "Select a price range",
        min_value=0.0,
        max_value=500.0,
        value=(24.0, 27.0),  # Initial selected range
        step=1.0
    )
    st.write("Selected price range:", price_range[0], "to", price_range[1])

    qty_range = st.slider(
        "Select a quantity range",
        min_value=0,
        max_value=150000,
        value=(10000, 15000),  # Initial selected range
        step=1000
    )
    st.write("Selected Quantity range:", qty_range[0], "to", qty_range[1])
    for i,item in enumerate(parameter_cost):
        print(i,item)
        df1=df.sort_values(by=item, ascending=False)
        df2 = df1[df1[item].between(price_range[0],price_range[1])]#df.nlargest(n=20, columns=item) #df.sort_values(by=item, inplace=True, ascending=False)
        df3 = df2.sort_values(by=parameter_qty[0], ascending=False)
        df4 = df3[df3[parameter_qty[0]].between(qty_range[0],qty_range[1])]
        bars = (
            alt.Chart(df4)
            .mark_bar()
            .encode(
                x="PartNum",
                y=item,
                color=alt.Color('PrevYR_Used').scale(scheme='lightgreyred'),
                # color=colors[-1-i],
                text=alt.Text('PrevYR_Used', format='.1f'),
            )
        )
        text = alt.Chart(df4).mark_text(dx=20, dy=3, color='black',angle=270).encode(#bars.mark_text(baseline="middle").encode(#
            x="PartNum",
            y=item,
            # detail='site:N',
            text=alt.Text('PrevYR_Used', format='.1d'),)

        chart = alt.vconcat(bars+text, data=df4, title="Cost Reduction Analysis "+item)
        st.altair_chart(chart, theme="streamlit")#, use_container_width=True)

        ##_______________________________________
        subprocess.run(['python','Strmlt_DataPrep.py'])
