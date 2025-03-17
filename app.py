import streamlit as st
import json
import pandas as pd
import pydeck as pdk
import requests
import datetime
import matplotlib.pyplot as plt
from collections import Counter

# Function to get latitude & longitude from IP address
def get_lat_long(ip_address, access_token):
    url = f"https://ipinfo.io/{ip_address}/json?token={access_token}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if 'loc' in data:
            lat, lon = data['loc'].split(',')
            return float(lat), float(lon)
    except requests.RequestException:
        return None, None
    return None, None

# Streamlit UI
st.title("📂 Instagram Privacy Data Processor")

# Step 1: Upload JSON File
uploaded_file = st.file_uploader("Upload a JSON file", type=["json"])

if uploaded_file:
    # Step 2: Load JSON Data
    data = json.load(uploaded_file)
    st.success("✅ JSON file loaded successfully!")

    # Step 3: Extract User Information
    try:
        user_info = data['personal_information']['profile_user'][0]['string_map_data']
        user_email = user_info['Email']['value']
        user_username = user_info['Username']['value']
        user_name = user_info['Name']['value']
        user_dob = user_info['Date of birth']['value']

        st.write(f"**👤 User Info:** {user_name} ({user_username}) | Email: {user_email} | DOB: {user_dob}")
    except KeyError:
        st.warning("⚠️ User info not found.")

    # Step 4: Extract & Display All Ad Information
    try:
        ads_with_info = data['advertisers_using_your_activity_or_information']['ig_custom_audiences_all_types']
        num_ads = len(ads_with_info)
        num_ads_with_data = sum([ad['has_data_file_custom_audience'] for ad in ads_with_info])
        num_ads_with_visit_data = sum([ad['has_in_person_store_visit'] for ad in ads_with_info])

        st.subheader("📢 Advertisement Insights")
        st.write(f"**Total Ads:** {num_ads}")
        st.write(f"**Ads Using Custom Data:** {num_ads_with_data}")
        st.write(f"**Ads That Know You Visited a Store:** {num_ads_with_visit_data}")

        # Convert to DataFrame & Show All Ads
        ad_data = [
            {
                "Advertiser Name": ad.get("advertiser_name", "Unknown"),
                "Uses Custom Data": ad.get("has_data_file_custom_audience", False),
                "Knows In-Person Visit": ad.get("has_in_person_store_visit", False),
            }
            for ad in ads_with_info
        ]
        st.subheader("📜 List of All Ads")
        st.dataframe(pd.DataFrame(ad_data))

    except KeyError:
        st.warning("⚠️ Ad information not found.")

    # Step 5: Extract Post Information
    try:
        posts = data['posts_viewed']['impressions_history_posts_seen']
        num_posts = len(posts)

        # Extract timestamps and convert them to dates
        timestamps = [item["string_map_data"]["Time"]["timestamp"] for item in posts]
        dates = [datetime.datetime.fromtimestamp(ts).date() for ts in timestamps]

        # Count posts per day
        date_counts = Counter(dates)
        sorted_dates = sorted(date_counts.keys())
        post_counts = [date_counts[date] for date in sorted_dates]

        st.subheader("📊 Posts Viewed Over Time")
        st.bar_chart(pd.DataFrame({"Date": sorted_dates, "Posts Seen": post_counts}).set_index("Date"))

    except KeyError:
        st.warning("⚠️ Post view data not found.")

    # Step 6: Process IP Data for Mapping
    try:
        locations = data['login_activity']['account_history_login_history']
        ip_data = [
            {
                "IP Address": entry["string_map_data"].get("IP Address", {}).get("value", ""),
                "User Agent": entry["string_map_data"].get("User Agent", {}).get("value", ""),
                "Timestamp": entry["string_map_data"].get("Time", {}).get("timestamp", ""),
            }
            for entry in locations
        ]

        # Get Geo Data
        access_token = '3ff067e36a649a'  # Replace with a valid IPInfo token
        geo_data = []
        for entry in ip_data:
            ip_address = entry.get('IP Address')
            if ip_address:
                lat, lon = get_lat_long(ip_address, access_token)
                entry['Latitude'] = lat if lat is not None else 'N/A'
                entry['Longitude'] = lon if lon is not None else 'N/A'
            geo_data.append(entry)

        # Convert Timestamp to Date-Time Format
        for entry in geo_data:
            entry["Date Time"] = datetime.datetime.utcfromtimestamp(entry["Timestamp"]).strftime('%Y-%m-%d %H:%M:%S')

        # Convert to DataFrame
        df = pd.DataFrame(geo_data)

        # Step 7: Pydeck Map Visualization
        if not df.empty and "Latitude" in df.columns and "Longitude" in df.columns:
            st.subheader("🌍 IP Address Mapping")

            scatterplot_layer = pdk.Layer(
                "ScatterplotLayer",
                data=df,
                get_position=["Longitude", "Latitude"],
                get_color=[255, 0, 0, 160],
                get_radius=10000,
                pickable=True
            )

            tooltip = {
                "html": "<b>Date:</b> {Date Time} <br/> <b>User Agent:</b> {User Agent}",
                "style": {"backgroundColor": "black", "color": "white"}
            }

            view_state = pdk.ViewState(
                latitude=df["Latitude"].mean(),
                longitude=df["Longitude"].mean(),
                zoom=5,
                pitch=0
            )

            deck = pdk.Deck(
                layers=[scatterplot_layer],
                initial_view_state=view_state,
                tooltip=tooltip
            )

            st.pydeck_chart(deck)

    except KeyError:
        st.warning("⚠️ Login activity data not found.")

    # Step 8: Extract Recently Viewed Products
    try:
        products = data['recently_viewed_items']['checkout_saved_recently_viewed_products']
        product_pairs = [
            (item["string_map_data"]["Product Name"]["value"], item["string_map_data"]["Merchant Name"]["value"])
            for item in products
        ]

        st.subheader("🛍️ Recently Viewed Products")
        st.write(pd.DataFrame(product_pairs, columns=["Product Name", "Merchant"]))

    except KeyError:
        st.warning("⚠️ Recently viewed products not found.")

    # Step 9: Extract Recommended Topics
    try:
        topics = data['recommended_topics']['topics_your_topics']
        topic_names = [topic['string_map_data']['Name']['value'] for topic in topics]

        st.subheader("📌 Recommended Topics")
        st.write(topic_names)

    except KeyError:
        st.warning("⚠️ Recommended topics not found.")
