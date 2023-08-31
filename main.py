#!/usr/bin/env python
# coding: utf-8

# In[31]:


#IMPORTING REQUIRED LIBRARIES
import streamlit as st
import pandas as pd
import mysql.connector as mysql
import plotly.express as px
from PIL import Image


st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   layout= "wide",
                   initial_sidebar_state= "expanded",)

#CONNECTING TO SQL
mydb=mysql.connect(
      host="localhost",
      user="root",
      password="Positive011205?",
      database="phonepe")
mycursor=mydb.cursor(buffered=True)

#CREATING TABS 
tab1,tab2,tab3=st.tabs([":orange[Home]",":orange[TopCharts]",":orange[Insights]"])

with tab1:
    st.markdown("## Phonepe Pulse Data Visualization and Exploration")
    col1,col2=st.columns([1.5,1],gap="medium")
    with col1:
        st.markdown("## Technologies Used:")
        st.write(" **-->Github Cloning**")
        st.write(" **-->Python**")
        st.write(" **-->Pandas**")
        st.write(" **-->MySql**")
        st.write(" **-->Mysql-connector-python**")
        st.write(" **-->Streamlit**")
        st.write(" **-->Plotly**")
        st.write('''## :red[Go] :orange[to] :green[Top charts] :blue[and] :violet[Insights] :green[tabs] :violet[to] :orange[visualize] :red[Data]''')
    with col2:
        image = Image.open("C:\\Users\\aditi\\Downloads\\phonepe.png")
        st.image(image,use_column_width=True)
with tab2:
    st.info(
                """
                #### Lets see the Top Charts :
                - Top 10  based on Total number of transaction and Total amount spent on PhonePe
                  On each district,Pincode and state
                - Top 10 based on Total PhonePe users and their app opening frequency.
                - Top 10 based on how many people use PhonePe.
                - Use slider to get data for each year.
                - No data for year 2023 Quarter 2,3 and 4
                """,icon="ℹ️"
         )
    st.markdown("## :red[Top Charts]")
    colum1,colum2= st.columns([1.5,1],gap="small")
    with colum2:
        Year = st.slider("**Year**", min_value=2018, max_value=2023,key="1")
        st.divider()
        Quarter = st.slider("Quarter", min_value=1, max_value=4,key="2")
        st.divider()
    
    with colum1:
        Type = st.selectbox("**Type**", ("Transactions", "Users"),key="7")
    if Type == "Transactions":
        col1,col2 = st.columns([1,1],gap="medium")
        
        with col1:
            st.markdown("### :orange[State]")
            mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_trans where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
            fig = px.bar(df, x='Total_Amount',
                             y='State',
                             title='Top 10',
                             orientation="h",
                             color="Transactions_Count",
                             color_discrete_sequence=px.colors.sequential.RdBu,
                             )

            
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :orange[District]")
            mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_trans where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

            fig = px.bar(df, x='Total_Amount',
                             y='District',
                             title='Top 10',
                             orientation="h",
                             color='Transactions_Count',
                             color_discrete_sequence=px.colors.sequential.RdBu,
                             )

          
            st.plotly_chart(fig,use_container_width=True)          
       
        st.markdown("### :orange[Pincode]")
        mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_trans where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
        fig = px.bar(df, x='Total_Amount',
                             y='Pincode',
                             title='Top 10',
                             color="Transactions_Count",
                             orientation='h',
                             color_discrete_sequence=px.colors.sequential.RdBu,
                             )

            
        st.plotly_chart(fig)
# Top Charts - USERS          
    if Type == "Users":
        col1,col2 = st.columns([2,2],gap="small")
        
        with col1:
            st.markdown("### :orange[Brands]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2022 Qtr 2,3,4")
            else:
                mycursor.execute(f"select brands, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brands order by Total_Count limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.RdBu)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :orange[District]")
            mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                         title='Top 10',
                         x="Total_Users",
                         y="District",
                         orientation='h',
                         color='Total_Users',
                         color_continuous_scale=px.colors.sequential.RdBu)
            st.plotly_chart(fig,use_container_width=True)
        col3,col4 = st.columns([2,2],gap="small")
              
        with col3:
            st.markdown("### :orange[Pincode]")
            mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
            fig = px.pie(df,
                         values='Total_Users',
                         names='Pincode',
                         title='Top 10',
                         color_discrete_sequence=px.colors.sequential.RdBu,
                         hover_data=['Total_Users'])
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :orange[State]")
            mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                             names='State',
                             title='Top 10',
                             color_discrete_sequence=px.colors.sequential.RdBu,
                             hover_data=['Total_Appopens'],
                             labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
with tab3:
    col1,col2=st.columns(2)
    st.info("No data info for year 2023 and Quarter 2, 3 and 4")
    with col1:
        Year1 = st.slider("**Year**", min_value=2018, max_value=2023,key="3")
        Quarter1 = st.slider("Quarter", min_value=1, max_value=4,key="4")
    with col2:
        Type1 = st.selectbox("**Type**", ("Transactions", "Users"),key="5")
  
    if Type1 == "Transactions":
        
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
     
        st.markdown("## :red[Overall State Data - Transactions Amount]")
        mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year1} and quarter = {Quarter1} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        s=["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh",
           "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir",
           "Jharkhand","Karnataka","Kerala","Ladakh",
            "Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya",
            "Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu",
            "Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"]
        df2 = pd.DataFrame(s)
        df1.State = df2

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                      featureidkey='properties.ST_NM',
                      locations='State',
                      color='Total_amount',
                      basemap_visible=True,
                      color_continuous_scale='Rainbow',
                      template="plotly_dark")

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
            
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
     
            
        st.markdown("## :red[Overall State Data - Transactions Count]")
        mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year1} and quarter = {Quarter1} group by state order by state")
        df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
        s=["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh",
            "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir",
            "Jharkhand","Karnataka","Kerala","Ladakh",
            "Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya",
            "Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu",
            "Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"]
        df2 = pd.DataFrame(s)
        df1.Total_Transactions = df1.Total_Transactions.astype(int)
        df1.State = df2

        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Transactions',
                    color_continuous_scale='plasma',
                    basemap_visible=True,
                    template="plotly_dark")

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)
            
# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :red[Top Payment Type]")
        mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_trans where year= {Year1} and quarter = {Quarter1} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                     title='Transaction Types vs Total_Transactions',
                     x="Transaction_type",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.Jet)
        st.plotly_chart(fig,use_container_width=False)
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
         
        mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_trans where year = {Year1} and quarter = {Quarter1} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
        
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                         'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                     title=selected_state,
                     x="District",
                     y="Total_Transactions",
                     orientation='v',
                     color='Total_amount',
                     color_continuous_scale=px.colors.sequential.thermal)
        st.plotly_chart(fig,use_container_width=True)
        
# EXPLORE DATA - USERS      
    if Type1 == "Users":
        if Year1 == 2023 and Quarter1 in [2,3,4]:
                st.markdown("#### Sorry No Data to Display for 2023 Qtr 2,3,4")
        
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        else:
            st.markdown("## :red[Overall State Data - User App opening frequenacy]")
            mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year1} and quarter = {Quarter1} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            s=["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh",
               "Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himachal Pradesh","Jammu & Kashmir",
               "Jharkhand","Karnataka","Kerala","Ladakh",
               "Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya",
               "Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu",
               "Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"]
            df2 = pd.DataFrame(s)
            df1.Total_Appopens = df1.Total_Appopens.astype(float)
            df1.State = df2
        
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                  featureidkey='properties.ST_NM',
                  locations='State',
                  color='Total_Appopens',
                  color_continuous_scale='spectral',
                  template="plotly_dark",
                  basemap_visible=True)

            
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
        
        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
            st.markdown("## :red[Select State]")
            selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
            mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year1} and quarter = {Quarter1} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
        
            df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(int)
        
            fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
        
    
    


# In[ ]:















