import streamlit as st
import pandas as pd

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Fiche Rappel - Contamination Azote", layout="wide")

# --- 2. CSS PERSONNALISÉ ---
st.markdown("""
<style>
    .main-card {
        border: 1px solid #e6e9ef;
        border-radius: 12px;
        padding: 15px;
        background-color: white;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .img-container {
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f0f2f6;
        border-radius: 8px;
        margin: 5px 0;
        overflow: hidden;
    }
    .img-container img { max-height: 100%; max-width: 100%; object-fit: contain; }
    .product-title { font-size: 0.9rem; font-weight: 800; color: #1f2937; min-height: 35px; margin-top: 5px; }
    .info-text { font-size: 0.8rem; margin-bottom: 4px; }
    .card-button {
        background-color: #FF4B4B;
        color: white !important;
        text-align: center;
        padding: 8px;
        border-radius: 6px;
        font-weight: bold;
        text-decoration: none;
        display: block;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. FONCTIONS DE TRAITEMENT ---
@st.cache_data(ttl=3600)
def load_data_by_motif(): 
    url = "https://www.data.gouv.fr/fr/datasets/r/5a4e7174-657c-4920-af1f-3440a996837c"
    try:
        df = pd.read_csv(url, sep=';', on_bad_lines='skip', encoding='utf-8', low_memory=False)
        
        # Filtre Alimentation strict
        df = df[df['categorie_produit'].str.contains("Alimentation", case=False, na=False)]
        
        # Filtre Motif strict
        cible = "oxyde d'éthylène|ethylene oxide|éthylène" 
        mask_motif = df['motif_rappel'].str.contains(cible, case=False, na=False)
        mask_risque = df['risques_encourus'].str.contains(cible, case=False, na=False)
        
        df_filtered = df[mask_motif | mask_risque].copy()
        df_filtered['date_pub'] = pd.to_datetime(df_filtered['date_publication'], errors='coerce')
        
        return df_filtered.sort_values(by='date_pub', ascending=False)
        
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return pd.DataFrame()

def normaliser_motif(motif, risque):
    m = str(motif).lower()
    r = str(risque).lower()
    if "oxyde d'éthylène" in m or "ethylene oxide" in m or "éthylène" in r: 
        return "Contamination à l'oxyde d'éthylène"
    return "Autre motif"

# --- 4. NAVIGATION ---
if st.button("⬅️ Retour à l'accueil", type="primary"):
    st.switch_page("rappelconso.py")

st.title("Focus : :red[Contamination à l'oxyde d'éthylène]")
st.divider()

# --- 5. STRUCTURE EN COLONNES ---
col_gauche, col_droite = st.columns([2, 1])

with col_gauche:
    st.error("**Niveau de gravité : 4/4**")
    with st.container(border=True):
        st.markdown("### 🔍 Comprendre ce risque")
        st.info("""
        L’oxyde d’éthylène est un gaz utilisé pour la désinfection de certaines matières premières
        agricoles (épices, graines, additifs). En Europe, son utilisation est interdite.
        La présence de l’oxyde d’éthylène ne provient généralement pas de l'aliment en lui-même. La contamination 
        est souvent liée à des ajouts d’additifs ou d’ingrédients (épices, arômes). Le risque immédiat pour 
        le consommateur reste faible.
        """)
        
        st.write("""
        **Risques pour la santé :**
        Selon la dose et la durée d’exposition, les risques peuvent être différents. Les effets principaux sont des 
        irritations des yeux, de la peau et des voies respiratoires, des maux de têtes, nausées et vomissements et 
        des effets toxiques sur le système nerveux (à forte dose, cas rare). A long terme, il est classé comme cancérogène.
        """)
        
        st.markdown("""
        **Conduite à tenir :**
        * ✅ Ne plus consommer le produit
        * 🔙 Ramener le produit au point de vente (ou le jeter)
        * 😷 Surveiller l'apparition de symptômes
        * 👨‍⚕️ Consulter un médecin en cas d'apparition de symptômes
        """)
        
        # Bloc d'urgence
        st.markdown("""
        **⚠️ Numéros utiles :**
        * ☎️ **Centre antipoison :** 0 800 59 59 59 (appel gratuit)
        * 🚑 **Samu :** 15
        * 🚒 **Pompiers :** 18
        * 🆘 **Numéro d’urgence européen :** 112
        """)
        
        st.markdown("""
        **Sources :**
        * Centre de lutte contre le cancer Leon Berard, 2025. Oxyde d’éthylène et effets sur la santé • Cancer Environnement. Date de consultation : 16/04/2026. Disponible sur : <https://www.cancer-environnement.fr/fiches/expositions-environnementales/oxyde-dethylene/>.
        * Commission Européenne, 2022. Règlement n° 231/2012. Date de consultation : 16/04/2026. Disponible sur : <https://ec.europa.eu/transparency/comitology-register/core/api/integration/ers/318129/080145/3/attachment>.
        * INRS, 2022. Oxyde d’éthylène (FT 70). Généralités - Fiche toxicologique - INRS. Date de consultation : 16/04/2026. Disponible sur : <https://www.inrs.fr/publications/bdd/fichetox/fiche.html?refINRS=FICHETOX_70>.
        * Ministère de l’Economie, des Finances et de la Relance Rappels de crèmes glacées. Date de consultation : 16/04/2026. Disponible sur : <https://www.economie.gouv.fr/files/files/directions_services/dgccrf/media-document/dgccrf_presse_CP-ETO-glace.pdf>.
        """)


with col_droite:
    st.markdown("### 📢 Derniers rappels")
    st.warning("⚠️ Rappel important : Si vous possédez l'un de ces produits, ne le consommez pas et rapportez-le au point de vente")
    data_rappels = load_data_by_motif()
    
    if not data_rappels.empty:
        top_3 = data_rappels.head(3)
        placeholder = "https://img.freepik.com/vecteurs-premium/icone-erreur-chargement-image-indisponible-absent-signe-fleche-cycle-format-jpg-pour-conception-site-web-application-mobile-graphique-vectoriel_748571-293.jpg"

        for _, row in top_3.iterrows():
            # On utilise la fonction de normalisation
            motif_propre = normaliser_motif(row.get('motif_rappel', ''), row.get('risques_encourus_par_le_consommateur', ''))
            
            raw_img = str(row.get('liens_vers_les_images', '')).replace('|', ' ').split()
            img_url = raw_img[0] if (raw_img and "http" in raw_img[0]) else placeholder
            
            # Détection de la marque ou du modèle pour le titre
            titre_produit = row.get('nom_produit', row.get('modeles_ou_references', 'Produit'))

            categorie_clean = (row['sous_categorie_produit'][:40] + '..') if len(row['sous_categorie_produit']) > 40 else row['sous_categorie_produit']
            
            st.markdown(f"""
                <div class="main-card">
                    <div style="display: flex; justify-content: space-between; color: #6b7280; font-size: 0.7rem; font-weight: bold;">
                        <span>🗓️ {row['date_pub'].strftime('%d/%m/%Y') if pd.notnull(row['date_pub']) else 'N/A'}</span>
                        <span style="color: #f59e0b;">📂 {categorie_clean}</span>
                    </div>
                    <div class="img-container"><img src="{img_url}" onerror="this.src='{placeholder}';"></div>
                    <div class="product-title">{str(titre_produit)[:50]}</div>
                    <div class="info-text"><b>🛒 Magasin :</b> {str(row.get('distributeurs', 'N/A'))[:50]}...</div>
                    <div class="info-text"><b>⚠️ Motif :</b> {motif_propre}</div>
                    <a href="{row.get('lien_vers_affichette_pdf', '#')}" target="_blank" class="card-button">VOIR DÉTAILS</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Aucun rappel récent trouvé pour contamination à l'oxyde d'éthylène.")

st.divider()