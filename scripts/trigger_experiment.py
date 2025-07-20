#!/usr/bin/env python3
"""
Trigger experiment workflow via GitHub API when research files change.

This script monitors for changes in the research/ directory and triggers
the experiment workflow to automatically synthesize, experiment, and deploy.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Optional
import requests
from datetime import datetime


class ExperimentTrigger:
    """Handles triggering experiments via GitHub API."""
    
    def __init__(self, token: str, repo: str):
        self.token = token
        self.repo = repo
        self.api_base = f"https://api.github.com/repos/{repo}"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def get_changed_research_files(self, commit_sha: Optional[str] = None) -> List[str]:
        """Get list of changed research files in the latest commit or specified commit."""
        if not commit_sha:
            # Get latest commit on main branch
            response = requests.get(
                f"{self.api_base}/commits/main",
                headers=self.headers
            )
            response.raise_for_status()
            commit_sha = response.json()["sha"]
        
        # Get commit details
        response = requests.get(
            f"{self.api_base}/commits/{commit_sha}",
            headers=self.headers
        )
        response.raise_for_status()
        commit_data = response.json()
        
        # Filter for research files
        changed_files = []
        for file in commit_data.get("files", []):
            if file["filename"].startswith("research/") and file["filename"].endswith(".md"):
                changed_files.append(file["filename"])
        
        return changed_files
    
    def extract_research_topics(self, files: List[str]) -> Dict[str, List[str]]:
        """Extract unique research topics and models from file paths."""
        topics = {}
        
        for file in files:
            parts = file.split("/")
            if len(parts) >= 3:  # research/<topic>/<model>/...
                topic = parts[1]
                model = parts[2]
                
                if topic not in topics:
                    topics[topic] = []
                if model not in topics[topic]:
                    topics[topic].append(model)
        
        return topics
    
    def trigger_workflow(self, research_topics: Dict[str, List[str]], 
                        branch: str = "main") -> Dict:
        """Trigger the experiment workflow with specified research topics."""
        workflow_id = "multi-agent-experiment.yml"
        
        payload = {
            "ref": branch,
            "inputs": {
                "research_topics": json.dumps(research_topics),
                "trigger_source": "research_change",
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        response = requests.post(
            f"{self.api_base}/actions/workflows/{workflow_id}/dispatches",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 204:
            print(f"✅ Successfully triggered experiment workflow for topics: {list(research_topics.keys())}")
            return {"status": "success", "topics": research_topics}
        else:
            print(f"❌ Failed to trigger workflow: {response.status_code}")
            print(f"Response: {response.text}")
            return {"status": "error", "code": response.status_code, "message": response.text}
    
    def monitor_workflow_status(self, run_id: int) -> str:
        """Monitor the status of a workflow run."""
        response = requests.get(
            f"{self.api_base}/actions/runs/{run_id}",
            headers=self.headers
        )
        response.raise_for_status()
        
        run_data = response.json()
        return run_data["status"]
    
    def create_tracking_issue(self, research_topics: Dict[str, List[str]]) -> int:
        """Create a GitHub issue to track the experiment."""
        title = f"🔬 Experiment: {', '.join(research_topics.keys())}"
        
        body = f"""## Automated Experiment Triggered

**Timestamp**: {datetime.utcnow().isoformat()}

### Research Topics Modified:
"""
        
        for topic, models in research_topics.items():
            body += f"\n**{topic}**:\n"
            for model in models:
                body += f"- {model}\n"
        
        body += """
### Workflow Stages:
- [ ] Research Digestion
- [ ] Synthesis Report Generation
- [ ] Implementation Plan
- [ ] Codebase Setup
- [ ] Quality Assurance
- [ ] Deployment

### Expected Outputs:
- Synthesis report in `synthesis-reports/`
- Updated implementation prompts
- Experiment results in `experiments/`
- Performance metrics
- Documentation updates

---
*This issue was automatically created by the experiment trigger system.*
"""
        
        payload = {
            "title": title,
            "body": body,
            "labels": ["experiment", "automated", "research-driven"]
        }
        
        response = requests.post(
            f"{self.api_base}/issues",
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        
        issue_data = response.json()
        print(f"📋 Created tracking issue #{issue_data['number']}: {issue_data['html_url']}")
        return issue_data["number"]


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Trigger experiment workflow based on research changes"
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("GITHUB_TOKEN"),
        help="GitHub personal access token"
    )
    parser.add_argument(
        "--repo",
        default=os.environ.get("GITHUB_REPOSITORY", "mcp/mcp"),
        help="GitHub repository (owner/name)"
    )
    parser.add_argument(
        "--commit",
        help="Specific commit SHA to check (default: latest on main)"
    )
    parser.add_argument(
        "--branch",
        default="main",
        help="Branch to trigger workflow on"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force trigger even if no research files changed"
    )
    parser.add_argument(
        "--topics",
        help="Manually specify topics as JSON (e.g., '{\"ui-frameworks\": [\"o3\", \"sonnet\"]}')"
    )
    
    args = parser.parse_args()
    
    if not args.token:
        print("❌ GitHub token required (--token or GITHUB_TOKEN env var)")
        sys.exit(1)
    
    trigger = ExperimentTrigger(args.token, args.repo)
    
    # Determine what research topics to process
    if args.topics:
        # Manual topic specification
        research_topics = json.loads(args.topics)
        print(f"📚 Using manually specified topics: {research_topics}")
    else:
        # Check for changed files
        changed_files = trigger.get_changed_research_files(args.commit)
        
        if not changed_files and not args.force:
            print("ℹ️  No research files changed. Use --force to trigger anyway.")
            sys.exit(0)
        
        if changed_files:
            print(f"📝 Found {len(changed_files)} changed research files:")
            for file in changed_files:
                print(f"  - {file}")
            
            research_topics = trigger.extract_research_topics(changed_files)
        else:
            # Force mode with no specific topics - run for all
            print("⚡ Force mode: triggering for all research topics")
            research_topics = {
                "chatgpt-agent": ["o3", "claude-4-sonnet", "claude-4-opus"],
                "codebase-generation-prompt": ["o3", "claude-4-sonnet", "claude-4-opus"]
            }
    
    # Create tracking issue
    issue_number = trigger.create_tracking_issue(research_topics)
    
    # Trigger the workflow
    result = trigger.trigger_workflow(research_topics, args.branch)
    
    if result["status"] == "success":
        print(f"\n🚀 Experiment pipeline started!")
        print(f"📊 Monitor progress at: https://github.com/{args.repo}/actions")
        print(f"📋 Tracking issue: https://github.com/{args.repo}/issues/{issue_number}")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main() 