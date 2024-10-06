import streamlit as st
import requests
from datetime import datetime

# Place your API key here
API_KEY = 'e1fc82e10f9347f5840ee0bca72902b7'  # Put your own API key here

def fetch_news(query):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'language': 'en',  # English news
        'apiKey': API_KEY
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json().get('articles', [])  # Ensure articles is returned as a list
    else:
        st.error("An error occurred while fetching the news.")
        return []

def is_relevant_article(article):
    # Only include articles with "landfill" in the title
    return 'landfill' in article.get('title', '').lower()

def format_date(iso_date_str):
    # Convert ISO format to user-friendly format
    try:
        date_obj = datetime.strptime(iso_date_str, "%Y-%m-%dT%H:%M:%SZ")
        return date_obj.strftime("%d %B %Y")
    except ValueError:
        return "Unknown Date"

def display_article(article):
    # Handle cases where urlToImage is None or invalid
    image_url = article.get('urlToImage') or 'https://via.placeholder.com/150'  # Default image if urlToImage is None
    
    # Convert the date to user-friendly format
    published_at = format_date(article.get("publishedAt", "Unknown"))

    # Compact card design for the article
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
        <img src="{image_url}" style="width: 120px; height: 80px; object-fit: cover; border-radius: 5px; margin-right: 15px;" alt="Article Image">
        <div style="flex: 1;">
            <h3 style="margin: 0; font-size: 20px; color: #FF6347;">{article.get("title", "No Title")}</h3>
            <p style="margin: 5px 0; font-size: 14px; color: #333;">{article.get("description", "No Description")}</p>
            <div style="display: flex; justify-content: space-between; font-size: 12px; color: #555;">
                <a href="{article.get('url', '#')}" target="_blank" style="color: #007BFF; text-decoration: none;">Read More</a>
                <span>Published on: {published_at}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def display_news_section():
    st.header("Latest News About Landfills")

    # Fetch main articles
    articles = fetch_news('landfill fire')

    # Suggested news categories
    suggestion_queries = ['waste', 'environment', 'landfill']
    suggested_articles = []
    
    for query in suggestion_queries:
        suggested_articles += fetch_news(query)
    
    # Combine main articles and suggested articles
    all_articles = articles + suggested_articles
    
    # Filter articles to only include those with "landfill" in the title
    filtered_articles = [article for article in all_articles if is_relevant_article(article)]
    
    if filtered_articles:
        # Pagination for articles
        num_articles_per_page = 3
        total_articles = len(filtered_articles)
        
        # Initialize session state for pagination
        if 'page' not in st.session_state:
            st.session_state.page = 0
        
        # CSS style to make buttons appear in one row and centered
        st.markdown("""
        <style>
        .pagination-buttons {
            display: flex;
            justify-content: center;
            margin-bottom: 20px;
        }
        .pagination-buttons button {
            width: 100px;
            height: 35px;
            margin: 0 10px;
            font-size: 14px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Place Previous and Next buttons at the top (centered above the articles)
        st.markdown('<div class="pagination-buttons">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        previous_clicked = col1.button("Previous", use_container_width=True)
        next_clicked = col2.button("Next", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle the pagination
        if previous_clicked and st.session_state.page > 0:
            st.session_state.page -= 1
        
        if next_clicked and (st.session_state.page + 1) * num_articles_per_page < total_articles:
            st.session_state.page += 1
        
        # Calculate the start and end index for the current page
        start_idx = st.session_state.page * num_articles_per_page
        end_idx = min(start_idx + num_articles_per_page, len(filtered_articles))  # Ensure it doesn't exceed the list size

        # Display the articles for the current page
        for article in filtered_articles[start_idx:end_idx]:
            display_article(article)
        
    else:
        st.write("No relevant news found.")
