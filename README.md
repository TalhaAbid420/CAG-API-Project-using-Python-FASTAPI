# 📘 CAG API Project — Chat With Your PDF

A FastAPI-based backend that allows you to upload PDFs, extract their text, store it temporarily, and query a Large Language Model (Google Gemini) using the extracted text as context.

This is essentially your own “Chat with PDF” backend — like a mini version of ChatPDF, but built from scratch in Python.

---

## 🚀 Features

- 📤 Upload PDF documents  
- 🧠 Extract text automatically using PyPDF  
- 🔐 Associate extracted text with a UUID  
- 📝 Update (append) PDF data  
- 🤖 Ask questions related to the PDF using Google Gemini  
- 🗑 Delete stored data  
- 📋 List all UUIDs  
- ⚡ FastAPI-powered API  
- 🧹 Temporary file cleanup after processing  

---

## 🧩 Project Structure

src/
│
├── routers/
│ └── data_handler.py # All upload, update, chat, delete APIs
│
├── utils/
│ ├── pdf_processor.py # Extract text from PDFs
│ └── llm_client.py # Connects to Google Gemini API
│
└── data_store.py # In-memory text storage (acts as DB)



---

## 💡 How the System Works

1. User uploads a PDF → `/api/v1/upload/{uuid}`
2. PDF is saved temporarily and text is extracted
3. Text is stored in `data_store` using the UUID as key
4. User asks a question → `/api/v1/query/{uuid}?query=...`
5. Stored PDF text is sent to Google Gemini as “context”
6. Gemini returns an answer based on the PDF contents

Clean, simple, and extremely effective.

---

## 🛠 Tech Stack

- **Python 3.10+**
- **FastAPI**
- **Uvicorn**
- **PyPDF**
- **Google Gemini API (genai)**
- **dotenv**

---

## 🔧 Installation

### 1. Clone the repo

git clone https://github.com/yourusername/cag-api.git
cd cag-api

### 2. Create a virtual environment
python -m venv venv  

source venv/bin/activate    # Linux / Mac

venv\Scripts\activate       # Windows



### 3. Install dependencies

pip install -r requirements.txt



### 4. Add your Gemini API Key

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here

Get your key from:

https://aistudio.google.com/apikey

---

### ▶ Running the Project

Start the API server:

`uvicorn main:app --reload --port 8001`


Then open:

Swagger UI (API Docs):  

`http://127.0.0.1:8001/docs`

---

### 📌 Available Endpoints

➤ Upload a PDF

`POST /api/v1/upload/{uuid}`

Stores extracted PDF text

Fails if UUID already exists

➤ Update PDF text

`PUT /api/v1/update/{uuid}`

Appends new PDF text to existing UUID

➤ Query your PDF

`GET /api/v1/query/{uuid}?query=Your question`

Sends your question + PDF text to Gemini

➤ Delete a UUID

`DELETE /api/v1/data/{uuid}`

➤ List all UUIDs

`GET /api/v1/list_uuids`

---

## 🙌 Credits

Built with ❤️ using Python & FastAPI

by *Talha Abid*