# NeuroUX — Cognitive Load & Human Attention Intelligence Engine

NeuroUX is a high-fidelity visual intelligence platform that analyzes UI screenshots to predict human visual attention, cognitive load, and UX metrics. Built for designers and researchers, it uses OpenCV-based saliency mapping and custom heuristics to provide actionable, science-backed design recommendations.

![NeuroUX Dashboard](https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=2070&ixlib=rb-4.0.3)

## 🚀 Features

- **Saliency Mapping:** Visualize exactly where a user's eyes will land in the first 500ms using Spectral Residual algorithms.
- **5 Custom UX Metrics:**
  - **Cognitive Friction Index (CFI):** Measures effort required to parse information.
  - **Visual Competition Score (VCS):** Detects conflict between different focal points.
  - **Interaction Fatigue Score (IFS):** Predicts interaction burnout probability.
  - **Decision Delay Probability (DDP):** Identifies regions causing "choice paralysis."
  - **UX Intelligence Score:** A weighted effectiveness rating for your interface.
- **AI Recommendation Engine:** Get immediate, heuristic-based design suggestions (e.g., "High visual complexity detected, increase whitespace").
- **Stateless PDF Reports:** Generate and download branded reports for stakeholders instantly.
- **Privacy-First:** No history tracking, no database, no authentication required. Your data is processed in isolated sessions and cleared upon exit.

## 🛠️ Technology Stack

- **Frontend:** React 19, Vite, Tailwind CSS v4, Framer Motion, Lucide Icons.
- **Backend:** FastAPI (Python 3.10+), Pydantic v2.
- **ML Engine:** OpenCV (Saliency API), NumPy.
- **Reporting:** fpdf2.

## 🏁 Quick Start

### Prerequisites
- [Node.js](https://nodejs.org/) (v18+)
- [Python](https://www.python.org/) (3.10+)

### One-Command Setup & Launch
```bash
# Clone the repository
git clone https://github.com/yourusername/NeuroUX.git
cd NeuroUX

# Install root dependencies
npm install

# Run the unified launch script (Starts Backend & Frontend)
npm start
```

### Manual Setup (If needed)

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/macOS
pip install -r requirements.txt
uvicorn main:app --port 8000
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

## 📂 Project Structure

```text
NeuroUX/
├── frontend/          # React + Vite (Modern SaaS UI)
├── backend/           # FastAPI (Stateless Orchestrator)
├── ml_engine/         # OpenCV-based Attention Models
├── database/          # Session-based temporary file storage
├── reports/           # Pre-generated PDF report storage
└── package.json       # Unified launch scripts
```

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---
Built with 🧠 for the next generation of UX Designers.
