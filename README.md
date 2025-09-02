# 📚 Book Management Web App (FastAPI + Streamlit)

An interactive **Book Management Application** that integrates **FastAPI** for backend API services and **Streamlit** for frontend visualization.

---

## ✨ Features
- 🔎 View all books with details (title, author, description, rating).
- ➕ Add new books with validation (ratings 1–5, minimum text length checks).
- ✏️ Update existing books.
- ❌ Delete books by ID.
- ⚡ Fully documented API via **FastAPI Swagger UI** 
- 🎨 Modern UI built with **Streamlit** — no HTML/CSS required.

---

## 🛠️ Tech Stack
- **FastAPI** → High-performance REST API
- **Pydantic** → Data validation & schema
- **Starlette** → Status codes & exception handling
- **Streamlit** → Interactive frontend for CRUD operations
- **Python 3.9+**

---

pip install -r requirements.txt
3️⃣ Run the Application
bash
streamlit run app.py
This will start both the Streamlit UI and the FastAPI backend, all in a single app.
