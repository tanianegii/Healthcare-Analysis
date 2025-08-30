import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

with st.sidebar:
    opt=option_menu("Menu",["Home","Graphs","About"],icons=["house","bar-chart","people"],menu_icon="cast",default_index=0)

if opt == "Home":
    # Title and Subtitle
    st.title("Welcome to the Global Health Analysis Dashboard")
    st.subheader("Exploring Chronic Diseases: Diabetes and Heart Disease")
    
    # Introduction Section
    st.write("""
    Chronic diseases such as diabetes and heart disease are among the leading causes of morbidity and mortality worldwide.
    This dashboard aims to provide insights into the prevalence, trends, and risk factors associated with these diseases,
    empowering data-driven strategies for better public health outcomes.
    """)
    
    # Objectives Section
    st.markdown("---")
    st.header("Objectives")
    st.write("""
    The key objectives of this dashboard are:
    1. **Analyze Trends:** Understand the prevalence of diabetes and heart disease over time.
    2. **Identify Risk Factors:** Highlight correlations between demographic and lifestyle factors and disease risks.
    3. **Visualize Data:** Present interactive visualizations for a global understanding of disease impacts.
    """)

    # Images Section (Add relevant images to enhance visuals)
    col1, col2 = st.columns(2)
    with col1:
        st.image("global.jpg", caption="Global Disease Trends", use_column_width=True)
    with col2:
        st.image("Virus-close-up.jpg", caption="Chronic Disease Impact", use_column_width=True)

elif opt=="Graphs":
    
    a=st.sidebar.selectbox("Select Continents",options=["Globe","Asian","African","American","European"])
    
    if a=="Globe": 

       data=pd.read_csv("globe.csv")
       data.drop(columns=['Unnamed: 0'],inplace=True)
       data

       year = st.selectbox('Select Year for Comparison', data['Year'].unique())
       filtered_data = data[data['Year'] == year]

    # Select the columns for causes of death
       causes_of_death = [
                'Meningitis',
                "Alzheimer's Disease and Other Dementias", "Parkinson's Disease",
                'Nutritional Deficiencies', 'Malaria', 'Drowning', 'Maternal Disorders',
                'HIV/AIDS', 'Tuberculosis', 'Cardiovascular Diseases',
                'Lower Respiratory Infections', 'Neonatal Disorders',
                'Diarrheal Diseases', 'Neoplasms', 'Diabetes Mellitus',
                'Chronic Kidney Disease', 'Protein-Energy Malnutrition',
                'Chronic Respiratory Diseases',
                'Cirrhosis and Other Chronic Liver Diseases', 'Digestive Diseases'
            ]

    # Aggregate data for the selected year
       deaths_by_cause = filtered_data[causes_of_death].sum().reset_index()
       deaths_by_cause.columns = ['Cause of Death', 'Number of Deaths']
       fig = px.bar(deaths_by_cause,
                        x='Cause of Death',
                        y='Number of Deaths',
                        title=f'Number of Deaths by Cause in {year}',
                        labels={'Number of Deaths':'Number of Deaths', 'Cause of Death':'Cause of Death'},
                        text='Number of Deaths')

     # Customize layout for better appearance
       fig.update_layout(xaxis_tickangle=-45)
       st.plotly_chart(fig)
   
    # Sidebar for user input
       st.sidebar.header("Options")
       diseases = data.columns[4:]  # Disease columns start from the 5th column
       selected_disease = st.sidebar.selectbox("Select a Disease", diseases)

       year = st.sidebar.slider("Select Year", 
                                min_value=int(data["Year"].min()), 
                                max_value=int(data["Year"].max()), 
                                step=1)

        # Filter data for the selected year
       filtered_data = data[data["Year"] == year]

        # Plot choropleth map
       fig = px.choropleth(
            filtered_data,
            locations="Country/Territory",
            locationmode="country names",
            color=selected_disease,
            hover_name="Country/Territory",
            color_continuous_scale=px.colors.sequential.Plasma,
            title=f"{selected_disease} Deaths in {year}"
        )

        # Display the chart
       st.plotly_chart(fig)


            
    elif a=="Asian":
        data=pd.read_csv("asia.csv")
        data.drop(columns=['Unnamed: 0'],inplace=True)
        st.title("Dataset of Asia")
        st.dataframe(data)
        
        #line graph
        country = st.selectbox('Select Country', data['Country/Territory'].unique())
        filtered_data = data[data['Country/Territory'] == country]
        disease = st.selectbox('Select Disease for Trend Analysis', filtered_data.columns[4:])
        fig_trend = px.line(filtered_data, x='Year', y=disease, title=f'Trend of {disease} in {country} from 1990 to 2019')
        st.plotly_chart(fig_trend)

         # bar chart
        year = st.selectbox('Select Year for Comparison', filtered_data['Year'].unique())
        st.subheader(f"Disease Comparison in {country} in {year}")
        data_year = filtered_data[filtered_data['Year'] == year].melt(id_vars=['Country/Territory', 'Code', 'Year'], var_name='Disease', value_name='Count')
        # st.write(data_year)
        fig_comparison = px.bar(data_year, x='Disease', y='Count', title=f'Disease Comparison in {country} in {year}')
        st.plotly_chart(fig_comparison)

        #multiple selected disease heat map
        diseases = data.columns.difference(['Year', 'Country/Territory', 'Code'])
        selected_diseases = st.sidebar.multiselect(
            'Select Diseases',
            options=diseases,default=['Diarrheal Diseases','Cirrhosis and Other Chronic Liver Diseases','Drowning',
                                        'HIV/AIDS','Lower Respiratory Infections']
        )
        filtered_data = data[['Year'] + selected_diseases]
        # st.write(filtered_data)
        heatmap_data = filtered_data.set_index('Year')

        st.subheader('Heatmap of Disease Counts Over the Years')
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data.T,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Viridis'
        ))
        fig_heatmap.update_layout(title='Disease Counts Heatmap')
        st.plotly_chart(fig_heatmap)

        
            
    elif a =='African':
        data =  pd.read_csv('african.csv')
        data.drop(columns=['Unnamed: 0'],inplace=True)
        data
        # line Chart
        country = st.selectbox('Select Country', data['Country/Territory'].unique())
        filtered_data = data[data['Country/Territory'] == country]
        disease = st.selectbox('Select Disease for Trend Analysis', filtered_data.columns[4:])
        # st.write(filtered_data)
        fig_trend = px.line(filtered_data, x='Year', y=disease, title=f'Trend of {disease} in {country} from 1990 to 2019')
        st.plotly_chart(fig_trend)

        # bar chart
        year = st.selectbox('Select Year for Comparison', filtered_data['Year'].unique())
        st.subheader(f"Disease Comparison in {country} in {year}")
        data_year = filtered_data[filtered_data['Year'] == year].melt(id_vars=['Country/Territory', 'Code', 'Year'], var_name='Disease', value_name='Count')
        # st.write(data_year)
        fig_comparison = px.bar(data_year, x='Disease', y='Count', title=f'Disease Comparison in {country} in {year}')
        st.plotly_chart(fig_comparison)
        
        # Pie Chart
        st.subheader(f'Disease Distribution in {country} in {year}')
        diseases = st.multiselect('Select Diseases for Pie Chart', data_year['Disease'].unique(), default=data_year['Disease'].unique()[:5])
        data_pie = data_year[data_year['Disease'].isin(diseases)]
        fig_distribution = px.pie(data_pie, names='Disease', values='Count', title=f'Disease Distribution in {country} in {year}')
        st.plotly_chart(fig_distribution)
        
        # Heatmap for correlation between diseases
        st.subheader("Heatmap for correlation between diseases")
        corr = filtered_data.iloc[:, 4:].corr()
        plt.figure(figsize=(17, 17))
        heatmap = sns.heatmap(corr, annot=True, cmap='coolwarm')
        st.pyplot(heatmap.figure)
            
            
    elif a == 'American':
        
        data = pd.read_csv("american.csv")
        # print(data.columns)
        data.drop(columns=['Unnamed: 0'],inplace=True)
        # data

        countries = st.sidebar.multiselect('Select Countries', options=data['Country/Territory'].unique(), default=data['Country/Territory'].unique()[:5])
        diseases = st.sidebar.multiselect('Select Diseases', options=data.columns[3:].to_list(),default=data.columns[7:13].to_list())
        # st.write(diseases)
        year = st.sidebar.slider('Select Year', int(data['Year'].min()), int(data['Year'].max()), value=[2001])

        filtered_data = data[data['Country/Territory'].isin(countries)]
        st.write("### Disease Data")
        st.dataframe(filtered_data)

        # Line Chart
        st.write("## Trends Over Time")
        for disease in diseases:
            fig = px.line(filtered_data, x='Year', y=disease, color='Country/Territory', title=f'{disease} Over Time')
            st.plotly_chart(fig)

        # Bar Chart
        st.write("## Comparisons Between Countries")
        bar_chart_data = filtered_data[filtered_data['Year'] == year]
        for disease in diseases:
            fig = px.bar(bar_chart_data, x='Country/Territory', y=disease, color='Country/Territory', title=f'{disease} Comparison in {year}')
            st.plotly_chart(fig)

        # Heatmap for Matrix View of Disease Prevalence
        st.write("## Disease Prevalence Heatmap")
        heatmap_data = bar_chart_data.set_index('Country/Territory')[diseases].transpose()
        # st.write(heatmap_data)
        fig = px.imshow(heatmap_data, labels=dict(x="Country/Territory", y="Disease", color="Prevalence"), title=f'Disease Prevalence in {year}')
        st.plotly_chart(fig)

        # Pie Chart for Distribution of Diseases within a Country for a Specific Year
        st.write("## Disease Distribution Pie Chart")
        country = st.sidebar.selectbox('Select Country for Pie Chart', options=countries)
        pie_chart_data = filtered_data[(filtered_data['Country/Territory'] == country) & (filtered_data['Year'] == year)]
        pie_chart_data = pie_chart_data[diseases].melt(var_name='Disease', value_name='Prevalence')
        fig = px.pie(pie_chart_data, values='Prevalence', names='Disease', title=f'Disease Distribution in {country} for {year}')
        st.plotly_chart(fig)
    
    
    elif a == 'European':
        data = pd.read_csv("europe.csv")
        data.drop(columns=['Unnamed: 0'],inplace=True)
        data
        
        diseases = data.columns.difference(['Year', 'Country/Territory', 'Code'])
        selected_diseases = st.sidebar.multiselect(
            'Select Diseases',
            options=diseases,default=['Diarrheal Diseases','Cirrhosis and Other Chronic Liver Diseases','Drowning',
                                        'HIV/AIDS','Lower Respiratory Infections']
        )
        filtered_data = data[['Year'] + selected_diseases]
        # st.write(filtered_data)
        heatmap_data = filtered_data.set_index('Year')

        st.subheader('Heatmap of Disease Counts Over the Years')
        fig_heatmap = go.Figure(data=go.Heatmap(
            z=heatmap_data.T,
            x=heatmap_data.columns,
            y=heatmap_data.index,
            colorscale='Viridis'
        ))
        fig_heatmap.update_layout(title='Disease Counts Heatmap')
        st.plotly_chart(fig_heatmap)
        
        
        # Pie Chart of Disease Proportions
        st.subheader('Pie Chart of Disease Proportions for Selected Year')
        years = data['Year'].unique()
        selected_year = st.selectbox('Select a year for pie chart', years, index=len(years)-1)
        pie_data = data[data['Year'] == selected_year].drop(columns=['Country/Territory', 'Code', 'Year']).sum().head(10)
        fig_pie = go.Figure(data=go.Pie(labels=pie_data.index, values=pie_data.values, hole=0.3))
        fig_pie.update_layout(title=f'Disease Proportions for {selected_year}')
        st.plotly_chart(fig_pie)

        #  Bar Chart of Disease Counts by Year
        st.subheader('Bar Chart of Disease Counts by Year')
        selected_years = st.multiselect('Select years to display', years, default=[1995,1996,1998,2000])
        selected_diseases = st.multiselect('Select diseases to display', heatmap_data.columns)
        filtered_data = data[data['Year'].isin(selected_years)]
        grouped_data = filtered_data[selected_diseases].groupby(filtered_data['Year']).sum().reset_index()
        fig_bar = px.bar(grouped_data, x='Year', y=selected_diseases, title='Disease Counts by Year', labels={'value': 'Count'})
        st.plotly_chart(fig_bar)

        # # Line Chart of Specific Disease Trends
        selected_diseases_line = st.multiselect('Select diseases for trend analysis', data.columns[3:],default=['Diabetes Mellitus','HIV/AIDS','Lower Respiratory Infections'])
        if selected_diseases_line:
            grouped_data = data.groupby('Year')[selected_diseases_line].sum().reset_index()
            fig_line = go.Figure()
            for disease in selected_diseases_line:
                fig_line.add_trace(go.Scatter(x=grouped_data['Year'], y=grouped_data[disease], mode='lines+markers', name=disease))
            fig_line.update_layout(title='Trend of Selected Diseases', xaxis_title='Year', yaxis_title='Count')
            st.plotly_chart(fig_line)
        else:
            st.warning('Please select at least one disease.')

        # # Area Chart of Disease Counts
        st.subheader('Area Chart of Disease Counts Over the Years')
        fig_area = px.area(data, x='Year', y=heatmap_data.columns, title='Disease Counts Area Chart', labels={'value': 'Count'})
        st.plotly_chart(fig_area)
        
else:
    st.title("About Us")
    
    # Section: Purpose of the Dashboard
    st.header("Purpose")
    st.write(
        """
        The Global Health Dashboard is designed to provide an interactive platform for analyzing 
        and understanding global health trends. By presenting health data in an intuitive format, 
        it helps policymakers, researchers, and the general public gain valuable insights into 
        disease patterns and public health challenges worldwide.
        """
    )
    
    # Section: Data Sources
    st.header("Data Sources")
    st.write(
        """
        The data used in this dashboard is sourced from reputable organizations, ensuring reliability 
        and accuracy. Key source include:
        - [kaggle ](https://www.kaggle.com/datasets/iamsouravbanerjee/cause-of-deaths-around-the-world)
        """
    )
    
    # Section: Features
    st.header("Features")
    st.write(
        """
        - **Interactive Graphs:** Visualize disease trends, distributions, and comparisons across regions.
        - **Custom Filters:** Analyze data by continents, countries, diseases, and years.
        - **Correlation Analysis:** Understand relationships between various health metrics.
        - **Data Insights:** Explore key patterns in morbidity and mortality rates.
        """
    )       


