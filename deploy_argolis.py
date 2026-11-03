"""Deploy the 3 Dexcom SW Anomaly Thought Partner ADK Agents to Vertex AI Agent Engine
and optionally register them in a Gemini Enterprise (Agentspace) App in Argolis.

Usage:
    # 1. Deploy all 3 phases to Vertex AI Agent Engine:
    python deploy_argolis.py --project YOUR_ARGOLIS_PROJECT_ID --staging-bucket gs://YOUR_BUCKET --phase all

    # 2. Deploy to Vertex AI Agent Engine AND add to a Gemini Enterprise App:
    python deploy_argolis.py \
      --project YOUR_ARGOLIS_PROJECT_ID \
      --staging-bucket gs://YOUR_BUCKET \
      --gemini-enterprise-app-id YOUR_GEMINI_ENTERPRISE_APP_ID \
      --gemini-enterprise-location global \
      --phase all

    # 3. Register an already-deployed Reasoning Engine in a Gemini Enterprise App:
    python deploy_argolis.py \
      --project YOUR_ARGOLIS_PROJECT_ID \
      --gemini-enterprise-app-id YOUR_GEMINI_ENTERPRISE_APP_ID \
      --register-only \
      --phase 1 \
      --reasoning-engine projects/YOUR_PROJECT/locations/us-central1/reasoningEngines/1234567890
"""

import argparse
import json
import os
import sys
from typing import Any
import urllib.error
import urllib.request

from dotenv import load_dotenv
import google.auth
import google.auth.transport.requests
import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

from agents.phase1_core_triage.agent import root_agent as phase1_agent
from agents.phase2_contextual_depth.agent import root_agent as phase2_agent
from agents.phase3_thought_partner.agent import root_agent as phase3_agent


AGENT_REGISTRY: dict[str, dict[str, Any]] = {
    "1": {
        "display_name": "Dexcom-SW-Anomaly-Thought-Partner-Phase1-Core-Triage",
        "description": (
            "Phase 1 (Weeks 1-2): 3-Step Core Triage (Manifestation, Triggering Event, "
            "Reproducibility) to rapidly generate a Core Bug Report."
        ),
        "tool_description": (
            "Use this agent when an engineer wants to quickly triage and log a software "
            "anomaly using the Phase 1 (3-step Core Triage) interview covering Manifestation, "
            "Triggering Event, and Reproducibility to produce a Core Bug Report."
        ),
        "agent": phase1_agent,
        "extra_packages": ["agents/phase1_core_triage"],
    },
    "2": {
        "display_name": "Dexcom-SW-Anomaly-Thought-Partner-Phase2-Contextual-Depth",
        "description": (
            "Phase 2 (Weeks 3-4): 5-Step Contextual SW Depth (Discovery, Pre/Post System State, "
            "Triggering Event, Reproducibility) to generate a Detailed Technical Anomaly Report."
        ),
        "tool_description": (
            "Use this agent when a QA or software engineer wants to log a detailed technical "
            "software anomaly using the Phase 2 (5-step Contextual Assessment) interview covering "
            "Discovery & Manifestation, Pre-Anomaly System State, Triggering Event, Post-Anomaly "
            "System State, and Reproducibility."
        ),
        "agent": phase2_agent,
        "extra_packages": ["agents/phase2_contextual_depth"],
    },
    "3": {
        "display_name": "Dexcom-SW-Anomaly-Thought-Partner-Phase3-Thought-Partner",
        "description": (
            "Phase 3 (Week 5+): 4-Step Full QAC Assessment (Core Issue, Environment, "
            "Risk = Frequency x Severity, Retrospective) to generate a Comprehensive QAC Recommendation Report."
        ),
        "tool_description": (
            "Use this agent when an engineer, QA lead, or PM wants to conduct a full Phase 3 "
            "Software Health Hazard Assessment (SW HHA) / QAC anomaly review, including Risk "
            "Estimation (Frequency x Severity) and Root Cause / Continuous Improvement Retrospective."
        ),
        "agent": phase3_agent,
        "extra_packages": ["agents/phase3_thought_partner"],
    },
}

REQUIREMENTS = [
    "google-adk>=1.0.0",
    "google-cloud-aiplatform[adk,agent_engines]>=1.88.0",
]


def deploy_phase(phase_key: str) -> str:
    """Deploys a single phase ADK agent to Vertex AI Agent Engine."""
    spec = AGENT_REGISTRY[phase_key]
    print(f"\n[Phase {phase_key}] Packaging '{spec['display_name']}' for Vertex AI Agent Engine...")

    adk_app = reasoning_engines.AdkApp(
        agent=spec["agent"],
        enable_tracing=True,
    )

    remote_agent = agent_engines.create(
        adk_app,
        display_name=spec["display_name"],
        description=spec["description"],
        requirements=REQUIREMENTS,
        extra_packages=spec["extra_packages"],
    )

    resource_name = remote_agent.resource_name
    print(f"[Phase {phase_key}] Successfully deployed to Vertex AI Agent Engine: {resource_name}")
    return resource_name


def register_in_gemini_enterprise(
    project_id: str,
    app_id: str,
    app_location: str,
    phase_key: str,
    reasoning_engine_resource: str,
) -> dict[str, Any]:
    """Registers a deployed Vertex AI Reasoning Engine (ADK Agent) in a Gemini Enterprise App."""
    spec = AGENT_REGISTRY[phase_key]
    print(
        f"[Phase {phase_key}] Registering '{spec['display_name']}' in Gemini Enterprise App "
        f"'{app_id}' (location='{app_location}')..."
    )

    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    auth_req = google.auth.transport.requests.Request()
    credentials.refresh(auth_req)

    endpoint_host = (
        "discoveryengine.googleapis.com"
        if app_location == "global"
        else f"{app_location}-discoveryengine.googleapis.com"
    )
    url = (
        f"https://{endpoint_host}/v1alpha/projects/{project_id}/locations/{app_location}"
        f"/collections/default_collection/engines/{app_id}/assistants/default_assistant/agents"
    )

    payload = {
        "displayName": spec["display_name"],
        "description": spec["description"],
        "adk_agent_definition": {
            "tool_settings": {
                "tool_description": spec["tool_description"],
            },
            "provisioned_reasoning_engine": {
                "reasoning_engine": reasoning_engine_resource,
            },
        },
    }

    req = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {credentials.token}",
            "Content-Type": "application/json",
            "X-Goog-User-Project": project_id,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req) as resp:
            response_data = json.loads(resp.read().decode("utf-8"))
            agent_name = response_data.get("name", "UNKNOWN")
            print(f"[Phase {phase_key}] Registered in Gemini Enterprise! Agent Resource: {agent_name}")
            return response_data
    except urllib.error.HTTPError as err:
        error_body = err.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Failed to register Phase {phase_key} agent in Gemini Enterprise "
            f"(HTTP {err.code}): {error_body}"
        ) from err


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description=(
            "Deploy Dexcom SW Anomaly Thought Partner ADK Agents to Vertex AI Agent Engine "
            "and optionally register them in a Gemini Enterprise App."
        )
    )
    parser.add_argument(
        "--project",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help="Argolis Google Cloud Project ID (or set GOOGLE_CLOUD_PROJECT).",
    )
    parser.add_argument(
        "--location",
        default=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        help="Vertex AI region for Agent Engine deployment (default: us-central1).",
    )
    parser.add_argument(
        "--staging-bucket",
        default=os.environ.get("STAGING_BUCKET"),
        help="GCS bucket URI for staging Agent Engine artifacts (e.g., gs://my-argolis-staging-bucket).",
    )
    parser.add_argument(
        "--phase",
        choices=["1", "2", "3", "all"],
        default="all",
        help="Which phase agent to deploy/register: '1', '2', '3', or 'all' (default: all).",
    )
    parser.add_argument(
        "--gemini-enterprise-app-id",
        default=os.environ.get("GEMINI_ENTERPRISE_APP_ID"),
        help=(
            "Optional Gemini Enterprise (Agentspace / Discovery Engine) App/Engine ID. "
            "When provided, each deployed agent is automatically added to this Gemini Enterprise app."
        ),
    )
    parser.add_argument(
        "--gemini-enterprise-location",
        default=os.environ.get("GEMINI_ENTERPRISE_LOCATION", "global"),
        help="Gemini Enterprise App location: 'global' (default), 'us', or 'eu'.",
    )
    parser.add_argument(
        "--register-only",
        action="store_true",
        help=(
            "Skip deploying a new Reasoning Engine to Vertex AI and only register an existing "
            "Reasoning Engine resource name (--reasoning-engine) in Gemini Enterprise."
        ),
    )
    parser.add_argument(
        "--reasoning-engine",
        help=(
            "Existing Reasoning Engine resource name (projects/.../locations/.../reasoningEngines/...) "
            "when using --register-only with a single --phase (1, 2, or 3)."
        ),
    )
    args = parser.parse_args()

    if not args.project:
        print("ERROR: --project (or GOOGLE_CLOUD_PROJECT) is required.", file=sys.stderr)
        sys.exit(1)

    if args.register_only:
        if not args.gemini_enterprise_app_id:
            print(
                "ERROR: --gemini-enterprise-app-id (or GEMINI_ENTERPRISE_APP_ID) is required with --register-only.",
                file=sys.stderr,
            )
            sys.exit(1)
        if args.phase == "all" or not args.reasoning_engine:
            print(
                "ERROR: When using --register-only, specify a single --phase (1, 2, or 3) "
                "and --reasoning-engine projects/.../locations/.../reasoningEngines/...",
                file=sys.stderr,
            )
            sys.exit(1)

        registered = register_in_gemini_enterprise(
            project_id=args.project,
            app_id=args.gemini_enterprise_app_id,
            app_location=args.gemini_enterprise_location,
            phase_key=args.phase,
            reasoning_engine_resource=args.reasoning_engine,
        )
        print("\n=== Gemini Enterprise Registration Summary ===")
        print(f"  Phase {args.phase} Gemini Enterprise Agent: {registered.get('name')}")
        return

    if not args.staging_bucket:
        print(
            "ERROR: --staging-bucket (or STAGING_BUCKET) is required when deploying to Vertex AI Agent Engine.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(
        f"Initializing Vertex AI in Argolis project='{args.project}', "
        f"location='{args.location}', staging_bucket='{args.staging_bucket}'..."
    )
    vertexai.init(
        project=args.project,
        location=args.location,
        staging_bucket=args.staging_bucket,
    )

    phases_to_deploy = ["1", "2", "3"] if args.phase == "all" else [args.phase]
    deployed_resources: dict[str, str] = {}
    gemini_enterprise_agents: dict[str, str] = {}

    for phase_key in phases_to_deploy:
        resource_name = deploy_phase(phase_key)
        deployed_resources[f"Phase {phase_key}"] = resource_name

        if args.gemini_enterprise_app_id:
            reg_resp = register_in_gemini_enterprise(
                project_id=args.project,
                app_id=args.gemini_enterprise_app_id,
                app_location=args.gemini_enterprise_location,
                phase_key=phase_key,
                reasoning_engine_resource=resource_name,
            )
            gemini_enterprise_agents[f"Phase {phase_key}"] = reg_resp.get("name", "REGISTERED")

    print("\n=== Vertex AI Agent Engine Deployment Summary ===")
    for phase_label, res_name in deployed_resources.items():
        print(f"  {phase_label}: {res_name}")

    if gemini_enterprise_agents:
        print("\n=== Gemini Enterprise App Registration Summary ===")
        for phase_label, ge_agent_name in gemini_enterprise_agents.items():
            print(f"  {phase_label}: {ge_agent_name}")


if __name__ == "__main__":
    main()
