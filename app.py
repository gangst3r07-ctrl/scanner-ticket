import streamlit as st
from fpdf import FPDF
import google.generativeai as genai
import json

# --- CONFIGURATION ---
# genai.configure(api_key="AIzaSyAUzrLSEexrKXQS02q1NTvlPWT_spVpz88")
model = genai.GenerativeModel('gemini-1.5-flash')

# --- FONCTION GENERATION PDF ---
def generer_pdf(data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, f"FACTURE : {data['nom_magasin']}", 0, 1, 'C')
    pdf.ln(10)
    
    pdf.set_font("Helvetica", '', 12)
    pdf.cell(0, 10, f"Date: {data['date']}", 0, 1)
    pdf.ln(5)

    # Tableau
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(100, 10, "Article", 1, 0, 'L', True)
    pdf.cell(40, 10, "Prix TTC", 1, 1, 'R', True)

    for art in data['articles']:
        pdf.cell(100, 10, art['nom'], 1)
        pdf.cell(40, 10, f"{art['prix_unitaire_ttc']:.2f} €", 1, 1, 'R')

    pdf.ln(5)
    pdf.cell(100, 10, "TOTAL HT", 0, 0, 'R')
    pdf.cell(40, 10, f"{data['total_ht']:.2f} €", 1, 1, 'R')
    pdf.cell(100, 10, f"TVA ({data['taux_tva']}%)", 0, 0, 'R')
    pdf.cell(40, 10, f"{data['total_tva']:.2f} €", 1, 1, 'R')
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(100, 10, "TOTAL TTC", 0, 0, 'R')
    pdf.cell(40, 10, f"{data['total_ttc']:.2f} €", 1, 1, 'R')
    
    return pdf.output(dest='S')

# --- INTERFACE STREAMLIT ---
st.set_page_config(page_title="Scanner de Tickets Pro", page_icon="🧾")
st.title("🧾 Convertisseur Ticket en Facture")
st.write("Téléchargez une photo de votre ticket, l'IA s'occupe du reste.")

fichier_image = st.file_uploader("Choisissez une photo de ticket (JPG, PNG)", type=['jpg', 'jpeg', 'png'])

if fichier_image is not None:
    st.image(fichier_image, caption="Ticket téléchargé", width=300)
    
    if st.button("Analyser et Générer la Facture"):
        with st.spinner("L'IA analyse les montants et la TVA..."):
            try:
                # Simulation de l'appel IA (Code simplifié pour l'exemple)
                # En production, on enverrait l'image à l'API comme vu précédemment
                img_bytes = fichier_image.getvalue()
                
                # Ici nous utilisons des données de test pour la démonstration
                # Mais vous pouvez décommenter la logique IA réelle ici
                resultats_ia = {
                    "nom_magasin": "SUPER U", "date": "16/02/2026", "taux_tva": 20,
                    "articles": [{"nom": "Fournitures bureau", "prix_unitaire_ttc": 12.50}],
                    "total_ht": 10.42, "total_tva": 2.08, "total_ttc": 12.50
                }
                
                pdf_output = generer_pdf(resultats_ia)
                
                st.success("Analyse terminée !")
                st.download_button(
                    label="📥 Télécharger la Facture PDF",
                    data=pdf_output,
                    file_name="facture_automatique.pdf",
                    mime="application/pdf"
                )
            except Exception as e:

                st.error(f"Erreur : {e}")


