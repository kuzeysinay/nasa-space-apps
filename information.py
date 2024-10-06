import streamlit as st
import pandas as pd
import plotly.express as px

def display_greenhouse_gas_section():
    # Main title
    st.title("Greenhouse Gas Effects: CO₂ and CH₄")

    # Displaying images side by side using two-column layout
    col1, col2 = st.columns(2)

    with col1:
        st.image("icons/fire.jpg", use_column_width=True)
    with col2:
        st.image("icons/fire2.jpg", use_column_width=True)

    # Introduction text
    st.markdown("""
    **Greenhouse gases** are gases that contribute to the warming of the Earth by trapping heat in the atmosphere; among them, carbon dioxide and methane are the most significant.
    """)

    # Sidebar for selecting the year range within this section
    st.sidebar.header("Graph Settings")
    year_min = 1990
    year_max = 2021
    selected_years = st.sidebar.slider("Select Year Range", min_value=year_min, max_value=year_max, value=(year_min, year_max), step=1)

    # CO₂ and CH₄ data
    data_co2 = {
        'Year': [1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 
                 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 
                 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 
                 2019, 2020, 2021],
        'CO₂ Emissions (Million Tonnes)': [
            151.6, 158.1, 164.1, 171.1, 167.6, 
            181.4, 199.6, 212.1, 212.1, 207.9, 
            229.9, 213.6, 221.2, 236.8, 244.8, 
            264.9, 282.4, 313.7, 310.6, 316.4, 
            316.2, 342.1, 356.1, 347.3, 364.0, 
            384.9, 406.0, 430.9, 422.1, 402.7, 
            412.9, 452.7
        ]
    }

    data_ch4 = {
        'Year': [1990, 1995, 2000, 2005, 2010, 2015, 2016, 2017, 2018, 2019, 2020, 2021],
        'CH₄ Emissions (Thousand Tonnes)': [
            1699.5, 1704.5, 1746.7, 1806.9, 
            2065.8, 2111.4, 2223.3, 2272.7, 
            2416.4, 2528.7, 2555.8, 2560.8
        ]
    }

    # Creating dataframes
    df_co2 = pd.DataFrame(data_co2)
    df_ch4 = pd.DataFrame(data_ch4)

    # Filtering data based on selected year range
    df_co2 = df_co2[(df_co2['Year'] >= selected_years[0]) & (df_co2['Year'] <= selected_years[1])]
    df_ch4 = df_ch4[(df_ch4['Year'] >= selected_years[0]) & (df_ch4['Year'] <= selected_years[1])]

    # CO₂ and CH₄ tabs
    tab1, tab2, tab3 = st.tabs(["CO₂", "CH₄", "Comparison"])

    # CO₂ Tab
    with tab1:
        st.subheader("Carbon Dioxide (CO₂)")
        st.markdown("""
        **CO₂** is the most common greenhouse gas. Human activities, especially the burning of fossil fuels (coal, oil, natural gas) and deforestation, increase CO₂ emissions.
        """)

        # CO₂ line chart
        fig_co2 = px.line(df_co2, x='Year', y='CO₂ Emissions (Million Tonnes)', 
                          title='CO₂ Emissions Over the Years', 
                          markers=True)
        st.plotly_chart(fig_co2)

    # CH₄ Tab
    with tab2:
        st.subheader("Methane (CH₄)")
        st.markdown("""
        **CH₄** is a more powerful greenhouse gas than carbon dioxide. It is released into the atmosphere through natural gas production, agricultural activities (especially livestock farming), and the decomposition of organic waste in landfills.
        """)

        # CH₄ line chart
        fig_ch4 = px.line(df_ch4, x='Year', y='CH₄ Emissions (Thousand Tonnes)', 
                          title='CH₄ Emissions Over the Years', 
                          markers=True)
        st.plotly_chart(fig_ch4)

    # Comparison Tab
    with tab3:
        st.subheader("Comparison of CO₂ and CH₄ Emissions")
        st.markdown("""
        The following graphs show a comparative view of CO₂ and CH₄ emissions.
        """)

        # Merging CO₂ and CH₄ data
        df_co2_ch4 = pd.merge(df_co2, df_ch4, on='Year', how='outer')

        # Displaying both gases on the same graph
        fig_compare = px.line(df_co2_ch4, x='Year', y=['CO₂ Emissions (Million Tonnes)', 'CH₄ Emissions (Thousand Tonnes)'], 
                              title='Comparison of CO₂ and CH₄ Emissions Over the Years', 
                              markers=True)
        st.plotly_chart(fig_compare)

    # Conclusion and Additional Information
    st.markdown("""
    ### **How Are Greenhouse Gases Produced?**
    
    1. **Burning of Fossil Fuels**: The consumption of fuel in vehicles and the use of coal for electricity production result in carbon dioxide emissions.
    2. **Agricultural Activities**: Livestock farming produces methane gas, while the use of fertilizers leads to nitrous oxide emissions.
    3. **Industrial Production**: Carbon dioxide and fluorinated gases are released during chemical processes and the production of certain goods.
    4. **Waste**: The decomposition of organic waste in landfills produces methane gas.
    
    **Note**: Greenhouse gases can also come from natural sources such as volcanic eruptions and animal respiration.
    
    **Also**: Biomass burning and forest fires also release significant amounts of carbon dioxide and other greenhouse gases into the atmosphere.
    """)

    

    # Q&A Section
    st.markdown("### Questions and Answers")

    with st.expander("Question 1: What is the main source of CO₂ emissions?"):
        st.write("**Answer**: The main source of CO₂ emissions is the burning of fossil fuels (coal, oil, natural gas) for energy and transportation.")

    with st.expander("Question 2: Why is CH₄ considered a stronger greenhouse gas than CO₂?"):
        st.write("**Answer**: Methane (CH₄) is considered stronger because it traps more heat per molecule in the atmosphere compared to CO₂.")

    with st.expander("Question 3: What can we do to reduce greenhouse gas emissions?"):
        st.write("**Answer**: Switching to renewable energy sources, improving energy efficiency, preventing deforestation, and improving waste management are some steps that can be taken.")

    with st.expander("Question 4: What are the effects of greenhouse gases on climate change?"):
        st.write("**Answer**: Greenhouse gases cause global temperatures to rise, sea levels to increase, and the frequency of extreme weather events to intensify.")

    # Text area for feedback input
    feedback = st.text_area("**Submit Your Solutions for Greenhouse Gases and Feedback for the Site:**", "")

    # Submit button for feedback
    if st.button("Submit"):
        if feedback:
            try:
                # Create a DataFrame to store feedback
                if 'feedbacks' not in st.session_state:
                    st.session_state['feedbacks'] = []

                # Save the feedback
                st.session_state['feedbacks'].append(feedback)

                # Success message for the user
                st.success("Your feedback has been successfully recorded!")
            except Exception as e:
                st.error(f"An error occurred while recording your feedback: {e}")
        else:
            st.warning("Please enter your feedback.")
