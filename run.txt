Quick Start

0. Create virtual environment
   python -m venv .venv

   Activate it:
   - Windows:  .venv\Scripts\activate
   - Mac/Linux: source .venv/bin/activate

1. Install dependencies
   pip install python-socketio uvicorn

2. Run the server
   python server.py

3. Access in browser
   Frontend:    http://localhost:8000/
   Backoffice:  http://localhost:8000/backoffice

Notes:
- Make sure the file is named "server.py"
- Run the command in the same folder
- Ensure these files exist in root:
  - frontend.html
  - backoffice.html