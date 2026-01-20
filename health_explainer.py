import requests

API_URL = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "local-model"  # LM Studio accepte ce nom

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
"""

def expliquer_concept(question):
    requete = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": PROMPT_SYSTEME},
            {"role": "user", "content": question}
        ],
        "temperature": 0.3
    }

    reponse = requests.post(API_URL, json=requete)
    return reponse.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    question = "Explique le risque de surconfiance dans l’intelligence artificielle médicale"
    resultat = expliquer_concept(question)

    print("\n--- Sortie de l’agent Health Explainer ---\n")
    print(resultat)
