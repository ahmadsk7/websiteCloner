# ✅ MVP Build Plan – Orchids Website Cloner

Each task below is **atomic, testable, and clearly scoped** for execution.

---

## 🛠️ Setup & Scaffolding

1. **Initialize monorepo structure** with `frontend/` and `backend/` folders  
2. **Set up Next.js + TypeScript** in `frontend/`  
3. **Set up FastAPI backend** in `backend/`  
4. **Add `docker-compose.yml`** for unified local dev (`frontend + backend`)  

---

## 🌐 Frontend – Input UI

5. Build landing layout in `pages/index.tsx`  
6. Create `InputBox` component for URL  
7. Create `SubmitButton` component with onClick handler  
8. Use `useState` to track `url`, `loading`, and `cloneResult`  

---

## 🔌 Backend – Cloning API

9. Create `/clone` POST endpoint in `routes/clone.py`  
10. Connect frontend `axios.post` to `/clone`, return dummy HTML to test flow  

---

## 🔍 Scraper Logic

11. Add `utils/validate_url.py` for input checking  
12. In `scraper.py`, use `requests` + `BeautifulSoup` to pull raw DOM  
13. Extract `<style>` + linked CSS into full stylesheet  
14. Parse high-level DOM structure summary for context  
15. (Optional) Use Playwright to save page screenshot (stubbed or real)  

---

## 🤖 LLM Integration

16. Create `prompts/base_prompt.txt` with clear instructions  
17. Build `llm.py → generate_clone(design_context)`  
18. Wire full pipeline: scrape → prompt → LLM → return HTML  

---

## 🔁 Frontend – Display Output

19. Add loading spinner during API call  
20. Render result using `<iframe srcDoc={...}>`  
21. Add error message if clone fails  
22. Display toast/notification on success  
23. Add basic Tailwind/CSS styling  

---

## 🧠 Bonus Features (from TL;DR Additions)

24. **Regenerate + Refine UI Button**  
   - Adds a button to re-prompt LLM with slight tweak ("make it more modern", etc.)  
   - ✅ Improves perceived control and product UX  

25. **Section Selector**  
   - Allows user to choose which section to clone (e.g., only hero/header/footer)  
   - ✅ Gives users finer control, improves clone accuracy  
"""
