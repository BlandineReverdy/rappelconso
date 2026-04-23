import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Focus Céréales et Boulangerie", page_icon="🥖", layout="wide")

# --- AJOUT D'ESPACE POUR QUE LE BOUTON SOIT VISIBLE ---
st.write("") # Ligne vide
st.write("") # Ligne vide
st.write("") # Ligne vide
st.write("") # Ligne vide

# --- 2. CSS PERSONNALISÉ (Inclus le style pour les liens et l'alignement) ---
st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    .main-card {
        border: 1px solid #e6e9ef;
        border-radius: 12px;
        padding: 15px;
        background-color: white;
        margin-bottom: 20px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        display: flex;
        flex-direction: column;
        height: 350px; /* Fixe la hauteur pour l'alignement comme sur le modèle viande */
    }
    .img-container {
        height: 150px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f0f2f6;
        border-radius: 8px;
        margin: 5px 0;
        overflow: hidden;
    }
    .img-container img { max-height: 100%; max-width: 100%; object-fit: contain; }
    .product-title { font-size: 1rem; font-weight: 800; color: #1f2937; min-height: 45px; margin-top: 5px; }
    .info-text { font-size: 0.85rem; margin-bottom: 4px; }
   
    /* Style spécifique pour les liens motifs */
    .motif-link {
        color: #FF4B4B !important;
        text-decoration: none;
        font-weight: bold;
    }
    .motif-link:hover { text-decoration: underline; }

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
        margin-top: auto;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. MAPPING DES PAGES (Élément manquant ajouté) ---
pages_motifs = {
    "Allergènes non mentionnés": "pages/allergènes.py",
    "Contamination à l'oxyde d'éthylène": "pages/éthylène.py",
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

# --- 4. FONCTIONS DE TRAITEMENT ---
@st.cache_data(ttl=3600)
def load_all_data():
    url = "https://www.data.gouv.fr/fr/datasets/r/5a4e7174-657c-4920-af1f-3440a996837c"
    try:
        df = pd.read_csv(url, sep=';', on_bad_lines='skip', encoding='utf-8', low_memory=False)
        cible = "céréales|boulangerie"
        mask = df['sous_categorie_produit'].str.contains(cible, case=False, na=False)
        return df[mask].copy()
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return pd.DataFrame()

def normaliser_motif(motif, risque):
    m = str(motif).lower()
    r = str(risque).lower()
    if "listeria" in m or "listeria" in r: return "Présence de Listeria"
    if "salmonelle" in m or "salmonella" in m or "salmonelle" in r: return "Présence de Salmonelle"
    if "e. coli" in m or "escherichia" in m or "e. coli" in r: return "Présence d'E.coli"
    if "oxyde d'éthylène" in m or "ethylene oxide" in m or "éthylène" in m: return "Contamination à l'oxyde d'éthylène"
    if any(x in m or x in r for x in ["corps étranger", "verre", "métal", "plastique", "caillou"]): return "Présence de corps étrangers"
    if "allerg" in m or "allerg" in r: return "Allergènes non mentionnés"
    if "histamine" in m or "histamine" in r: return "Présence d'histamine"
    if "moisissure" in m or "moisi" in m: return "Présence de moisissures"
    if "staphylocoque" in m or "staphylococcus" in m: return "Présence de staphylocoques"
    if "norovirus" in m: return "Présence de norovirus"
    if "vibrio" in m: return "Présence de vibrio"
    if "azote" in m: return "Contamination chimique à l'azote (abvt)"
    if "froid" in m or "température" in m: return "Rupture de la chaîne du froid"
    if "étiquetage" in m or "dlc" in m or "dluo" in m: return "Mauvaise DLC / étiquetage"
    if "fabrication" in m or "conception" in m: return "Défaut de fabrication"
    return "Autre motif"

# --- 5. EN-TÊTE ---
col_back, col_title_header = st.columns([1, 4])
with col_back:
    if st.button("⬅️ RETOUR À L'ACCUEIL", type="primary", width='stretch'):
        st.switch_page("rappelconso.py")

with col_title_header:
    st.title("🥖 Focus : :red[Céréales et Boulangerie]")

st.divider()

# --- 6. CHARGEMENT ET LOGIQUE ---
data_fish = load_all_data()

if not data_fish.empty:
    data_fish['Categorie_Rappel'] = data_fish.apply(
        lambda x: normaliser_motif(x['motif_rappel'], x.get('risques_encourus_par_le_consommateur', '')),
        axis=1
    )
    data_fish['date_pub'] = pd.to_datetime(data_fish['date_publication'], errors='coerce')

    col_graph, col_last_news = st.columns([2, 1])

    with col_graph:
        st.subheader("📊 Analyses statistiques")
       
        with st.expander("🔎 Outils de Filtrage - Affinez votre analyse", expanded=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                recherche_texte = st.text_input("Recherche libre (ex: Pain, Biscuits, Carrefour...)", "")
                risques_disponibles = sorted(data_fish['Categorie_Rappel'].unique())
                risques_selectionnes = st.multiselect("Filtrer par Risque", options=risques_disponibles, default=risques_disponibles)

        # Application filtres
        df_filtered = data_fish.copy()
        if recherche_texte:
            mask_text = df_filtered.astype(str).apply(lambda x: x.str.contains(recherche_texte, case=False)).any(axis=1)
            df_filtered = df_filtered[mask_text]
        df_filtered = df_filtered[df_filtered['Categorie_Rappel'].isin(risques_selectionnes)]

        # Calcul de métriques
        repartition = df_filtered['Categorie_Rappel'].value_counts().reset_index()
        repartition.columns = ['Motif', 'Nombre']
        total_rappels = repartition['Nombre'].sum()
       
        if total_rappels > 0:
            motif_principal = repartition.iloc[0]['Motif']
            pourcentage_principal = round((repartition.iloc[0]['Nombre'] / total_rappels) * 100, 1)
           
            m_col1, m_col2, m_col3 = st.columns(3)
            m_col1.metric("Rappels (filtrés)", f"{total_rappels} 📦")
            m_col2.metric("Danger N°1", f"{motif_principal}")
            m_col3.metric("Part du danger N°1", f"{pourcentage_principal}%")
            
            st.info("💡 **Interactivité :** Cliquez sur **'Autres risques'** pour zoomer. Bouton de retour au centre.")

            tab1, tab2 = st.tabs(["📌 Répartition des risques", "📈 Évolution"])
           
            with tab1:
                noms, parents, valeurs = ["Tous les produits"], [""], [total_rappels]
                top_4_motifs = repartition['Motif'].head(4).tolist()
                for motif in top_4_motifs:
                    val = repartition[repartition['Motif'] == motif]['Nombre'].sum()
                    if val > 0:
                        noms.append(motif); parents.append("Tous les produits"); valeurs.append(val)
                autres_df = repartition[~repartition['Motif'].isin(top_4_motifs)]
                val_autres = autres_df['Nombre'].sum()
                if val_autres > 0:
                    noms.append("Autres risques"); parents.append("Tous les produits"); valeurs.append(val_autres)
                    for _, row in autres_df.iterrows():
                        noms.append(row['Motif']); parents.append("Autres risques"); valeurs.append(row['Nombre'])
               
                fig_sunburst = px.sunburst(names=noms, parents=parents, values=valeurs, branchvalues="total", color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_sunburst.update_traces(maxdepth=2, textinfo='label+percent parent')
                st.plotly_chart(fig_sunburst, width='stretch')
            with tab2:
                df_filtered['Mois'] = df_filtered['date_pub'].dt.tz_localize(None).dt.to_period('M').dt.to_timestamp()
                evo = df_filtered.groupby(['Mois', 'Categorie_Rappel']).size().reset_index(name='nb')
                fig_bar = px.bar(evo, x='Mois', y='nb', color='Categorie_Rappel', barmode='stack', color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig_bar, width='stretch')
        else:
            st.warning("Aucun résultat pour ces filtres.")

    with col_last_news:
        st.subheader("🚨 3 Derniers rappels")
        st.warning("⚠️ Rappel important : Si vous possédez l'un de ces produits, ne le consommez pas et rapportez-le au point de vente")
       
        top_3 = data_fish.sort_values(by='date_pub', ascending=False).head(3)
        placeholder = "https://img.freepik.com/vecteurs-premium/icone-erreur-chargement-image-indisponible-absent-signe-fleche-cycle-format-jpg-pour-conception-site-web-application-mobile-graphique-vectoriel_748571-293.jpg"

        for _, row in top_3.iterrows():
            raw_img = str(row.get('liens_vers_les_images', '')).replace('|', ' ').split()
            img_url = raw_img[0] if (raw_img and "http" in raw_img[0]) else placeholder
           
            # LOGIQUE DU LIEN CLIQUABLE
            motif_nom = row.get('Categorie_Rappel', 'Autre motif')
            lien_page_motif = urls_motifs.get(motif_nom, "#")
           
            st.markdown(f"""
                <div class="main-card">
                    <div style="display: flex; justify-content: space-between; color: #6b7280; font-size: 0.75rem; font-weight: bold;">
                        <span>🗓️ {row['date_pub'].strftime('%d/%m/%Y') if pd.notnull(row['date_pub']) else 'NA'}</span>
                        <span style="color: #f59e0b;">📂 BOULANGERIE</span>
                    </div>
                    <div class="img-container"><img src="{img_url}" onerror="this.src='{placeholder}';"></div>
                    <div class="product-title">{str(row.get('modeles_ou_references', 'Produit'))[:50]}...</div>
                    <div class="info-text">
                        ⚠️ <b>Motif :</b>
                        <a href="{lien_page_motif}" target="_self" class="motif-link">{motif_nom}</a>
                    </div>
                    <div class="info-text" style="color: #4b5563; height: 40px; overflow: hidden;">
                        🛒 <b>Magasin :</b> {str(row.get('distributeurs', 'N/A'))[:60]}
                    </div>
                    <a href="{row.get('lien_vers_affichette_pdf', '#')}" target="_blank" class="card-button">VOIR DÉTAILS</a>
                </div>
            """, unsafe_allow_html=True)
else:
    st.error("Impossible de charger les données.")