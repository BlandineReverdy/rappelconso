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
        cible = "corps étranger|verre|métal|plastique|caillou|insecte"
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
    if "métal" in m or "corps étrangers" in m or "verre" in r or "plastique" in r or "caillou" in r or "insecte" in r: 
        return "Présence de corps étrangers"
    return "Autre motif"

# --- 4. NAVIGATION ---
if st.button("⬅️ Retour à l'accueil", type="primary"):
    st.switch_page("rappelconso.py")

st.title("Focus : :red[Présence de corps étrangers]")
st.divider()

# --- 5. STRUCTURE EN COLONNES ---
col_gauche, col_droite = st.columns([2, 1])

with col_gauche:
    st.error("**Niveau de gravité : 3/4**")
    with st.container(border=True):
        st.markdown("### 🔍 Comprendre ce risque")
        st.info("""
        Lorsqu'un produit est rappelé pour "corps étranger", cela signifie qu'un élément qui n'a rien à faire dans la recette a été détecté. Il peut s'agir 
        d'un objet inerte ou d'un organisme vivant.
        Dans le cas d'un objet inerte, il peut s'agir de fragments de verre, des copeaux métalliques, des morceaux de plastique dur ou des petits cailloux 
        introduits accidentellement lors de la récolte ou de la fabrication.
        Dans le cas d'un organisme vivant, il peut s'agir de d'insectes (mites alimentaires, charançons) ou de parasites naturels (ex: Anisakis dans le poisson).
        """)
       
        st.write("""
        **Risques pour la santé :**
        Dans le cas d'objet inerte, il y a un risque de lésions buccales, de coupures dans l'œsophage ou l'estomac, ou de perforation digestive,
        et un risque d'étouffement chez les enfants.
        Dans le cas d'un organisme vivant, il y a un risque allergique, troubles digestifs (nausées, vomissements liés au dégoût ou aux toxines) 
        ou infection parasitaire selon l'espèce.
        """)
       
        st.markdown("""
        **Conduite à tenir :**
        En cas d'objet inerte :
        * ✅ Ne plus consommer le produit
        * 🔙 Ramener le produit au point de vente (ou le jeter)
        * 😷 Surveiller l'apparition de douleurs abdominales, de difficultés à avaler ou de sang
        * 👨‍⚕️ Consulter un médecin si l'objet était tranchant ou si une gêne persiste
        * ❌ Ne pas essayer de se faire vomir
        
        En cas d'organisme vivant :
        * ✅ Ne plus consommer le produit
        * 🔙 Ramener le produit au point de vente (ou le jeter)
        * 😷 Surveiller d'éventuels symptômes digestifs inhabituels dans les jours qui suivent
        * 👨‍⚕️ Contacter un centre antipoison si un doute persiste
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
        * Parlement Européen, Conseil de l’Union Européenne Règlement (CE) n° 178/2022. Date de consultation : 16/04/2026. Disponible sur : <https://www.economie.gouv.fr/files/files/directions_services/dgccrf/securite/produits_alimentaires/controles_importation/rglt178_2002_consolide.pdf>.
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
        st.info("Aucun rappel récent trouvé pour présence de corps étrangers.")

st.divider()