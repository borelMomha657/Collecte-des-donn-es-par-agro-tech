import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuration de la page
st.set_page_config(page_title="AgroCollect - Analyse de Marché", layout="wide")

DATA_FILE = "prix_agricoles.csv"

# Chargement des données
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Date", "Region", "Produit", "Prix_KG"])
    df.to_csv(DATA_FILE, index=False)
else:
    df = pd.read_csv(DATA_FILE)

st.title("🌾 AgroCollect : Collecte & Analyse des Prix")

# --- SECTION 1 : COLLECTE DES DONNÉES ---
st.sidebar.header("Saisie des données")
with st.sidebar.form("form_collecte", clear_on_submit=True):
    date = st.date_input("Date du relevé")
    region = st.selectbox("Région", ["Centre", "Littoral", "Ouest", "Nord", "Est"])
    produit = st.text_input("Nom du produit (ex: Maïs, Manioc)")
    prix = st.number_input("Prix au KG (FCFA)", min_value=0)
    
    submit = st.form_submit_button("Enregistrer")
    
    if submit and produit:
        new_data = pd.DataFrame([[date, region, produit, prix]], columns=df.columns)
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.sidebar.success("Données enregistrées !")

# --- SECTION 2 : ANALYSE DESCRIPTIVE ---
col1, col2 = st.columns()

with col1:
    st.subheader("Données brutes")
    st.dataframe(df.tail(10), use_container_width=True)

with col2:
    st.subheader("Statistiques & Visualisation")
    if not df.empty:
        # Analyse descriptive simple
        avg_price = df.groupby("Produit")["Prix_KG"].mean().reset_index()
        
        # Graphique
        fig = px.bar(avg_price, x="Produit", y="Prix_KG", 
                     title="Prix moyen par produit",
                     labels={"Prix_KG": "Prix Moyen (FCFA)"},
                     color="Produit")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aucune donnée disponible pour l'analyse.")
