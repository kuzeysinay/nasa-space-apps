import pandas as pd
import streamlit as st

# Emisyon hesaplamasını yapan fonksiyon
def display_top_10_emissions():
    # CSV dosyasını oku
    data = pd.read_csv("per-capita-ghg-emissions.csv")

# Ülkelerin toplam emisyonunu hesapla
    total_emissions = data.groupby('Entity')['Per-capita greenhouse gas emissions in CO₂ equivalents'].sum().reset_index()

# En fazla emisyona sahip ilk 10 ülkeyi seç
    top_10_emissions = total_emissions.nlargest(10, 'Per-capita greenhouse gas emissions in CO₂ equivalents')

# Sıralama numarasını ekle
    top_10_emissions['Position'] = range(1, 11)

# Sadece 'Entity' ve 'Per-capita greenhouse gas emissions in CO₂ equivalents' sütunlarını göster
    st.markdown('**Top 10 Countries with the Highest Greenhouse Gas Emissions:**')
    st.dataframe(top_10_emissions[['Position', 'Entity', 'Per-capita greenhouse gas emissions in CO₂ equivalents']].set_index('Position'))
