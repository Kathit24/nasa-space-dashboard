import streamlit as st  # For the web app UI
import requests  # For API calls
import matplotlib.pyplot as plt  # For charts
from datetime import datetime, timedelta  # For date handling

# Replace 'YOUR_API_KEY' with your real NASA API key from Step 1
API_KEY = API_KEY = st.secrets["ylRcTmImqmCpfnHf3tsRNPJjhtyzEOkkOLib4FlD"]  # IMPORTANT: Use your key here!


# Function to fetch Astronomy Picture of the Day (APOD)
def get_apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['title'], data['explanation'], data['url']
    else:
        return "Error", "Could not fetch data. Check your API key.", None


# Function to fetch Near-Earth Objects (NEO) data for the next 7 days
def get_neo_data():
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
    url = f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={end_date}&api_key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        asteroids = []
        for date, objects in data['near_earth_objects'].items():
            for obj in objects:
                name = obj['name']
                size = obj['estimated_diameter']['meters']['estimated_diameter_max']  # Size in meters
                distance = float(obj['close_approach_data'][0]['miss_distance']['kilometers'])  # Distance in km
                asteroids.append((name, size, distance))
        return asteroids[:10]  # Limit to 10 for simplicity
    else:
        return []


# Streamlit App Layout
st.title("🚀 NASA Space Data Dashboard")
st.markdown("Built with Python | Fetches real-time data from NASA APIs")

# Section 1: Astronomy Picture of the Day
st.header("🌌 Astronomy Picture of the Day")
apod_title, apod_explanation, apod_url = get_apod()
if apod_url:
    st.image(apod_url, caption=apod_title, use_column_width=True)
    st.write(apod_explanation)
else:
    st.error(apod_title + ": " + apod_explanation)

# Section 2: Near-Earth Objects Tracker
st.header("🛰️ Near-Earth Asteroids (Next 7 Days)")
asteroids = get_neo_data()
if asteroids:
    # Display as a table
    st.subheader("Asteroid List")
    st.table([{"Name": name, "Max Size (m)": round(size, 2), "Miss Distance (km)": round(distance, 2)} for
              name, size, distance in asteroids])

    # Simple bar chart: Size vs Distance
    st.subheader("Asteroid Size vs. Miss Distance")
    names = [name for name, _, _ in asteroids]
    sizes = [size for _, size, _ in asteroids]
    distances = [distance for _, _, distance in asteroids]

    fig, ax = plt.subplots()
    ax.bar(names, sizes, color='skyblue', label='Size (m)')
    ax.set_ylabel('Size (meters)', color='skyblue')
    ax.tick_params(axis='y', labelcolor='skyblue')

    ax2 = ax.twinx()
    ax2.plot(names, distances, color='red', marker='o', label='Distance (km)')
    ax2.set_ylabel('Miss Distance (km)', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)
else:
    st.error("Could not fetch asteroid data. Check your API key.")

# Footer
st.markdown("---")
st.markdown("Data sourced from NASA APIs. Built by [Your Name] for portfolio.")