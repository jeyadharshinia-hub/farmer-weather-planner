import streamlit as st
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="🌾 Farmer Weather & Crop Planner", page_icon="🌦️", layout="centered")

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #a8edea, #fed6e3);
        font-family: 'Segoe UI';
    }
    .main-title {
        text-align: center;
        color: #2e4053;
        font-size: 38px;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .sub-text {
        text-align: center;
        font-size: 18px;
        color: #424949;
        margin-bottom: 30px;
    }
    .card {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 18px;
        border-radius: 12px;
        box-shadow: 0px 2px 6px rgba(0,0,0,0.08);
        margin-bottom: 18px;
        border: 1px solid #dfe6e9;
    }
    hr {
        border: none;
        border-top: 1px solid #dcdcdc;
        margin: 15px 0;
    }
    @media (max-width: 600px) {
        .main-title { font-size: 26px !important; }
        .sub-text { font-size: 14px !important; }
        .stButton>button { width: 100%; font-size: 15px; }
    }
    </style>
""", unsafe_allow_html=True)

# --- PAGE HEADER ---
st.markdown("<div class='main-title'>🌾 Farmer Weather & Crop Planner</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Get live weather and simple crop suggestions for your farm</div>", unsafe_allow_html=True)

# --- INPUT SECTION ---
with st.container():
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        city = st.selectbox(
            "🏙 Select Your City",
            ["Select a city", "Madurai", "Chennai", "Coimbatore", "Trichy", "Salem", 
             "Tirunelveli", "Thanjavur", "Erode", "Vellore", "Nagercoil"]
        )

    with col2:
        soil_type = st.selectbox("🌱 Select Soil Type", ["Sandy", "Clay", "Loamy"])

    soil_condition = st.selectbox(
        "🧑‍🌾 How is your soil condition?",
        [
            "Normal (average fertility)",
            "Dry and sandy",
            "Wet or sticky (holds water)",
            "Rich and dark (fertile)"
        ]
    )

    st.markdown("</div>", unsafe_allow_html=True)

# --- WEATHER FUNCTION ---
def get_weather(city):
    api_key = "97c183466252c626f0ab132e75f192ba"  # your OpenWeatherMap key
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get("cod") == 200:
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            desc = data["weather"][0]["description"]
            return temp, humidity, desc
        else:
            st.warning(f"⚠️ API Error: {data.get('message', 'Unknown error')}")
            return None
    except:
        return None

# --- Convert Soil Condition to Approx. pH ---
def get_ph_from_condition(condition):
    if condition == "Normal (average fertility)":
        return 6.5
    elif condition == "Dry and sandy":
        return 6.0
    elif condition == "Wet or sticky (holds water)":
        return 7.0
    else:
        return 6.8

# --- CROP SUGGESTION FUNCTION ---
def suggest_crop(temp, humidity, soil, ph):
    if soil == "Loamy" and 20 <= temp <= 30 and 6 <= ph <= 7.5:
        return "Rice 🌾 or Wheat 🌿"
    elif soil == "Sandy" and temp > 30 and humidity < 60:
        return "Groundnut 🥜 or Millet 🌾"
    elif soil == "Clay" and humidity > 70:
        return "Sugarcane 🍬 or Paddy 🌾"
    elif soil == "Loamy" and temp < 20:
        return "Potato 🥔 or Barley 🌾"
    else:
        return "Maize 🌽 or Cotton ☁️"

# --- MAIN LOGIC ---
if st.button("🔍 Get Weather & Crop Suggestion"):
    if city == "Select a city":
        st.warning("⚠️ Please select a city first.")
    else:
        weather = get_weather(city)
        if weather:
            temp, humidity, desc = weather
            ph_value = get_ph_from_condition(soil_condition)

            # --- WEATHER CARD ---
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🌦️ Live Weather Report")
            st.write(f"**City:** {city}")
            st.write(f"**Temperature:** 🌡️ {temp} °C")
            st.write(f"**Humidity:** 💧 {humidity}%")
            st.write(f"**Condition:** ☁️ {desc.title()}")
            st.markdown("</div>", unsafe_allow_html=True)

            # --- CROP CARD ---
            crop = suggest_crop(temp, humidity, soil_type, ph_value)
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.subheader("🌾 Suggested Crop(s)")
            st.success(f"✅ {crop}")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("❌ Unable to fetch weather. Please try again later.")

