# Website Cloner

A modern web application that clones websites using AI. Built with Next.js, TypeScript, and FastAPI.

## Features

- Input any public website URL
- AI-powered website cloning
- Real-time preview
- Modern, responsive UI

## Tech Stack

- **Frontend**: Next.js + TypeScript
- **Backend**: FastAPI + Python
- **AI**: Claude/GPT for HTML generation

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.8+
- Git

### Installation

1. Clone the repository:

```bash
git clone https://github.com/ahmadsk7/websiteCloner.git
cd websiteCloner
```

2. Install frontend dependencies:

```bash
cd frontend
npm install
```

3. Install backend dependencies:

```bash
cd ../backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

4. Start the development servers:

```bash
# Terminal 1 (Frontend)
cd frontend
npm run dev

# Terminal 2 (Backend)
cd backend
uvicorn app.main:app --reload
```

## License

MIT
