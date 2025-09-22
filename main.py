import streamlit as st
import requests

# ---------------- Config ----------------
st.set_page_config(page_title="Quran Lecture App", layout="wide")

st.title("📖 Quran Lecture App with Audio & Translation")
st.sidebar.title("📖 Controls")
st.sidebar.write("Select Surah and search Ayahs")

# ---------------- Surah List ----------------
surah_list = requests.get("http://api.alquran.cloud/v1/surah").json()['data']
surah_names = [f"{s['number']}. {s['englishName']} ({s['name']})" for s in surah_list]

selected_surah_name = st.sidebar.selectbox("Choose Surah", surah_names)
selected_surah_number = int(selected_surah_name.split(".")[0])

# Search input
search_keyword = st.sidebar.text_input("Search Ayah (Arabic text)")

# Translation toggle
show_translation = st.sidebar.checkbox("Show Translation")
translation_choice = st.sidebar.selectbox(
    "Choose Translation", ["ur.maududi", "en.asad", "en.pickthall", "ur.jalandhry"]
)

# ---------------- Fetch Data ----------------
# Arabic + Recitation
recitation_url = f"http://api.alquran.cloud/v1/surah/{selected_surah_number}/ar.abdurrahmaansudais"
recitation_response = requests.get(recitation_url).json()
arabic_ayahs = recitation_response['data']['ayahs']

# Translation
if show_translation:
    translation_url = f"https://api.alquran.cloud/v1/surah/{selected_surah_number}/{translation_choice}"
    translation_response = requests.get(translation_url).json()
    translated_ayahs = translation_response['data']['ayahs']
else:
    translated_ayahs = [None] * len(arabic_ayahs)

# ---------------- Filter ----------------
if search_keyword.strip():
    filtered_arabic = []
    filtered_translations = []
    for i, ayah in enumerate(arabic_ayahs):
        if search_keyword in ayah['text']:
            filtered_arabic.append(ayah)
            filtered_translations.append(translated_ayahs[i])
    arabic_ayahs = filtered_arabic
    translated_ayahs = filtered_translations

# ---------------- Display ----------------
st.subheader(selected_surah_name)

for i, ayah in enumerate(arabic_ayahs):
    st.markdown(f"**{ayah['numberInSurah']}** — {ayah['text']}")
    
    # Play audio with st.audio()
    if 'audio' in ayah and ayah['audio']:
        st.audio(ayah['audio'], format="audio/mp3")
    
    # Show translation if enabled
    if show_translation and translated_ayahs[i]:
        st.info(translated_ayahs[i]['text'])

# ---------------- Footer ----------------
st.markdown("---")
st.markdown("Developed by **Syed Muhammad Arsalan Shah Bukhari**")
