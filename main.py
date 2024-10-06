import streamlit as st
from emissions import display_emissions_map
from news import display_news_section
from most_emission_landfills import display_most_emission_landfills
from information import display_greenhouse_gas_section  # Newly added function
from top10 import display_top_10_emissions
from PIL import Image


st.set_page_config(page_title="Trash Can Harm", page_icon="🗑️")
# Main function to control the app layout
def main():
    # Create a header with image and text side by side using columns
    header_col1, header_col2 = st.columns([1, 8])  # Adjust column ratios as needed

    with header_col1:
        try:
            # Load and display the trashcan image
            trashcan_image = Image.open("icons/trashcan.png")
            st.image(trashcan_image, width=60)
        except FileNotFoundError:
            st.error("Trashcan image not found. Please ensure 'icons/trashcan.png' exists.")
    
    with header_col2:
        # Display the site name
        st.markdown("<h2 style='margin-left: 10px;'>Trash Can Harm Us</h2>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)  # Optional: Add a horizontal line below the header

    # Sidebar navigation
    nav_options = [
        "Home",
        "Emissions Map",
        "News",
        "Greenhouse Gas Effects",
        "Top 10 Countries With Highest Emission"
    ]
    choice = st.sidebar.radio("Menu", nav_options)

    # Main content area
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    if choice == "Home":
        st.markdown("""
            ### Home
            The goal of our NASA Space App Challenge is to highlight that waste is one of the main contributors to the greenhouse effect, emphasizing the urgency of sustainable waste management practices and innovative solutions to reduce our environmental impact.
        """)
        left_co, cent_co,last_co = st.columns(3)
        with cent_co:
            st.image("icons/home_page.png", width=400)
        
        
    
    elif choice == "Emissions Map":
        st.markdown("### Emissions Map")
        display_emissions_map()
        display_most_emission_landfills()
    
  
        
    
    elif choice == "News":
        st.markdown("### News")
        display_news_section()
    
    elif choice == "Greenhouse Gas Effects":
        display_greenhouse_gas_section()  # Call the content of the new tab

    elif choice == "Top 10 Countries With Highest Emission":
        display_top_10_emissions()  # Call the content of the new tab

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
