import streamlit as st
import requests
from bs4 import BeautifulSoup

def get_faceit_elo(nickname: str):
    """Prøv at hente FaceIt ELO fra en profilside med requests"""
    url = f"https://www.faceit.com/en/players/{nickname}"
    headers = {"User-Agent": "Mozilla/5.0"}  # trick for at ligne en browser
    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        return f"Fejl {r.status_code} ved hentning af profil"

    soup = BeautifulSoup(r.text, "html.parser")

    # Prøv at finde elementet hvor ELO står
    # OBS: Du skal måske ændre 'stats-value' hvis FaceIt ændrer design
    elo_element = soup.find("span", {"class": "stats-value"})
    if elo_element:
        return elo_element.text.strip()

    return "Kunne ikke finde ELO i HTML (FaceIt loader muligvis via JavaScript)"

# =============================
# Streamlit UI
# =============================
st.title("FaceIt ELO Scraper Demo")
st.write("Indtast et FaceIt nickname og se spillerens ELO (POC-version).")

nickname = st.text_input("FaceIt nickname:", "s1mple")

if st.button("Hent ELO"):
    with st.spinner("Henter data..."):
        elo = get_faceit_elo(nickname)
    st.success(f"{nickname} → {elo}")
