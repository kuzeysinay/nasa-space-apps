import streamlit as st
import pandas as pd
import pydeck as pdk
import numpy as np
from streamlit_geolocation import streamlit_geolocation  # Doğru içe aktarma





def display_emissions_map():
    # Kullanıcının geolokasyonunu al
    
    

    # Veri setini yükle
    df = pd.read_csv('solid-waste-disposal_emissions_sources.csv')

    # İlgili sütunları çıkar
    df_filtered = df[['lat', 'lon', 'start_time', 'source_name', 'emissions_quantity', 'source_id', 'gas']]

    # Sadece 'co2e_100yr' gaz türünü filtrele
    df_filtered = df_filtered[df_filtered['gas'] == 'co2e_100yr']

    # Daha kolay filtreleme için yıl sütunu ekle
    df_filtered['year'] = pd.to_datetime(df_filtered['start_time']).dt.year

    # Emisyon miktarına göre sıralama ve sıralama numarası hesaplama
    df_filtered['rank'] = df_filtered['emissions_quantity'].rank(method="min", ascending=False).astype(int)

    # Daire boyutları için min ve max yarıçap ayarla
    min_radius = 2000
    max_radius = 10000

    # Emisyon verilerine log ölçeği uygulayın ve min_radius ile max_radius arasında normalize edin
    df_filtered['emission_scaled'] = np.interp(
        np.log1p(df_filtered['emissions_quantity']),
        (np.log1p(df_filtered['emissions_quantity'].min()), np.log1p(df_filtered['emissions_quantity'].max())),
        (min_radius, max_radius)
    )

    # Emisyonları kullanıcı dostu bir string olarak formatla
    df_filtered['emissions_formatted'] = df_filtered.apply(lambda row: f"{int(row['emissions_quantity']):,}", axis=1)

    # 2021 ve 2022 verilerini filtrele
    df_2021 = df_filtered[df_filtered['year'] == 2021]
    df_2022 = df_filtered[df_filtered['year'] == 2022]

    # Streamlit UI
    st.header("Landfill Emissions in Turkey")

    # Yıl seçimi için selectbox kullan
    year = st.selectbox('', [2021, 2022], index=1)  # Varsayılan değer 2022


    

    # Seçilen yıla göre veriyi belirle
    if year == 2021:
        data_to_display = df_2021
    else:
        data_to_display = df_2022

    location = streamlit_geolocation()
    if location and 'latitude' in location and 'longitude' in location:
        user_lat = location["latitude"]
        user_lon = location["longitude"]
    else:
        user_lat, user_lon = None, None
        st.error("Lokasyon bilgisi alınamadı. Lütfen izin verin ve butona basın.")


    # Emisyon yoğunluğunu hesapla ve en yoğun 10 konumu bul
    emissions_per_location = df_filtered.groupby(['lat', 'lon']).agg({
        'emissions_quantity': 'sum'
    }).reset_index()
    emissions_per_location['emissions_density'] = emissions_per_location['emissions_quantity']
    top_10_locations = emissions_per_location.nlargest(10, 'emissions_density')

    # Tooltip içeriğini data_to_display için oluşturun
    def generate_tooltip_content(row):
        return f"""
        <b style="color:white;">{row['source_name']}</b><br>
        <div style="color:white;">{row['emissions_formatted']} tons CO<sub>2</sub>e in {row['year']}</div>
        <div style="color:white;">Rank: {row['rank']}</div>
        """
    data_to_display['tooltip_content'] = data_to_display.apply(generate_tooltip_content, axis=1)

    # top_10_locations için tooltip_content ekleyin
    top_10_locations['tooltip_content'] = 'Recommended Recycling Center Location'

    # Harita görünümünü tanımla
    if user_lat and user_lon:
        view_state = pdk.ViewState(
            latitude=user_lat,
            longitude=user_lon,
            zoom=10
        )
    else:
        view_state = pdk.ViewState(
            latitude=data_to_display['lat'].mean(),
            longitude=data_to_display['lon'].mean(),
            zoom=6
        )

    # CO2 emisyonlarına göre boyutlandırılmış noktaları gösteren katman
    layer_original = pdk.Layer(
        'ScatterplotLayer',
        data=data_to_display,
        get_position='[lon, lat]',
        get_radius='emission_scaled',
        get_color=[125, 100, 0, 140],  # Varsayılan renk
        pickable=True
    )

    # En yoğun 10 konum için farklı renk ve opaklıkta katman
    layer_top_10 = pdk.Layer(
        'ScatterplotLayer',
        data=top_10_locations,
        get_position='[lon, lat]',
        get_radius=10000,  # Sabit büyük boyut
        get_color=[33, 158, 33, 255],  # Opak yeşil renk
        pickable=True
    )

    # Kullanıcının konumu varsa bir katman ekle
    if user_lat and user_lon:
        user_location_df = pd.DataFrame({
            'lat': [user_lat],
            'lon': [user_lon],
            'tooltip_content': ['Your Location']
        })

        user_location_layer = pdk.Layer(
            'ScatterplotLayer',
            data=user_location_df,
            get_position='[lon, lat]',
            get_radius=5000,
            get_color=[0, 0, 255, 255],  # Mavi renk
            pickable=True
        )

        # Tüm katmanları ekle
        layers = [layer_original, layer_top_10, user_location_layer]
    else:
        # Kullanıcının konumu yoksa sadece orijinal katmanları ekle
        layers = [layer_original, layer_top_10]

    # Tooltip'i güncelleyin
    r = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={
            "html": "{tooltip_content}",
            "style": {"color": "white"}
        },
        map_style="mapbox://styles/mapbox/light-v10"  # Açık harita stili
    )

    # Güncellenmiş pydeck grafiğini Streamlit'te göster
    st.pydeck_chart(r)

# Uygulamayı çalıştır
if __name__ == "__main__":
    display_emissions_map()