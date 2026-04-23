import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="Qui sommes nous ?", layout="wide")

st.write("") # Ligne vide
st.write("") # Ligne vide

# -----------------------------
# Fonction pour afficher une image en HTML
# -----------------------------
def image_to_base64(image_path):
    path = Path(image_path)
    if not path.exists():
        return None

    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    suffix = path.suffix.lower()
    if suffix == ".png":
        mime = "image/png"
    elif suffix in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    else:
        mime = "application/octet-stream"

    return f"data:{mime};base64,{encoded}"

# -----------------------------
# Données équipe
# -----------------------------
membres = [
    {
        "prenom": "Baptiste",
        "nom": "HUTEAU",
        "photo": "pages/Photos/Photo_HUTEAU_Baptiste.jpg",
        "linkedin": "https://www.linkedin.com/in/baptiste-huteau-142aba353/"
    },
    {
        "prenom": "Soline",
        "nom": "LEJEUNE",
        "photo": "pages/Photos/Photo_LEJEUNE_Soline.jpg",
        "linkedin": "https://www.linkedin.com/in/soline-lejeune-081514352/"
    },
    {
        "prenom": "Aloïs",
        "nom": "MAILLARD",
        "photo": "pages/Photos/Photo_MAILLARD_Aloïs.jpeg",
        "linkedin": "https://www.linkedin.com/in/alo%C3%AFs-maillard-772a19252/"
    },
    {
        "prenom": "Lou-Anne",
        "nom": "MERCIER",
        "photo": "pages/Photos/Photo_MERCIER_Lou-Anne.jpg",
        "linkedin": "https://www.linkedin.com/in/lou-anne-mercier-a27527251/"
    },
    {
        "prenom": "Blandine",
        "nom": "REVERDY",
        "photo": "pages/Photos/Photo_REVERDY_Blandine.jpg",
        "linkedin": "https://www.linkedin.com/in/blandine-reverdy-97a273263/"
    },
]

remerciements_personnes = [
    {
        "prenom": "Sofia",
        "nom": "NESTORA",
        "photo": "pages/Photos/Photo_Sofia.jpg",
        "linkedin": "https://www.linkedin.com/in/sofia-nestora-45603a75/"
    },
    {
        "prenom": "Hamilton",
        "nom": "DE ARAUJO",
        "photo": "pages/Photos/Photo_Hamilton.jpg",
        "linkedin": "https://www.linkedin.com/in/hamiltonaraujo/"
    },
]

texte_projet = """
Ce site est le résultat de notre projet de semestre. L’objectif de la démarche est de vulgariser et de rendre accessible la plateforme <a href="https://rappel.conso.gouv.fr/" target="_blank">RappelConso</a>  afin qu’un consommateur lambda puisse être averti et conscient des risques liés à son alimentation. Pour cela, il faut un site internet ludique et instinctif, lié aux données de la base et possédant une boîte à outils pour trouver des informations précises et expliquer les bons comportements à adopter.
C’est ainsi qu’il a été décidé de réaliser une plateforme en ligne regroupant en temps réel les informations principales de la plateforme RappelConso. Il est possible d’y retrouver le nom du produit concerné, sa photo, ainsi que le motif du rappel, tout en lui offrant un visuel plus accessible et compréhensible.
""".strip()

texte_remerciements = """
Nous souhaitons adresser nos sincères remerciements à <b>Madame Sofia NESTORA</b> et <b>Monsieur Hamilton DE ARAUJO</b>, nos deux tuteurs de projet, pour leur accompagnement tout au long de ce travail. Leur disponibilité, la pertinence de leurs conseils ainsi que la richesse de leurs expertises ont été essentielles pour orienter nos réflexions et assurer la réussite de ce projet.
Nous remercions tout particulièrement <b>Madame NESTORA</b> pour son aide précieuse dans la compréhension de la base de données RappelConso, ainsi que pour son suivi régulier et attentif.
Nous exprimons également notre gratitude à <b>Monsieur DE ARAUJO</b> pour son accompagnement dans le développement de notre code et la création du site associé, ainsi que pour ses idées constructives et son soutien constant.
""".strip()

# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1350px;
        margin: auto;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .accueil-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 70vh;
    }

    .titre-page {
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 25px;
    }

    .texte-equipe {
        text-align: center;
        font-size: 18px;
        line-height: 1.6;
        margin-bottom: 28px;
    }

    .boite-projet {
        width: 100%;
        background-color: #ffffff;
        border: 1px solid #d9d9d9;
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 30px;
        font-size: 17px;
        line-height: 1.7;
        text-align: justify;
        white-space: pre-line;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        box-sizing: border-box;
    }

    .boite-remerciements {
        width: 100%;
        background-color: #ffffff;
        border: 1px solid #d9d9d9;
        border-radius: 14px;
        padding: 22px 24px;
        margin-bottom: 30px;
        font-size: 17px;
        line-height: 1.7;
        text-align: justify;
        white-space: pre-line;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        box-sizing: border-box;
    }

    .nom-box {
        width: 100%;
        min-height: 90px;
        background-color: #ffffff;
        border: 1px solid #d9d9d9;
        border-radius: 12px;
        padding: 12px 8px;
        text-align: center;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 12px;
        line-height: 1.5;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        box-sizing: border-box;
    }

    .nom-box a {
        text-decoration: none;
        color: inherit;
    }

    .nom-box a:hover {
        color: #0A66C2;
        text-decoration: underline;
    }

    .photo-frame {
        width: 100%;
        border-radius: 10px;
        overflow: hidden;
        background-color: #fafafa;
        box-sizing: border-box;
        margin-bottom: 18px;
    }

    .photo-frame img {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 10px;
    }

    .photo-placeholder {
        width: 100%;
        height: 270px;
        border: 1px dashed #bdbdbd;
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #777777;
        font-size: 15px;
        background-color: #fafafa;
        box-sizing: border-box;
        margin-bottom: 18px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-size: 20px;
        font-weight: 600;
        padding: 0.8rem 1.5rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Crée deux colonnes pour l'en-tête
col_back, col_logo = st.columns([1, 1])

with col_back:
    # La fonction switch_page permet de retourner au fichier principal
    if st.button("⬅️ RETOUR À L'ACCUEIL", type="primary"):
        st.switch_page("rappelconso.py")

with col_logo:
    logo_data = image_to_base64("pages/Photos/logo.png")
    if logo_data:
        st.markdown(f'<div style="text-align: right;"><img src="{logo_data}" style="width:250px;"></div>', unsafe_allow_html=True)

st.divider() 

# -----------------------------
# Titre
# -----------------------------
st.markdown('<div class="titre-page">Qui sommes nous ?</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="texte-equipe">
        Nous sommes 5 étudiants ingénieurs en Agroalimentation et santé à
        <a href="https://www.unilasalle.fr/" target="_blank">UniLaSalle Beauvais</a>
        dans le parcours métier <b>"Piloter la production et garantir la qualité des produits"</b>.
    </div>
    """,
    unsafe_allow_html=True
)

    # -----------------------------
    # Description projet
    # -----------------------------
st.markdown(
    f"""
    <div class="boite-projet">
        {texte_projet}
    </div>
    """,
    unsafe_allow_html=True
)

cols = st.columns(5, gap="medium")

for col, membre in zip(cols, membres):
    with col:
        st.markdown(
            f"""
            <div class="nom-box">
                <div>
                    <a href="{membre["linkedin"]}" target="_blank">
                        {membre["prenom"]}
                    </a>
                </div>
                <div>
                    <a href="{membre["linkedin"]}" target="_blank">
                        {membre["nom"]}
                    </a>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if membre["photo"]:
            photo_data = image_to_base64(membre["photo"])
            if photo_data:
                st.markdown(
                    f"""
                    <div class="photo-frame">
                        <img src="{photo_data}" alt="{membre['prenom']} {membre['nom']}">
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    '<div class="photo-placeholder">Photo introuvable</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div class="photo-placeholder">Photo à ajouter</div>',
                unsafe_allow_html=True
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # -----------------------------
    # Remerciements
    # -----------------------------
    st.markdown('<div class="titre-page">Remerciements</div>', unsafe_allow_html=True)

    col_texte, col_personnes = st.columns([2, 1.2], gap="large")

    with col_texte:
        st.markdown(
            f"""
            <div class="boite-remerciements">
                {texte_remerciements}
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_personnes:
        cols_photos = st.columns(2, gap="small")

        for col, personne in zip(cols_photos, remerciements_personnes):
            with col:
                st.markdown(
                    f"""
                    <div class="nom-box">
                        <div>
                            <a href="{personne["linkedin"]}" target="_blank">
                                {personne["prenom"]}
                            </a>
                        </div>
                        <div>
                            <a href="{personne["linkedin"]}" target="_blank">
                                {personne["nom"]}
                            </a>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if personne["photo"]:
                    photo_data = image_to_base64(personne["photo"])
                    if photo_data:
                        st.markdown(
                            f"""
                            <div class="photo-frame">
                                <img src="{photo_data}" alt="{personne['prenom']} {personne['nom']}">
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            '<div class="photo-placeholder">Photo introuvable</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown(
                        '<div class="photo-placeholder">Photo à ajouter</div>',
                        unsafe_allow_html=True
                    )