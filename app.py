import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import calendar

# page setup
st.set_page_config(layout='wide',page_title='Startup Analysis')
@st.cache_data
def data_loading():
    df=pd.read_csv('startup_funding_cleaned.csv',encoding='utf-8')
    df["startup"] = (
        df["startup"]
        .astype(str)
        .str.replace('"', '', regex=False)
        .str.replace("\\'", "'", regex=False)
        .str.replace("’", "'", regex=False)
        .str.strip()
    )
    sname=sorted(list(set(df['startup'].str.strip().unique())))
    iname=sorted(list(set((df['investor'].str.strip()).str.split(', ').sum()))) # sum here create a giant list of investors
    return df,sname,iname

df,sname,iname=data_loading() 

st.sidebar.title('Startup Funding Analysis')
selection=st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

def load_overall_analysis():
    st.title('Overall Analysis')
    col1,col2,col3,col4=st.columns(4)
    with col1:
        st.metric("Total",str(round(df['amount'].sum()))+" Cr")
    
    with col2:
        # which month is the peak month for investment
        months=['jan','feb','mar','apr','may','jun','jul','aug','sept','oct','nov','dec']
        df['date']=pd.to_datetime(df['date'])
        df['month']=df['date'].dt.month
        x=df.groupby(df['month'])['amount'].mean().sort_values(ascending=False).index[0]
        st.metric("Peak Month",str(months[x-1]))
    
    with col3:
        
        # max investment into a startup
        st.metric("Max funding any startup recieved ",df.groupby('startup')['amount'].sum().sort_values(ascending=False).head(1).values[0].round())
    with col4:
        # total funded startups
        st.metric("Total startups funded",df['startup'].nunique())
        
    # MoM chart, for every year
    df['year']=df['date'].dt.year
    new_df=df.groupby(['year','month'])['month'].sum()
    
    # --- 1. Get unique years and force them to integers to prevent type matching bugs ---
    try:
        unique_years = sorted(list(set(new_df.index.get_level_values('year'))))
        selected_year = st.selectbox("Select a Year", unique_years)
    except Exception as e:
        st.error(f"Error reading years from data: {e}")
        selected_year = None

    if selected_year is not None:
        # --- 2. Safe Data Extraction ---
        try:
            # Explicitly locate the selected year data
            year_data = new_df.loc[selected_year]
            # st.write(year_data)
            # year_data.columns=['month','amount']
            # Check if the resulting series actually has data
            if not year_data.empty:
                # 1. Convert Series to DataFrame and set column name
                df_plot = year_data.to_frame(name='Funding')
                
                # 2. Move month index into a regular column
                df_plot = df_plot.reset_index(names='Month')
                
                # 3. Display line chart
                st.line_chart(df_plot, x='Month', y='Funding')
            else:
                st.warning(f"No data available for the year {selected_year}.")
                
        except KeyError:
            st.error(f"Could not find data for year {selected_year} in the index.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            
def investor_details(selected_investor):
    # displaying last 5 investments
    filtered_df=df[df['investor'].str.split(', ').apply(lambda x: selected_investor in x)]
    
    st.subheader("Last 5 Investments : ")
    investments=filtered_df.sort_values(by='date',ascending=False).reset_index().head(5)[['date','startup','vertical','city','round','amount']]
    st.dataframe(investments,hide_index=True)
    
    # displaying top investments
    big_investments=filtered_df.groupby('startup')['amount'].sum().sort_values(ascending=False).head()
    st.subheader("Biggest Investments : ")
    col1,col2=st.columns(2)
    with col1:
        # graph
        
        x=np.array(big_investments.index)
        y=np.array(big_investments.values)
        
        fig, ax = plt.subplots()
        ax.bar(x, y, color='blue', label='Major Investments')
        ax.set_xlabel('Startups')
        ax.set_ylabel('Amount in CR')
        
        st.pyplot(fig)

        # table
        st.dataframe(big_investments)
        
    with col2:
        st.subheader('Sector-wise Analysis')
        sector=filtered_df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
        
        # graph
        
        x=np.array(sector.index)
        y=np.array(sector.values)
        
        fig, ax = plt.subplots()
        ax.pie(sector,labels=sector.index,autopct='%0.01f%%')
        
        st.pyplot(fig)

        # table
        st.dataframe(sector)
       
    # generlly invests in
    st.subheader('Generally Invests in : ')
    sorted_df=filtered_df.groupby('vertical')['amount'].sum().sort_values(ascending=False)
    top=sorted_df.values[0]
    st.dataframe(sorted_df[sorted_df>=(0.9*top)])
    
    col3, col4 = st.columns(2)

    # 1. Filter and group the data first so BOTH columns can use it
    investor_df = filtered_df
    rounds_data = investor_df.groupby('round')['round'].count()

    with col3:
        st.subheader('Rounds Data')
        # Pass the actual DataFrame/Series to st.dataframe
        st.dataframe(rounds_data)

    with col4:
        st.subheader('Rounds Chart')
        
        # 2. Check if data is empty to prevent Matplotlib errors
        if not rounds_data.empty:
            fig, ax = plt.subplots()

            # 3. Build the pie chart using the raw values and index
            ax.pie(
                rounds_data.values,        # Use .values for the sizes
                labels=rounds_data.index,   # Use .index for the labels
                autopct='%1.1f%%', 
                startangle=90
            )
            ax.axis('equal')  

            # 4. Display the figure
            st.pyplot(fig)
        else:
            st.write("No data available for this investor.")

    

if(selection=='Overall Analysis'):
    load_overall_analysis()  
    
elif(selection=='Startup'):
    start=st.sidebar.selectbox('Select Startup',sname)
    btn2=st.sidebar.button('Select')
    st.title(f"{start} Funding Analysis")
    
    # vertical & subvertical
    
    temp_df=df[df['startup'].str.contains(start)]
    col1,col2=st.columns(2)
    if btn2:
        with col1:
            ver=temp_df['vertical'].values[0]
            st.metric('Vertical',ver)
                
        with col2:
            subV=temp_df['subvertical'].dropna()
            if not subV.empty and str(subV.values[0]).strip()!='':
                st.metric('SubVertical',subV.values[0])
                
        # based
        if not temp_df['city'].empty:
            
            city=temp_df['city'].values[0]
            st.metric('City',city)
        
        else:
            st.metric('City','N/A')
            
        # last five investments in the startup
        st.write("Last seedings")
        st.dataframe(df[df['startup'].str.contains(start)].sort_values('date',ascending=False)[['date','amount']].head(5),hide_index=True)
else:
    selected_investor=st.sidebar.selectbox('Select Investor Name',iname)
    btn3=st.sidebar.button('Select')
    if btn3:
        st.title(f"{selected_investor} Investor Analysis")
        investor_details(selected_investor)
         