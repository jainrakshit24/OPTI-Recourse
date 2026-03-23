# OPTI-Recourse: Comprehensive System Upgrade & Technical Documentation

## 1. Executive Summary
The **OPTI-Recourse** platform has evolved from a standalone machine learning script into a production-grade, containerized microservices ecosystem. This document serves as the categorical record of all improvements, architectural shifts, and newly integrated features. By leveraging **Docker**, **Django**, and **Streamlit**, the platform now provides high-availability credit risk assessments with deep AI interpretability (SHAP), automated PDF reporting, and high-performance analytics.

---

## 2. Platform Comparison: Evolution Overview

| Feature | Legacy System (Script-based) | Enhanced Platform (Enterprise) |
| :--- | :--- | :--- |
| **Architecture** | Component-heavy monolithic script | Decoupled Microservices (Docker) |
| **Deployment** | Manual Python environment setup | Single-command deployment (`docker-compose up`) |
| **Backend** | No persistence / In-memory | Robust **Django REST API** with SQLite/Postgres |
| **Explainability** | Black-box predictions | **SHAP Waterfall charts** for every assessment |
| **Reporting** | Console output / Text logs | **Professional PDF Reports** (fpdf2) |
| **Analytics** | Minimal / Static | **Dynamic Portfolio Dashboard** (Plotly) |
| **Scalability** | Single user only | Multi-user / API-first architecture |

---

## 3. Directory Structure Evolution

The project has been reorganized to support separate concern areas (Backend vs. Frontend), ensuring that the code is maintainable and scalable.

### 📁 New Project Topology
```text
OPTI-Recourse/
├── backend/                # Django REST API (Backend Service)
│   ├── credit_risk/        # Core business logic & model endpoints
│   ├── opti_backend/       # System configuration & security
│   └── manage.py           # Django administrative entrypoint
├── components/             # Reusable Frontend Components
│   ├── explanations.py     # SHAP visualization logic
│   └── pdf_generator.py    # Automated PDF generation engine
├── model/                  # AI Assets
│   └── model_data.pkl      # Serialized XGBoost & Scaler
├── Dockerfile.django       # Backend Image Configuration
├── Dockerfile.streamlit    # Frontend Image Configuration
├── docker-compose.yml      # Service Orchestration Logic
├── main.py                 # Streamlit UI (Frontend Entrypoint)
├── utils.py                # Shared AI Utility Module
└── requirements.txt        # Unified Dependency Management
```

---

## 9. Deployment to Render (Step-by-Step)

Render does not support `docker-compose.yml` directly, but we use a **Render Blueprint (`render.yaml`)** which handles multi-service orchestration similarly.

### 🛠️ Prerequisites
1.  **Git Repo**: Ensure your code is pushed to a GitHub or GitLab repository.
2.  **Render Account**: Create a free account at [render.com](https://render.com).

### 🚀 Deployment Steps
1.  **Connecting your Repo**:
    -   Log in to Render and go to the **Blueprints** section.
    -   Click **New Blueprint Instance**.
    -   Connect your GitHub repository.
2.  **Configuration**:
    -   Render will automatically detect the `render.yaml` file.
    -   Review the services (Backend & Frontend) and click **Apply**.
3.  **Environment Sync**:
    -   The backend will be available at an internal host `opti-backend:8000`.
    -   The frontend is pre-configured to talk to this host via the `API_BASE_URL` environment variable.
4.  **Verification**:
    -   Wait for both services to show a "Live" status.
    -   Open the URL provided for the `opti-frontend` service to access your application.

> [!TIP]
> Since we use the **Free Plan** in `render.yaml`, the services may spin down after inactivity. The first request after a spin-down might take a minute to load.

---

## 4. Architectural Deep-Dive

### 🏗️ Docker Orchestration Layer
The platform utilizes **Docker Compose** to manage two distinct services that communicate over an internal virtual network.
- **Service Isolation**: Each service runs in its own lightweight Debian-slim environment, ensuring no dependency conflicts.
- **Hot-Reloading**: Volume mapping tracks changes in the local directory, allowing developers to see code changes in real-time without rebuilding containers.
- **Health Checks**: The Streamlit container monitors its own health via `curl`, ensuring high availability.

### 🔗 API Technical Specification
The backend provides a standardized interface for all credit risk operations.

| Endpoint | Method | Description | Payload Example |
| :--- | :--- | :--- | :--- |
| `/api/predict/` | **POST** | Individual risk assessment | `{"age": 30, "income": 500000, ...}` |
| `/api/bulk-predict/`| **POST** | Batch assessment processing | `[{"age": 35, ...}, {"age": 42, ...}]` |
| `/api/history/` | **GET** | Retrieve assessment logs | N/A |
| `/api/analytics/` | **GET** | Dashboard aggregate data | N/A |

---

## 5. Feature Implementation Details

### 🔍 AI Interpretability (SHAP Intelligence)
Unlike standard models, OPTI-Recourse explains its decisions. 
- **Implementation**: We use the `shap` library to compute $2^{n}$ feature interaction values.
- **Visualization**: The `explanations.py` module converts these mathematical values into horizontal Plotly charts.
- **Impact Analysis**: Features that increase risk (positive SHAP) are highlighted in **Red**, while risk-mitigating factors (negative SHAP) are highlighted in **Green**.

### 📄 Professional PDF Reporting Engine
The `pdf_generator.py` module acts as a virtual document officer.
- **Formatting**: Uses HSL-based branding for a sleek, modern document feel.
- **Content**: Automatically pulls the assessment score, borrower profile, and top SHAP insights.
- **Security**: Reports are generated on-demand and streamed as binary data, ensuring no sensitive data is stored permanently on the web server.

### 📈 Enterprise Analytics Dashboard
The dashboard uses **Vectorized Data Processing** via Pandas and **Dynamic Rendering** via Plotly.
- **Portfolio Health**: Aggregates the `rating` column from the Django database to show the current credit spread.
- **Trend Detection**: Tracks assessment volume daily, allowing loan officers to monitor application surges.

---

## 6. Technical Optimizations & Security Protocols

### 🛡️ Security Implementation
- **CORS Management**: The `django-cors-headers` middleware is configured to allow traffic only from authorized frontend origins.
- **Host Validation**: `ALLOWED_HOSTS` is restricted to Docker network aliases to prevent Host Header injection attacks.
- **Model Security**: The `model_data.pkl` file is loaded using `joblib` in a controlled environment to ensure safe serialization.

### ⚡ Performance Tuning
- **SHAP Caching**: The SHAP explainer is initialized once at startup to avoid re-computation delays.
- **Multi-Streaming**: Streamlit’s `st.cache_resource` is used to maintain model state across different user sessions efficiently.

---

## 7. Roadmap & Future Expansion

### 🚀 Planned Phases
1. **Phase 3 (Authentication)**: Implementing JWT (JSON Web Tokens) to secure API access.
2. **Phase 4 (LLM Coaching)**: Integrating an LLM (like Gemini) to provide personalized financial improvement plans.
3. **Phase 5 (Database Migration)**: Transitioning from SQLite to PostgreSQL for high-concurrency production usage.

---
**Document Status**: Finalized
**Implementation Lead**: Antigravity AI
**Date**: March 2026
**Version**: 2.1.0
