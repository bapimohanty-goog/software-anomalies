# Dexcom SW Anomaly Thought Partner — 3-Phase ADK Agents (Argolis Deployment)

This repository implements the three progressive rollout phases (**"Crawl, Walk, Run"**) of the **Dexcom SW Anomaly Thought Partner** using the **Google Agent Development Kit (ADK)** (`google-adk`), ready for local testing via `adk web` and serverless deployment to **Vertex AI Agent Engine** in your **Argolis** GCP environment.

---

## Architecture & Agent Overview

Each phase is structured as an independent, self-contained ADK agent package under [`agents/`](./agents):

| Phase | Agent Package | ADK Agent Name | Interview Structure | Synthesized Report Output |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Core Triage** *(Weeks 1–2, "Crawl")* | [`agents/phase1_core_triage`](./agents/phase1_core_triage/agent.py) | `dexcom_anomaly_phase1_core_triage` | **3-Step Core Triage** (1 question at a time):<br>1. Manifestation<br>2. Triggering Event<br>3. Reproducibility | **Core Bug Report** (`Issue Summary`, `Manifestation`, `Trigger`, `Steps to Reproduce`) |
| **Phase 2: Contextual SW Depth** *(Weeks 3–4, "Walk")* | [`agents/phase2_contextual_depth`](./agents/phase2_contextual_depth/agent.py) | `dexcom_anomaly_phase2_contextual_depth` | **5-Step Contextual Assessment** (Senior QA Persona):<br>1. Discovery & Manifestation<br>2. Pre-Anomaly System State<br>3. Triggering Event<br>4. Post-Anomaly System State<br>5. Reproducibility | **Detailed Technical Anomaly Report** (objective technical report across all 5 headings) |
| **Phase 3: The True "Thought Partner"** *(Week 5+, "Run")* | [`agents/phase3_thought_partner`](./agents/phase3_thought_partner/agent.py) | `dexcom_anomaly_phase3_thought_partner` | **4-Step Full QAC Assessment**:<br>1. The Core Issue (Manifestation + Trigger/Steps)<br>2. The Environment (Pre & Post System State)<br>3. Risk Estimation ($\text{Risk} = \text{Frequency} \times \text{Severity}$)<br>4. Retrospective & Root Cause (Requirements vs. Verification vs. Systemic) | **Comprehensive QAC Recommendation Report** (formatted for rapid QAC confirmation) |

All three agents include a `save_anomaly_report` tool that exports the synthesized Markdown report to disk (`reports/phase{1,2,3}/` locally or `/tmp/dexcom_anomaly_reports/` in Vertex AI Agent Engine) and returns structured report metadata.

---

## 1. Installation from GitHub & Argolis Setup

1. **Clone the repository from GitHub**:
   ```bash
   # Using standard git:
   git clone https://github.com/bapimohanty-goog/software-anomalies.git
   cd software-anomalies

   # Or using GitHub CLI:
   gh repo clone bapimohanty-goog/software-anomalies
   cd software-anomalies
   ```

2. **Create a Python virtual environment and install dependencies**:
   ```bash
   python3 -m venv .venv
   .venv/bin/pip install --upgrade pip
   .venv/bin/pip install -r requirements.txt
   ```
   *(Optional) You can also install the dependencies directly from the remote GitHub repository:*
   ```bash
   .venv/bin/pip install -r https://raw.githubusercontent.com/bapimohanty-goog/software-anomalies/main/requirements.txt
   ```

3. **Authenticate with your Argolis GCP account and enable Vertex AI API**:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_ARGOLIS_PROJECT_ID
   gcloud auth application-default login
   gcloud services enable aiplatform.googleapis.com storage.googleapis.com
   ```

4. **Configure environment variables**:
   Copy [`.env.example`](./.env.example) to `.env` in the repository root and each agent directory:
   ```bash
   cp .env.example .env
   cp agents/phase1_core_triage/.env.example agents/phase1_core_triage/.env
   cp agents/phase2_contextual_depth/.env.example agents/phase2_contextual_depth/.env
   cp agents/phase3_thought_partner/.env.example agents/phase3_thought_partner/.env
   ```
   Update `.env` (and/or the agent `.env` files) with your Argolis project details:
   ```env
   GOOGLE_GENAI_USE_VERTEXAI=TRUE
   GOOGLE_CLOUD_PROJECT=your-argolis-project-id
   GOOGLE_CLOUD_LOCATION=us-central1
   STAGING_BUCKET=gs://your-argolis-staging-bucket
   ADK_MODEL=gemini-3.8-flash
   ```

---

## 2. Local Testing ("Show, Don't Tell" Live Demo)

You can interactively test and switch between all 3 agents side-by-side in the **ADK Web Dev UI**:

```bash
.venv/bin/adk web agents
```

Open `http://localhost:8000` in your browser and select any of the three agents from the top-left dropdown:
* `phase1_core_triage`
* `phase2_contextual_depth`
* `phase3_thought_partner`

Or run a single agent in the terminal:
```bash
.venv/bin/adk run agents/phase1_core_triage
```

---

## 3. Deploying to Vertex AI Agent Engine in Argolis

You can deploy the 3 agents to **Vertex AI Agent Engine** in Argolis using either the **ADK CLI** (`adk deploy agent_engine`) or the included Python deployment script ([`deploy_argolis.py`](./deploy_argolis.py)).

### Option A: Deploy via ADK CLI (`adk deploy agent_engine`)

Create a GCS staging bucket if you don't already have one:
```bash
gcloud storage buckets create gs://YOUR_ARGOLIS_PROJECT_ID-adk-staging --location=us-central1
```

Deploy each phase agent:
```bash
# Deploy Phase 1: Core Triage
.venv/bin/adk deploy agent_engine \
  --project=YOUR_ARGOLIS_PROJECT_ID \
  --region=us-central1 \
  --staging_bucket=gs://YOUR_ARGOLIS_PROJECT_ID-adk-staging \
  --display_name="Dexcom-SW-Anomaly-Phase1-Core-Triage" \
  agents/phase1_core_triage

# Deploy Phase 2: Contextual SW Depth
.venv/bin/adk deploy agent_engine \
  --project=YOUR_ARGOLIS_PROJECT_ID \
  --region=us-central1 \
  --staging_bucket=gs://YOUR_ARGOLIS_PROJECT_ID-adk-staging \
  --display_name="Dexcom-SW-Anomaly-Phase2-Contextual-Depth" \
  agents/phase2_contextual_depth

# Deploy Phase 3: The True Thought Partner
.venv/bin/adk deploy agent_engine \
  --project=YOUR_ARGOLIS_PROJECT_ID \
  --region=us-central1 \
  --staging_bucket=gs://YOUR_ARGOLIS_PROJECT_ID-adk-staging \
  --display_name="Dexcom-SW-Anomaly-Phase3-Thought-Partner" \
  agents/phase3_thought_partner
```

### Option B: Deploy via Python Script ([`deploy_argolis.py`](./deploy_argolis.py))

Deploy all 3 agents (or a single phase with `--phase 1|2|3`):
```bash
.venv/bin/python deploy_argolis.py \
  --project YOUR_ARGOLIS_PROJECT_ID \
  --location us-central1 \
  --staging-bucket gs://YOUR_ARGOLIS_PROJECT_ID-adk-staging \
  --phase all
```
