"""Deploy the 3 Dexcom SW Anomaly Thought Partner ADK Agents to Vertex AI Agent Engine in Argolis.

Usage:
    # Deploy a specific phase (1, 2, or 3):
    python deploy_argolis.py --project YOUR_ARGOLIS_PROJECT_ID --staging-bucket gs://YOUR_BUCKET --phase 1

    # Deploy all 3 phases to Vertex AI Agent Engine:
    python deploy_argolis.py --project YOUR_ARGOLIS_PROJECT_ID --staging-bucket gs://YOUR_BUCKET --phase all
"""

import argparse
import os
import sys

from dotenv import load_dotenv
import vertexai
from vertexai import agent_engines
from vertexai.preview import reasoning_engines

from agents.phase1_core_triage.agent import root_agent as phase1_agent
from agents.phase2_contextual_depth.agent import root_agent as phase2_agent
from agents.phase3_thought_partner.agent import root_agent as phase3_agent


AGENT_REGISTRY = {
    "1": {
        "display_name": "Dexcom-SW-Anomaly-Thought-Partner-Phase1-Core-Triage",
        "description": "Phase 1 (Weeks 1-2): 3-Step Core Triage (Manifestation, Triggering Event, Reproducibility)",
        "agent": phase1_agent,
        "extra_packages": ["agents/phase1_core_triage"],
    },
    "2": {
        "display_name": "Dexcom-SW-Anomaly-Thought-Partner-Phase2-Contextual-Depth",
        "description": "Phase 2 (Weeks 3-4): 5-Step Contextual SW Depth (Discovery, Pre/Post System State, Trigger, Reproducibility)",
        "agent": phase2_agent,
        "extra_packages": ["agents/phase2_contextual_depth"],
    },
    "3": {
        "display_name": "Dexcom-SW-Anomaly-Thought-Partner-Phase3-Thought-Partner",
        "description": "Phase 3 (Week 5+): 4-Step Full QAC Assessment (Core Issue, Environment, Risk = Frequency x Severity, Retrospective)",
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
    print(f"[Phase {phase_key}] Successfully deployed! Resource name: {resource_name}")
    return resource_name


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(
        description="Deploy Dexcom SW Anomaly Thought Partner ADK Agents to Vertex AI Agent Engine (Argolis)."
    )
    parser.add_argument(
        "--project",
        default=os.environ.get("GOOGLE_CLOUD_PROJECT"),
        help="Argolis Google Cloud Project ID (or set GOOGLE_CLOUD_PROJECT).",
    )
    parser.add_argument(
        "--location",
        default=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
        help="Vertex AI region (default: us-central1).",
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
        help="Which phase agent to deploy: '1', '2', '3', or 'all' (default: all).",
    )
    args = parser.parse_args()

    if not args.project or not args.staging_bucket:
        print(
            "ERROR: Both --project (or GOOGLE_CLOUD_PROJECT) and --staging-bucket (or STAGING_BUCKET) are required.",
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

    for phase_key in phases_to_deploy:
        deployed_resources[f"Phase {phase_key}"] = deploy_phase(phase_key)

    print("\n=== Deployment Summary ===")
    for phase_label, res_name in deployed_resources.items():
        print(f"  {phase_label}: {res_name}")


if __name__ == "__main__":
    main()
