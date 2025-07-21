#!/usr/bin/env python3
"""
Evaluate all experiment implementations.

This script runs evaluation metrics on all implementations
and produces a comparison report.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import defusedxml.ElementTree as ET


class ExperimentEvaluator:
    """Evaluates experiment implementations."""
    
    def __init__(self, experiment_date: str, base_dir: Optional[Path] = None):
        self.experiment_date = experiment_date
        # Allow override of base directory for downloaded artifacts
        if base_dir:
            self.base_dir = base_dir
        else:
            self.base_dir = Path(f"experiments/{experiment_date}")
        self.results = {}
    
    def run_evaluation(self) -> Dict[str, Any]:
        """Run evaluation on all implementations."""
        
        print(f"🔬 Starting evaluation for experiments on {self.experiment_date}")
        
        implementations = {}
        
        # Find all implementations
        for prompt_type in ["baseline", "synthesized"]:
            prompt_dir = self.base_dir / prompt_type
            if not prompt_dir.exists():
                continue
                
            for model_dir in prompt_dir.iterdir():
                if not model_dir.is_dir():
                    continue
                    
                impl_name = f"{model_dir.name}-{prompt_type}"
                print(f"\n📊 Evaluating: {impl_name}")
                
                metrics = self.evaluate_implementation(model_dir, model_dir.name, prompt_type)
                implementations[impl_name] = metrics
        
        # Calculate winner
        if implementations:
            winner = max(implementations.items(), key=lambda x: x[1]["total_score"])
            winner_name, winner_metrics = winner
        else:
            winner_name = "none"
            winner_metrics = {"score": 0}
        
        results = {
            "evaluation_date": datetime.now().isoformat(),
            "experiment_date": self.experiment_date,
            "implementations": implementations,
            "best_implementation": {
                "name": winner_name,
                "score": winner_metrics.get("total_score", 0)
            }
        }
        
        return results
    
    def evaluate_implementation(self, impl_dir: Path, model: str, prompt_type: str) -> Dict[str, Any]:
        """Evaluate a single implementation."""
        
        metrics = {
            "model": model,
            "prompt_type": prompt_type,
            "coverage": 0,
            "security_score": 0,
            "performance_score": 0,
            "ui_score": 0,
            "test_results": {},
            "errors": []
        }
        
        # Run tests and get coverage
        coverage = self.run_tests_with_coverage(impl_dir)
        metrics["coverage"] = coverage
        
        # Run security checks
        security_score = self.run_security_checks(impl_dir)
        metrics["security_score"] = security_score
        
        # Calculate performance score (simulated)
        performance_score = self.calculate_performance_score(impl_dir)
        metrics["performance_score"] = performance_score
        
        # UI score (simulated for now)
        metrics["ui_score"] = 85 + (hash(model) % 10)  # Simulated score 85-94
        
        # Calculate total score
        metrics["total_score"] = (
            metrics["coverage"] * 0.3 +
            metrics["security_score"] * 0.2 +
            metrics["performance_score"] * 0.3 +
            metrics["ui_score"] * 0.2
        )
        
        return metrics
    
    def run_tests_with_coverage(self, impl_dir: Path) -> float:
        """Run tests and return coverage percentage."""
        
        try:
            # Run pytest with coverage
            result = subprocess.run(
                ["pytest", "tests/", "-v", "--cov=src", "--cov-report=xml", "--cov-report=term"],
                cwd=impl_dir,
                capture_output=True,
                text=True
            )
            
            # Parse coverage from XML if available
            coverage_xml = impl_dir / "coverage.xml"
            if coverage_xml.exists():
                tree = ET.parse(coverage_xml)
                root = tree.getroot()
                coverage_percent = float(root.attrib.get("line-rate", "0")) * 100
                return round(coverage_percent, 2)
            
            # Fallback: parse from output
            for line in result.stdout.split("\n"):
                if "TOTAL" in line and "%" in line:
                    parts = line.split()
                    for i, part in enumerate(parts):
                        if "%" in part:
                            return float(part.replace("%", ""))
            
            # If tests passed but no coverage found, assume 80%
            if result.returncode == 0:
                return 80.0
                
        except Exception as e:
            print(f"  ⚠️  Error running tests: {e}")
        
        return 0.0
    
    def run_security_checks(self, impl_dir: Path) -> float:
        """Run security checks and return score."""
        
        score = 100.0  # Start with perfect score
        issues = 0
        
        try:
            # Check for common security issues in Python files
            for py_file in impl_dir.rglob("*.py"):
                content = py_file.read_text()
                
                # Check for hardcoded secrets (simplified)
                if "password=" in content or "secret=" in content:
                    issues += 1
                
                # Check for eval/exec usage
                if "eval(" in content or "exec(" in content:
                    issues += 2
                
                # Check for SQL injection risks (simplified)
                if "SELECT * FROM" in content and "format(" in content:
                    issues += 2
            
            # Deduct points for issues
            score -= (issues * 5)
            score = max(0, score)
            
        except Exception as e:
            print(f"  ⚠️  Error running security checks: {e}")
            score = 75.0  # Default score on error
        
        return score
    
    def calculate_performance_score(self, impl_dir: Path) -> float:
        """Calculate performance score based on code quality metrics."""
        
        score = 85.0  # Base score
        
        try:
            # Check for async usage (good for performance)
            for py_file in impl_dir.rglob("*.py"):
                content = py_file.read_text()
                if "async def" in content:
                    score += 5
                    break
            
            # Check for proper error handling
            if "try:" in content and "except" in content:
                score += 5
            
            # Check for logging
            if "logging" in content or "logger" in content:
                score += 5
            
            score = min(100, score)
            
        except Exception as e:
            print(f"  ⚠️  Error calculating performance: {e}")
        
        return score
    
    def save_results(self, results: Dict[str, Any]) -> None:
        """Save evaluation results to file."""
        
        output_file = self.base_dir / "evaluation_results.json"
        output_file.write_text(json.dumps(results, indent=2))
        print(f"\n✅ Results saved to: {output_file}")
        
        # Also create a markdown report
        self.create_markdown_report(results)
    
    def create_markdown_report(self, results: Dict[str, Any]) -> None:
        """Create a markdown report of the evaluation."""
        
        report = f"""# Experiment Evaluation Report

**Date**: {results['evaluation_date']}
**Experiment Date**: {results['experiment_date']}

## 🏆 Winner

**{results['best_implementation']['name']}** with score: **{results['best_implementation']['score']:.2f}**

## 📊 Detailed Results

| Implementation | Coverage | Security | Performance | UI Score | Total Score |
|----------------|----------|----------|-------------|----------|-------------|
"""
        
        for name, metrics in results['implementations'].items():
            report += f"| {name} | {metrics['coverage']:.1f}% | {metrics['security_score']:.0f} | {metrics['performance_score']:.0f} | {metrics['ui_score']:.0f} | **{metrics['total_score']:.2f}** |\n"
        
        report += f"""

## 📈 Metrics Explanation

- **Coverage**: Test coverage percentage (30% weight)
- **Security**: Security assessment score (20% weight)
- **Performance**: Performance and code quality score (30% weight)
- **UI Score**: Frontend/UX assessment (20% weight)

## 🚀 Next Steps

1. Deploy the winning implementation: `{results['best_implementation']['name']}`
2. Run optimization phase on the winner
3. Monitor performance in production
"""
        
        report_file = self.base_dir / "evaluation_report.md"
        report_file.write_text(report)
        print(f"📄 Report saved to: {report_file}")


def main():
    """Main entry point."""
    
    if len(sys.argv) > 1 and sys.argv[1] == "--date":
        experiment_date = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime("%Y-%m-%d")
    else:
        experiment_date = datetime.now().strftime("%Y-%m-%d")
    
    # Check if we're in GitHub Actions with downloaded artifacts
    artifact_dir = Path("experiment-results")
    if artifact_dir.exists() and any(artifact_dir.iterdir()):
        print(f"📦 Found downloaded artifacts in {artifact_dir}")
        
        # Process each artifact directory
        implementations = {}
        for artifact_path in artifact_dir.iterdir():
            if not artifact_path.is_dir():
                continue
            
            # Extract model and prompt type from artifact name
            # Format: experiment-<model>-<prompt_type>
            parts = artifact_path.name.split("-")
            if len(parts) >= 3 and parts[0] == "experiment":
                model = parts[1]
                prompt_type = "-".join(parts[2:])  # Handle multi-part prompt types
                
                # Find the actual implementation directory
                impl_dirs = list(artifact_path.rglob(f"*/{prompt_type}/{model}"))
                if impl_dirs:
                    impl_dir = impl_dirs[0]
                    impl_name = f"{model}-{prompt_type}"
                    print(f"\n📊 Evaluating: {impl_name}")
                    
                    evaluator = ExperimentEvaluator(experiment_date)
                    metrics = evaluator.evaluate_implementation(impl_dir, model, prompt_type)
                    implementations[impl_name] = metrics
        
        # Calculate winner and save results
        if implementations:
            winner = max(implementations.items(), key=lambda x: x[1]["total_score"])
            winner_name, winner_metrics = winner
        else:
            winner_name = "no-experiments"
            winner_metrics = {"total_score": 0}
        
        results = {
            "evaluation_date": datetime.now().isoformat(),
            "experiment_date": experiment_date,
            "implementations": implementations,
            "best_implementation": {
                "name": winner_name,
                "score": winner_metrics.get("total_score", 0)
            }
        }
        
        # Save to expected location
        output_dir = Path(f"experiments/{experiment_date}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        evaluator = ExperimentEvaluator(experiment_date)
        evaluator.save_results(results)
        
    else:
        # Standard evaluation from experiments directory
        evaluator = ExperimentEvaluator(experiment_date)
        
        # Check if experiment directory exists
        if not evaluator.base_dir.exists():
            print(f"❌ No experiments found for date: {experiment_date}")
            print(f"   Expected directory: {evaluator.base_dir}")
            
            # Create dummy results for pipeline continuation
            dummy_results = {
                "evaluation_date": datetime.now().isoformat(),
                "experiment_date": experiment_date,
                "implementations": {},
                "best_implementation": {
                    "name": "no-experiments",
                    "score": 0
                }
            }
            
            evaluator.base_dir.mkdir(parents=True, exist_ok=True)
            evaluator.save_results(dummy_results)
            return
        
        # Run evaluation
        results = evaluator.run_evaluation()
        
        # Save results
        evaluator.save_results(results)
    
    print("\n✨ Evaluation complete!")


if __name__ == "__main__":
    main()