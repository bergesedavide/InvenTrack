# 🏪 InvenTrack

> A full-stack business inventory simulator with AI integration, automated order simulation, and real-time sales analytics.

---

## 📖 About

InvenTrack is a warehouse and sales management simulator built as a school project. It simulates a real company's inventory system, handling automatic orders, discount events, client management, and data analytics — all backed by a REST API and an interactive React dashboard.

The project was designed to replicate a production-like environment, including multi-threaded order simulation, a virtual calendar with scheduled discount events, JWT authentication, and an AI assistant powered by a custom Ollama model.

---

## ✨ Features

- 🔄 **Sales Simulation** — multi-threaded engine that generates random orders day by day, with demand spikes during events like Black Friday
- 📅 **Virtual Calendar** — persistent calendar with scheduled discount events (Black Friday, Summer Sales, Birthdays, Random Discounts)
- 🤖 **AI Integration** — custom Ollama models for inventory management advice and a built-in chatbot
- 📊 **Analytics Dashboard** — sales charts, order history, and product performance via a React frontend
- 🔐 **JWT Authentication** — secure login system with role-based access control
- 🗃️ **Supabase Database** — cloud PostgreSQL backend with repositories for products, orders, clients, employees, and more
- 📝 **Automatic Logging** — system-wide event logger with file output
- 🧾 **Automatic Receipts & Invoicing** — generated on each completed order

---

## 🛠️ Tech Stack

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=flat&logo=supabase&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=flat&logo=jsonwebtokens&logoColor=white)

### Frontend
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![Redux](https://img.shields.io/badge/Redux-764ABC?style=flat&logo=redux&logoColor=white)
![Recharts](https://img.shields.io/badge/Recharts-22B5BF?style=flat&logoColor=white)

### AI
![Ollama](https://img.shields.io/badge/Ollama-000000?style=flat&logoColor=white)

---

## 📂 Project Structure

```
InvenTrack/
├── server/
│   ├── app/
│   │   ├── ai/              # Ollama AI integration & custom models
│   │   ├── database/        # Repository layer (products, orders, clients...)
│   │   ├── models/          # Pydantic data models
│   │   ├── routes/          # Flask API endpoints
│   │   ├── services/        # Business logic (simulation, analytics, auth...)
│   │   ├── utils/           # Helper utilities
│   │   └── core/            # Security, decorators, config
│   ├── wsgi.py
│   └── requirements.txt
└── client/
    └── src/
        ├── components/      # React UI components
        │   └── dashboard/   # Dashboard pages (analytics, orders, products...)
        ├── pages/
        └── App.jsx
```

---

## 🚀 Getting Started

### Backend

```bash
# Activate virtual environment (Windows)
.\.venv\Scripts\activate

# Install dependencies
pip install -r server/requirements.txt

# Set up your .env file with Supabase credentials
# then start the server:
cd server
waitress-serve --listen=127.0.0.1:5050 wsgi:app
```

### Frontend

```bash
cd client
npm install
npm run dev
```

---

## 🎯 Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/simulation/start` | Start the order simulation |
| POST | `/simulation/stop` | Stop the simulation |
| GET | `/simulation/status` | Get current simulation state |
| GET | `/analytics/...` | Sales and inventory analytics |
| POST | `/auth/login` | User authentication |
| GET | `/products` | Product catalog |
| GET | `/orders` | Order history |

---

## 🎓 About This Project

Built as a final project for the IT diploma at **ITIS Delpozzo, Cuneo** (Italy).
Developed by **Davide Bergese** — aspiring Data Engineer.

---

## 📬 Get in Touch

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/davide-bergese-5930b5375)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/bergesedavide)
