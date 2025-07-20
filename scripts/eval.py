#!/usr/bin/env python3
"""
Evaluation script for agent implementation experiments.
Compares and ranks implementations based on multiple criteria.
"""

import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple
import argparse
import numpy as np

class AgentEvaluator:
    """Evaluates agent-generated implementations."""
    
    def __init__(self, experiment_dir: str):
        self.experiment_dir = Path(experiment_dir)
        self.metrics = {}
        
    def evaluate_implementation(self, impl_path: Path) -> Dict:
        """Evaluate a single implementation."""
        metrics = {
            'test_pass_rate': self._run_tests(impl_path),
            'cyclomatic_complexity': self._measure_complexity(impl_path),
            'docker_image_size': self._measure_docker_size(impl_path),
            'lint_score': self._run_linter(impl_path),
            'code_coverage': self._measure_coverage(impl_path),
            'build_time': self._measure_build_time(impl_path),
            'timestamp': datetime.now().isoformat()
        }
        return metrics
    
    def _run_tests(self, path: Path) -> float:
        """Run tests and return pass rate."""
        try:
            result = subprocess.run(
                ['pytest', '-v', '--json-report', '--json-report-file=/tmp/report.json'],
                cwd=path,
                capture_output=True,
                text=True
            )
            
            if os.path.exists('/tmp/report.json'):
                with open('/tmp/report.json') as f:
                    report = json.load(f)
                    total = report['summary']['total']
                    passed = report['summary']['passed']
                    return (passed / total * 100) if total > 0 else 0
        except Exception as e:
            print(f"Test error: {e}")
        return 0.0
    
    def _measure_complexity(self, path: Path) -> float:
        """Measure cyclomatic complexity."""
        try:
            result = subprocess.run(
                ['radon', 'cc', '-a', '--json', str(path)],
                capture_output=True,
                text=True
            )
            data = json.loads(result.stdout)
            complexities = []
            for file_data in data.values():
                for func in file_data:
                    complexities.append(func['complexity'])
            return np.mean(complexities) if complexities else 0
        except Exception as e:
            print(f"Complexity error: {e}")
        return 0.0
    
    def _measure_docker_size(self, path: Path) -> int:
        """Build Docker image and measure size in MB."""
        try:
            dockerfile = path / 'Dockerfile'
            if not dockerfile.exists():
                return 0
            
            image_name = f"agent-test-{path.name}"
            subprocess.run(
                ['docker', 'build', '-t', image_name, '.'],
                cwd=path,
                capture_output=True
            )
            
            result = subprocess.run(
                ['docker', 'images', image_name, '--format', '{{.Size}}'],
                capture_output=True,
                text=True
            )
            
            size_str = result.stdout.strip()
            # Convert to MB
            if 'GB' in size_str:
                return float(size_str.replace('GB', '')) * 1024
            elif 'MB' in size_str:
                return float(size_str.replace('MB', ''))
            return 0
        except Exception as e:
            print(f"Docker error: {e}")
        return 0
    
    def _run_linter(self, path: Path) -> float:
        """Run linter and return score."""
        try:
            result = subprocess.run(
                ['pylint', '--output-format=json', str(path)],
                capture_output=True,
                text=True
            )
            data = json.loads(result.stdout)
            # Pylint score is out of 10
            return data.get('score', 0) * 10  # Convert to percentage
        except Exception:
            # Fallback to simple check
            return 80.0  # Default score
    
    def _measure_coverage(self, path: Path) -> float:
        """Measure test coverage."""
        try:
            subprocess.run(
                ['pytest', '--cov=.', '--cov-report=json'],
                cwd=path,
                capture_output=True
            )
            
            coverage_file = path / 'coverage.json'
            if coverage_file.exists():
                with open(coverage_file) as f:
                    data = json.load(f)
                    return data['totals']['percent_covered']
        except Exception:
            pass
        return 0.0
    
    def _measure_build_time(self, path: Path) -> float:
        """Measure build time in seconds."""
        try:
            start = time.time()
            if (path / 'setup.py').exists():
                subprocess.run(['python', 'setup.py', 'build'], cwd=path)
            elif (path / 'package.json').exists():
                subprocess.run(['npm', 'run', 'build'], cwd=path)
            elif (path / 'Makefile').exists():
                subprocess.run(['make', 'build'], cwd=path)
            return time.time() - start
        except Exception:
            return 0.0
    
    def evaluate_all(self, stage: str) -> Dict:
        """Evaluate all implementations in a stage."""
        stage_dir = self.experiment_dir / stage
        results = {}
        
        for model_dir in stage_dir.iterdir():
            if model_dir.is_dir():
                print(f"Evaluating {model_dir.name}...")
                results[model_dir.name] = self.evaluate_implementation(model_dir)
        
        return results
    
    def rank_implementations(self, results: Dict) -> List[Tuple[str, float]]:
        """Rank implementations based on weighted criteria."""
        weights = {
            'test_pass_rate': 0.35,
            'cyclomatic_complexity': -0.20,  # Lower is better
            'docker_image_size': -0.15,      # Lower is better
            'lint_score': 0.15,
            'code_coverage': 0.15
        }
        
        scores = {}
        for model, metrics in results.items():
            score = 0
            for metric, weight in weights.items():
                if metric in metrics:
                    # Normalize metrics
                    value = metrics[metric]
                    if metric == 'cyclomatic_complexity':
                        # Lower complexity is better, normalize inversely
                        normalized = 100 / (1 + value)
                    elif metric == 'docker_image_size':
                        # Lower size is better, normalize inversely
                        normalized = 100 / (1 + value/10)  # Scale MB
                    else:
                        normalized = value
                    
                    score += normalized * abs(weight) * (1 if weight > 0 else -1)
            
            scores[model] = score
        
        return sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    def select_winner(self, results: Dict) -> str:
        """Select winning implementation based on criteria."""
        # First check for 100% test pass rate
        perfect_tests = [m for m, metrics in results.items() 
                        if metrics.get('test_pass_rate', 0) == 100]
        
        if perfect_tests:
            # Among perfect test scores, pick lowest complexity
            winner = min(perfect_tests, 
                        key=lambda m: results[m].get('cyclomatic_complexity', float('inf')))
        else:
            # Otherwise use ranking
            rankings = self.rank_implementations(results)
            winner = rankings[0][0] if rankings else None
        
        return winner
    
    def generate_report(self, baseline_results: Dict, cross_results: Dict = None) -> Dict:
        """Generate comprehensive evaluation report."""
        report = {
            'experiment_date': datetime.now().isoformat(),
            'baseline_results': baseline_results,
            'baseline_rankings': self.rank_implementations(baseline_results),
            'baseline_winner': self.select_winner(baseline_results)
        }
        
        if cross_results:
            report['cross_results'] = cross_results
            report['cross_rankings'] = self.rank_implementations(cross_results)
            report['final_winner'] = self.select_winner({**baseline_results, **cross_results})
        
        # Add summary statistics
        report['summary'] = {
            'total_implementations': len(baseline_results) + (len(cross_results) if cross_results else 0),
            'perfect_test_scores': sum(1 for r in baseline_results.values() 
                                     if r.get('test_pass_rate', 0) == 100),
            'average_complexity': np.mean([r.get('cyclomatic_complexity', 0) 
                                         for r in baseline_results.values()]),
            'average_coverage': np.mean([r.get('code_coverage', 0) 
                                       for r in baseline_results.values()])
        }
        
        return report

def main():
    parser = argparse.ArgumentParser(description='Evaluate agent implementations')
    parser.add_argument('--experiment-dir', required=True, help='Experiment directory')
    parser.add_argument('--output', default='evaluation_report.json', help='Output report file')
    args = parser.parse_args()
    
    evaluator = AgentEvaluator(args.experiment_dir)
    
    # Stage A: Baseline evaluation
    print("=== Stage A: Baseline Evaluation ===")
    baseline_results = evaluator.evaluate_all('baseline')
    
    # Select top performer
    baseline_winner = evaluator.select_winner(baseline_results)
    print(f"\nBaseline winner: {baseline_winner}")
    
    # Stage B: Cross evaluation (if baseline completed)
    cross_results = None
    if baseline_winner:
        print("\n=== Stage B: Cross Evaluation ===")
        # In a real scenario, this would trigger cross-runs
        # For now, we'll check if cross results exist
        cross_dir = Path(args.experiment_dir) / 'cross'
        if cross_dir.exists():
            cross_results = evaluator.evaluate_all('cross')
    
    # Generate final report
    report = evaluator.generate_report(baseline_results, cross_results)
    
    # Save report
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\nEvaluation complete. Report saved to {args.output}")
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Baseline winner: {report['baseline_winner']}")
    if 'final_winner' in report:
        print(f"Final winner: {report['final_winner']}")

if __name__ == '__main__':
    main()