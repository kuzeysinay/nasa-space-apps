import streamlit as st
import pandas as pd
import altair as alt


def display_most_emission_landfills():
    # Load the CSV file
    df = pd.read_csv('solid-waste-disposal_emissions_sources.csv')

    # Filter the dataset to include only 'co2e_100yr' gas emissions
    df_filtered = df[df['gas'] == 'co2e_100yr']

    # Sort by emissions_quantity and select the top 10 landfills
    top_10_landfills = df_filtered.nlargest(10, 'emissions_quantity')

    # Format the emissions quantity for display
    top_10_landfills['emissions_formatted'] = top_10_landfills['emissions_quantity'].apply(lambda x: f"{int(x):,}")

    # Create the bar chart using Altair
    chart = alt.Chart(top_10_landfills).mark_bar(color='#7d6400').encode(
        x=alt.X('source_name:N', sort='-y', ),
        y=alt.Y('emissions_quantity:Q', title='Emissions Quantity (tons of CO2e)'),
        tooltip=['source_name', 'emissions_quantity']
    ).properties(
        title='Top 10 Landfills with Highest CO2e Emissions',
        width=700,
        height=400
    )

    # Display the chart in Streamlit
    st.altair_chart(chart, use_container_width=True)

if __name__ == "__main__":
    display_most_emission_landfills()
