import streamlit as st
import requests
from streamlit_player import st_player

st.set_page_config(page_title="Quran Lecture App", layout="wide")

st.title("📖 Quran Lecture App with Audio & Translation")
st.sidebar.title("📖 Quran Lecture App")
st.sidebar.write("Select Surah and search Ayahs")

# ----------- Surah List -----------
surah_list = requests.get("http://api.alquran.cloud/v1/surah").json()['data']
surah_names = [f"{s['number']}. {s['englishName']} ({s['name']})" for s in surah_list]

selected_surah_name = st.sidebar.selectbox("Choose Surah", surah_names)
selected_surah_number = int(selected_surah_name.split(".")[0])

# Search input
search_keyword = st.sidebar.text_input("Search Ayah (Arabic)")

# Translation toggle
show_translation = st.sidebar.checkbox("Show Translation")
translation_choice = st.sidebar.selectbox("Choose Translation", ["ur.maududi","en.asad"])

# ----------- Fetch Ayahs -----------
# Arabic recitation
recitation_url = f"http://api.alquran.cloud/v1/surah/{selected_surah_number}/ar.abdurrehmansudais"
recitation_response = requests.get(recitation_url).json()
arabic_ayahs = recitation_response['data']['ayahs']

# Translation
if show_translation:
    translation_url = f"https://api.alquran.cloud/v1/surah/{selected_surah_number}/{translation_choice}"
    translation_response = requests.get(translation_url).json()
    translated_ayahs = translation_response['data']['ayahs']
else:
    translated_ayahs = [None]*len(arabic_ayahs)

# Filter by search keyword if provided
if search_keyword.strip() != "":
    filtered_ayahs = []
    filtered_translations = []
    for i, ayah in enumerate(arabic_ayahs):
        if search_keyword in ayah['text']:
            filtered_ayahs.append(ayah)
            filtered_translations.append(translated_ayahs[i])
    arabic_ayahs = filtered_ayahs
    translated_ayahs = filtered_translations

# ----------- Display Ayahs -----------
for i, ayah in enumerate(arabic_ayahs):
    st.markdown(f"**{ayah['numberInSurah']}**: {ayah['text']}")
    audio_url = ayah.get('audio', None)
    if audio_url:
        st_player(audio_url, key=ayah['numberInSurah'])
    
    if show_translation and translated_ayahs[i] is not None:
        st.info(translated_ayahs[i]['text'])

# ----------- Footer -----------
st.markdown("---")
st.markdown("Developed by **Syed Muhammad Arsalan Shah Bukhari**")
