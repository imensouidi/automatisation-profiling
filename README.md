
# Automatisation du Profiling des Clients (Flask + React)

Ce projet implémente un système intelligent d'automatisation du profiling des clients en exploitant l’apprentissage automatique et le NLP. L'objectif est de regrouper les profils similaires et d’améliorer la gestion des interactions avec les utilisateurs.

---

## 🏗️ Architecture du Projet
Le projet est structuré en **backend Flask** et **frontend React** :

📂 **Backend (Flask)**
- API RESTful en Python
- Analyse des données avec Machine Learning (Scikit-learn, Pandas)
- Base de données MongoDB

🎨 **Frontend (React)**
- Interface utilisateur en React.js
- Affichage des résultats via des tableaux et graphiques interactifs
- Communication avec l'API Flask


---

## Fonctionnalités
✅ **Profiling automatique** basé sur l'apprentissage automatique  
✅ **Analyse et segmentation des utilisateurs** avec clustering  
✅ **Stockage des données** avec MongoDB  
✅ **Interface utilisateur moderne** en React.js  
✅ **Visualisation des résultats** sous forme de tableaux et graphiques  
✅ **Documentation complète avec diagrammes UML et explications techniques**  
✅ **Vidéo de démonstration de l’application**  

---

## 📦 Installation et Lancement

### 1️⃣ Prérequis
- **Python 3** & `pip`
- **Node.js** & `npm`
- **MongoDB** (ou un autre SGBD)

### 2️⃣ Cloner le projet
```bash
git clone https://github.com/votre-utilisateur/profiling-automation.git
cd profiling-automation
```

### 3️⃣ Installation du Backend Flask
```bash
cd backend
python3 -m venv venv  # Création d'un environnement virtuel
source venv/bin/activate  # (Mac/Linux) Activation de l'environnement virtuel
venv\Scripts\activate  # (Windows)
pip install -r requirements.txt
python app.py  # Lancement du backend
```

### 4️⃣ Installation du Frontend React
```bash
cd ../frontend
npm install
npm start  # Démarrer le serveur React
```

L’application sera accessible à `http://localhost:3000`.

---


## Technologies Utilisées
### 🔧 Backend (Flask)
- Python 3
- Flask
- MongoDB
- Pandas, Scikit-learn (Machine Learning)
- JWT pour l’authentification

### 🎨 Frontend (React)
- React.js
- Axios (communication avec l’API)
- Tailwind CSS (UI)
- Recharts (graphiques)

---

## 📑 Documentation et Démonstration
📄 **Rapport Technique**  
Le rapport détaillé est disponible à la racine du projet sous le nom [`Rapport.pdf`](Rapport.pdf). Il contient :
- 📌 L'architecture du projet
- 🎯 Les objectifs et la méthodologie utilisée (CRISP-DM, Machine Learning)
- 🖥️ Les diagrammes UML (cas d'utilisation, séquences, classes)
- 📊 Les résultats et analyses du modèle d'apprentissage automatique


🎥 **Vidéo de Démonstration**  
Une démonstration vidéo de l'application est disponible à la racine du projet sous le nom [`Démonstration.mp4`](Démonstration.mp4). Vous pouvez la visionner directement en cliquant sur ce lien ou en téléchargeant le fichier.
