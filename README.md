# 🍳 Agno Recipe Agent

**Agno Recipe Agent** is an AI-powered interactive cooking assistant built using **Streamlit**, **Agno**, **Google's Gemini model**, and **Exa tools**. It provides smart, ingredient-aware, diet-friendly recipe suggestions through a beautiful and conversational web interface.

---

## 🔧 Features

- ✅ Personalized recipe generation based on your ingredients
- ✅ Supports dietary preferences (vegan, gluten-free, nut-free, etc.)
- ✅ Recommends quick meals, full-course menus, and healthy options
- ✅ Chat memory persisted across sessions using **SQLite**
- ✅ Elegant UI with Streamlit & sidebar prompt tools
- ✅ Option to export and reuse chat history

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Krish-jain20/Agno-Recipe-Agent.git
cd Agno-Recipe-Agent
```

### 2. Create a Virtual Environment (Optional but Recommended)

```bash
python -m venv venv

# Activate:
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Required Packages

You can install the dependencies manually:

```bash
pip install streamlit agno google-genai exa-py sqlalchemy python-dotenv
```

Or create a `requirements.txt` file (if not already present) with:

```txt
streamlit
agno
google-genai
exa-py
sqlalchemy
python-dotenv
```

Then install via:

```bash
pip install -r requirements.txt
```

### 4. Add API Keys to `.env`

Create a `.env` file in the root directory with:

```env
GOOGLE_API_KEY=your_google_api_key
EXA_API_KEY=your_exa_api_key
```

⚠️ **Ensure** `.env` is added to your `.gitignore` to avoid leaking credentials.

### 5. Run the App

```bash
streamlit run app.py
```

If your main script has a different name, replace `app.py` accordingly.

---

## 📂 Project Structure

```bash
Agno-Recipe-Agent/
├── app.py                # Main Streamlit app
├── .env                  # API keys (excluded from Git)
├── tmp/                  # SQLite memory & chat databases
│   ├── chef_agent.db
│   └── chef_memory.db
├── requirements.txt      # Optional: dependencies
└── README.md             # You're reading this!
```

---

## 🧠 How It Works

- **Agno Agent**: Handles chat intelligence and tool orchestration
- **Gemini Model**: Powers natural language understanding and recipe generation
- **Exa Tools**: Performs intelligent ingredient-based recipe searches
- **SQLite**: Stores persistent chat and memory data
- **Streamlit**: Provides fast and interactive web UI

---

## 📥 Sidebar: Quick Recipe Prompts

- ⏱️ 15-minute dinner ideas
- 🌱 Healthy breakfast suggestions
- 🍝 Vegetarian pastas
- 🍰 Gluten-free desserts
- 🥘 One-pot meals for busy nights

![Image](https://github.com/user-attachments/assets/38c6945c-a5cd-4ad2-83c3-d36f496ac968)
