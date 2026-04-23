import streamlit as st
import pandas as pd

# 1. CONFIGURATION
st.set_page_config(page_title="Consom'Able", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS PERSONNALISÉ
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
   
    /* Bouton Qui sommes-nous */
    .about-button {
        position: absolute;
        top: 50px;
        right: 30px;
        background-color: #f0f2f6;
        color: #1f2937 !important;
        padding: 8px 16px;
        border-radius: 20px;
        text-decoration: none !important;
        font-weight: bold;
        font-size: 1rem;
        border: 1px solid #e6e9ef;
        transition: background-color 0.3s;
        z-index: 1000;
    }
    .about-button:hover {
        background-color: #e6e9ef;
        text-decoration: none;
    }

    .main-card {
        border: 1px solid #e6e9ef;
        border-radius: 12px;
        padding: 15px 20px;
        background-color: white;
        height: 460px;
        display: flex;
        flex-direction: column;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
   
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #6b7280;
        font-weight: bold;
        font-size: 0.85rem;
        margin-bottom: 15px;
    }

    .category-label {
        color: #f59e0b;
        font-weight: bold;
    }

    .img-container {
        height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f0f2f6;
        border-radius: 8px;
        margin: 5px 0 10px 0;
        overflow: hidden;
    }
   
    .img-container img { max-height: 100%; max-width: 100%; object-fit: contain; }
   
    .product-title {
        font-size: 1.1rem;
        font-weight: 800;
        line-height: 1.2;
        color: #1f2937;
        min-height: 55px;
        margin-bottom: 10px;
        overflow: hidden;
    }
   
    .info-text { font-size: 0.9rem; margin-bottom: 6px; line-height: 1.3; color: #374151; }
   
    .motif-link {
        color: #FF4B4B !important;
        text-decoration: none;
        font-weight: bold;
    }
    .motif-link:hover {
        text-decoration: underline;
    }

    .card-button {
        background-color: #FF4B4B;
        color: white !important;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        font-weight: bold;
        text-decoration: none;
        display: block;
        margin-top: auto;
    }
</style>
""", unsafe_allow_html=True)

# Bouton de navigation "Qui sommes-nous"
st.markdown('<a href="/nous" target="_self" class="about-button"> Qui sommes-nous ❓</a>', unsafe_allow_html=True)

# 3. MAPPING DES PAGES ET URLs
pages_motifs = {
    "Allergènes non mentionnés": "pages/allergènes.py",
    "Contamination à l'oxyde d'éthylène": "pages/éthylène.py",
    "Contamination chimique / Métaux lourds": "pages/métaux_lourds.py",
    "Contamination chimique à l'azote (abvt)": "pages/abvt.py",
    "Défaut de fabrication": "pages/défaut_fab.py",
    "Mauvaise DLC / étiquetage": "pages/DLC.py",
    "Présence d'E.coli": "pages/e_coli.py",
    "Présence d'histamine": "pages/histamine.py",
    "Présence de corps étrangers": "pages/corps_étrangers.py",
    "Présence de Listeria": "pages/listeria.py",
    "Présence de moisissures": "pages/moisissures.py",
    "Présence de norovirus": "pages/norovirus.py",
    "Présence de Salmonelle": "pages/salmonella.py",
    "Présence de staphylocoques": "pages/staph.py",
    "Présence de vibrio": "pages/vibrio.py",
    "Rupture de la chaîne du froid": "pages/chaîne_froid.py"
}

urls_motifs = {nom: "/" + chemin.replace("pages/", "").replace(".py", "") for nom, chemin in pages_motifs.items()}

mapping_types = {
    "Céréales et produits de boulangerie": "pages/céréales.py",
    "Plats préparés et snacks": "pages/plats_préparés.py",
    "Produits de la pêche": "pages/pêche.py",
    "Produits laitiers": "pages/lait.py",
    "Viande": "pages/viande.py"
}

# 4. FONCTIONS DE TRAITEMENT (MODIFIÉE)
def normaliser_motif(motif, risque):
    texte_analyse = f"{str(motif)} {str(risque)}".lower()
   
    # --- AJOUT DE LA LOGIQUE DE DÉTECTION PRIORITAIRE ---
    # On vérifie d'abord les métaux lourds pour éviter qu'ils soient pris pour des corps étrangers (métal)
    metaux_lourds = ["plomb", "mercure", "cadmium", "arsenic", "métaux lourds"]
    if any(m in texte_analyse for m in metaux_lourds):
        return "Contamination chimique / Métaux lourds"

    categories = {
        "listeria": "Présence de Listeria",
        "listéria": "Présence de Listeria",
        "salmonelle": "Présence de Salmonelle",
        "salmonella": "Présence de Salmonelle",
        "e. coli": "Présence d'E.coli",
        "escherichia": "Présence d'E.coli",
        "éthylène": "Contamination à l'oxyde d'éthylène",
        "corps étranger": "Présence de corps étrangers",
        "verre": "Présence de corps étrangers",
        "métal": "Présence de corps étrangers",
        "allerg": "Allergènes non mentionnés",
        "histamine": "Présence d'histamine",
        "moisissure": "Présence de moisissures",
        "staphylocoque": "Présence de staphylocoques",
        "froid": "Rupture de la chaîne du froid",
        "étiquetage": "Mauvaise DLC / étiquetage",
        "dlc": "Mauvaise DLC / étiquetage",
        "fabrication": "Défaut de fabrication",
        "vibrio" : "Présence de vibrio"
    }
    for cle, libelle in categories.items():
        if cle in texte_analyse: return libelle
    return "Autre motif"

@st.cache_data
def load_and_process_data():
    url = "https://www.data.gouv.fr/fr/datasets/r/5a4e7174-657c-4920-af1f-3440a996837c"
    df = pd.read_csv(url, sep=';', on_bad_lines='skip')
    df = df[df['categorie_produit'].str.contains("alimentatio", case=False, na=False)].copy()
    df['motif_normalise'] = df.apply(lambda row: normaliser_motif(row.get('motif_rappel', ''), row.get('risques_encourus', '')), axis=1)
    df['date_publication'] = pd.to_datetime(df['date_publication'])
    df = df.sort_values(by='date_publication', ascending=False).fillna("")
    df['date_publication_clean'] = df['date_publication'].dt.strftime('%d/%m/%Y')
    return df.head(3)

# --- INTERFACE (TITRE + NAVIGATION) ---
st.title("🛡️ :red[Consom']Able")
st.subheader("Dashboard principal")
st.divider()

col_filtre1, col_filtre2 = st.columns(2)

with col_filtre1:
    type_produit = st.selectbox("🍎 Type de produit", ["Choisir un type de produit"] + list(mapping_types.keys()))
    if type_produit in mapping_types:
        st.switch_page(mapping_types[type_produit])

with col_filtre2:
    motif_choisi = st.selectbox("⚠️ Motif de rappel", ["Choisir un motif de rappel"] + list(pages_motifs.keys()))
    if motif_choisi in pages_motifs:
        st.switch_page(pages_motifs[motif_choisi])

st.write("")

# --- DERNIERS RAPPELS RÉELS ---
st.markdown("### 📢 :red[Les 3 derniers rappels en temps réel]")

try:
    top_3 = load_and_process_data()
    cols = st.columns(3)
    placeholder = "https://img.freepik.com/vecteurs-premium/icone-erreur-chargement-image-indisponible-absent-signe-fleche-cycle-format-jpg-pour-conception-site-web-application-mobile-graphique-vectoriel_748571-293.jpg"

    for i, (index, row) in enumerate(top_3.iterrows()):
        with cols[i]:
            img_list = str(row['liens_vers_les_images']).replace('|', ' ').split()
            image_url = img_list[0] if img_list and "http" in img_list[0] else placeholder
           
            cat = str(row['sous_categorie_produit'])
            categorie_clean = (cat[:40] + '...') if len(cat) > 40 else cat

            motif_nom = row['motif_normalise']
            lien_page_motif = urls_motifs.get(motif_nom, "#")

            st.markdown(f"""
                <div class="main-card">
                    <div class="card-header">
                        <span>🗓️ {row['date_publication_clean']}</span>
                        <span class="category-label">📂 {categorie_clean}</span>
                    </div>
                    <div class="img-container">
                        <img src="{image_url}">
                    </div>
                    <div class="product-title">{str(row['modeles_ou_references'])[:60]}</div>
                    <div class="info-text">
                        ⚠️ <b>Motif :</b>
                        <a href="{lien_page_motif}" target="_self" class="motif-link">{motif_nom}</a>
                    </div>
                    <div class="info-text" style="color: #6b7280;">
                        🛒 <b>Magasin :</b> {str(row['distributeurs'])[:45]}
                    </div>
                    <a href="{row['lien_vers_affichette_pdf']}" target="_blank" class="card-button">VOIR DÉTAILS</a>
                </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Erreur de connexion : {e}")

st.divider()
st.info("Source : Données officielles de l'API Rappel Conso (Gouvernement Français)")