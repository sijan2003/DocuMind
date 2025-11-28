# AI Knowledge Hub

A full-stack AI-powered document management system with intelligent features powered by Google Gemini.

## 🚀 Features

### 📝 Document Management
- Create, read, update, and delete documents
- Upload PDF, DOCX, and TXT files with automatic text extraction
- Organize documents with categories
- Secure user authentication with JWT

### 🤖 AI-Powered Features
- **Summarization**: Generate concise summaries of your documents
- **Key Points Extraction**: Extract main points automatically
- **Paraphrasing**: Rewrite content in clearer language
- **Q&A**: Ask questions about your documents
- **Save AI Results**: Save AI-generated content as new documents

### 🎨 Modern UI
- Vibrant gradient design with glassmorphism effects
- Smooth animations and transitions
- Responsive layout for all devices
- Dark theme optimized for readability

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Python SQL toolkit and ORM
- **Google Gemini** - AI model for text processing
- **JWT** - Secure authentication
- **PyPDF2** - PDF text extraction
- **python-docx** - DOCX text extraction

### Frontend
- **Vanilla JavaScript** - No framework overhead
- **HTML5 & CSS3** - Modern web standards
- **Fetch API** - HTTP requests

## 📦 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Google Gemini API Key ([Get one here](https://aistudio.google.com/))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai_knowledge_hub.git
cd ai_knowledge_hub
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_api_key_here
```

5. **Set up PostgreSQL database**
Update `app/database.py` with your database credentials:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://username:password@localhost/ai_knowledge_hub"
```

6. **Run the application**
```bash
uvicorn app.main:app --reload
```

7. **Open the frontend**
Open `frontend/index.html` in your browser

## 📖 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

All API endpoints (except `/auth/register` and `/auth/login`) require JWT authentication.

1. Register: `POST /auth/register`
2. Login: `POST /auth/login` (returns access token)
3. Use token in headers: `Authorization: Bearer <token>`

## 📁 Project Structure

```
ai_knowledge_hub/
├── app/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── database.py          # Database configuration
│   ├── utils.py             # Utility functions
│   ├── routers/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── users.py         # User endpoints
│   │   ├── documents.py     # Document CRUD + upload
│   │   └── ai.py            # AI features
│   └── services/
│       ├── ai.py            # Gemini integration
│       └── file_processor.py # File text extraction
├── frontend/
│   ├── index.html           # Landing/login page
│   ├── dashboard.html       # Main application
│   ├── css/
│   │   └── style.css        # Styles
│   └── js/
│       ├── auth.js          # Authentication logic
│       ├── api.js           # API calls
│       ├── documents.js     # Document management
│       └── ai.js            # AI features
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (not in git)
```

## 🎯 Usage

1. **Register/Login** on the landing page
2. **Create documents** manually or upload files
3. **Use AI tools** to analyze your documents
4. **Save AI results** as new documents
5. **Organize** with categories

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Google Gemini for AI capabilities
- FastAPI for the excellent web framework
- The open-source community

---

**Built with ❤️ using FastAPI and Google Gemini**
