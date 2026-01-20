import requests
import streamlit as st
from datetime import datetime

API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "local-model"  # LM Studio accepte généralement ce nom

PROMPT_SYSTEME = """
Tu es un agent explicatif spécialisé dans l’intelligence artificielle appliquée au secteur de la santé.

Ton rôle est d’expliquer de manière pédagogique et structurée des concepts liés aux modèles de langage de grande taille (LLM) et à leurs usages en santé.

Règles strictes :
- Tu ne dois PAS fournir de diagnostic médical.
- Tu ne dois PAS donner de conseil clinique.
- Tu ne dois PAS interpréter de données réelles de patients.
- Tu dois adopter un ton neutre, prudent et informatif.
- Tu dois répondre uniquement sous forme de points (bullet points).
- Tu dois toujours mentionner les limites et les risques.

Structure obligatoire de la réponse :
1. Définition courte du concept
2. Pourquoi ce concept est important dans le secteur de la santé
3. Principaux risques ou limites
4. Exemple simple et fictif (non clinique)
5. Rappel que cet outil est une aide et non un système de décision médicale
""".strip()


def appeler_llm(question: str, temperature: float = 0.3, max_tokens: int = 500) -> str:
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": PROMPT_SYSTEME},
            {"role": "user", "content": question}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    r = requests.post(API_URL, json=payload, timeout=120)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]


st.set_page_config(page_title="Agent explicatif santé (LLM)", page_icon="🩺", layout="centered")

st.title("🩺 Agent explicatif santé (LLM)")
st.caption("Interface de démonstration — outil informatif (pas de diagnostic).")

with st.expander("⚙️ Paramètres", expanded=False):
    temperature = st.slider("Température (créativité)", 0.0, 1.0, 0.3, 0.05)
    max_tokens = st.slider("Longueur max (tokens)", 100, 1200, 500, 50)
    st.markdown("**API LM Studio :** " + API_URL)

st.markdown("### ❓ Question / concept à expliquer")
question = st.text_area(
    "Exemples : hallucinations, biais, confidentialité des données patients, surconfiance dans l’IA…",
    height=90,
    placeholder="Tape ici ta question…"
)

col1, col2 = st.columns([1, 1])
with col1:
    btn = st.button("🚀 Expliquer", type="primary")
with col2:
    clear = st.button("🧹 Effacer l’historique")

if "historique" not in st.session_state:
    st.session_state.historique = []

if clear:
    st.session_state.historique = []
    st.rerun()

if btn:
    if not question.strip():
        st.warning("Merci de saisir une question.")
    else:
        with st.spinner("Génération de l’explication…"):
            try:
                reponse = appeler_llm(question, temperature=temperature, max_tokens=max_tokens)
                st.session_state.historique.insert(0, {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "question": question.strip(),
                    "reponse": reponse.strip()
                })
            except requests.exceptions.RequestException as e:
                st.error("Erreur de connexion à LM Studio. Vérifie que le serveur local est démarré (port 1234).")
                st.code(str(e))

st.markdown("---")
st.markdown("## 📌 Résultats")

if len(st.session_state.historique) == 0:
    st.info("Aucun résultat pour l’instant. Pose une question puis clique sur **Expliquer**.")
else:
    for item in st.session_state.historique:
        with st.container():
            st.markdown(f"**🕒 {item['date']}**")
            st.markdown(f"**Question :** {item['question']}")
            st.markdown("**Réponse :**")
            st.write(item["reponse"])
            st.markdown("---")

st.markdown("### ⚠️ Avertissement")
st.write(
    "Cet outil est conçu pour expliquer des concepts (IA/LLM) en contexte santé. "
    "Il ne fournit pas de diagnostic et ne remplace pas un avis médical."
)
