# 🏗️ Architecture: Orchids Website Cloner

This document outlines the architecture for the Website Cloner project using **Next.js + TypeScript (frontend)** and **FastAPI + Python (backend)**. The app scrapes a public website, processes its design context, and sends it to an LLM to generate an HTML replica.

---

## 🗂️ File + Folder Structure

```bash
orchids-cloner/
│
├── frontend/                    # Next.js + TypeScript frontend
│   ├── components/              # Reusable UI components (InputBox, Preview, Loader, etc.)
│   ├── pages/                   # App routes: index.tsx, api/
│   ├── lib/                     # API handlers, utils for client-side logic
│   ├── styles/                  # Global CSS or Tailwind
│   ├── types/                   # TypeScript interfaces
│   └── state/                   # Global state with Zustand or Context
│
├── backend/                     # FastAPI backend
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── routes/
│   │   │   ├── clone.py         # API for triggering scraping + cloning
│   │   ├── services/
│   │   │   ├── scraper.py       # Website scraper logic (DOM, styles, assets)
│   │   │   ├── llm.py           # Interact with Claude/GPT for HTML generation
│   │   ├── models/              # Pydantic request/response models
│   │   └── utils/               # Helper functions (e.g., sanitize input URL)
│
├── shared/                      # Shared logic between frontend/backend (optional)
│   └── prompts/                 # Prompt templates for LLM generation
│
├── .env                         # Environment variables
├── docker-compose.yml          # Dev containers if needed
├── README.md
└── requirements.txt / package.json
⚙️ What Each Part Does
Frontend (Next.js + TypeScript)
Folder	Purpose
pages/	Main UI: input for URL, display clone preview, show status messages
components/	Modular UI components like InputBox, ClonePreview, LoadingSpinner
lib/	Axios-based API client, frontend logic
state/	Central state (e.g., loading state, clone HTML)
types/	Types for API responses, components

Backend (FastAPI)
Folder	Purpose
main.py	API entrypoint, mounts routes
routes/	Receives POST with URL, triggers scrape + LLM processing
scraper.py	Scrapes HTML, CSS, DOM tree, assets from input URL
llm.py	Formats prompt + sends request to Claude or GPT, returns HTML
models/	Pydantic schemas for input/output

🔁 Data Flow
User submits URL → /api/clone (frontend)

FastAPI receives the URL → clone.py

Scraper extracts:

DOM tree

Inline + external styles

High-level layout

Fonts/images (optional)

Design context is packaged → passed to llm.py

LLM returns HTML → sent back to frontend

Frontend shows live preview of clone

🧠 Where State Lives
Layer	State Managed
Frontend	Zustand or Context holds loading state, URL input, clone result
Backend	Stateless: data flows per request

If caching is desired, use Redis or in-memory caching for URL → HTML mappings.

🌐 Services & Integration
Service	Connected From	Purpose
Frontend → Backend	Axios	Send user-submitted URL
Backend → Scraper	Internal call	Get design context
Backend → LLM API	llm.py	Use Claude / GPT / Gemini for HTML generation

Optional Enhancements:

Use Browserless, Playwright, or Puppeteer for better scraping

Try Claude 3 Sonnet / GPT-4o for improved code generation

Add PostHog / Amplitude for usage analytics in production
"""

