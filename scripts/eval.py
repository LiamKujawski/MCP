#!/usr/bin/env python3
"""
Automated evaluation script for agent implementation experiments.
Analyzes test results, cyclomatic complexity, and Docker image sizes.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import re


class ExperimentEvaluator:
    def __init__(self, experiment_root: str):
        self.experiment_root = Path(experiment_root)
        self.results = {}
        
    def evaluate_all(self) -> Dict:
        """Evaluate all experiments and return metrics."""
        # Evaluate baseline experiments
        baseline_results = self._evaluate_baseline()
        
        # Evaluate cross experiments
        cross_results = self._evaluate_cross()
        
        # Select best scaffold
        best_scaffold = self._select_best_scaffold(baseline_results, cross_results)
        
        return {
            'baseline': baseline_results,
            'cross': cross_results,
            'best_scaffold': best_scaffold,
            'timestamp': str(Path.cwd().name)
        }
    
    def _evaluate_baseline(self) -> Dict:
        """Evaluate baseline experiments (each model with its own prompt)."""
        results = {}
        baseline_dir = self.experiment_root / 'baseline'
        
        for model_dir in baseline_dir.iterdir():
            if model_dir.is_dir():
                model_name = model_dir.name
                results[model_name] = self._evaluate_codebase(model_dir)
                
        return results
    
    def _evaluate_cross(self) -> Dict:
        """Evaluate cross experiments."""
        results = {}
        cross_dir = self.experiment_root / 'cross'
        
        if cross_dir.exists():
            for experiment_dir in cross_dir.iterdir():
                if experiment_dir.is_dir():
                    experiment_name = experiment_dir.name
                    results[experiment_name] = self._evaluate_codebase(experiment_dir)
                    
        return results
    
    def _evaluate_codebase(self, codebase_path: Path) -> Dict:
        """Evaluate a single codebase."""
        metrics = {
            'path': str(codebase_path),
            'test_pass_rate': 0.0,
            'cyclomatic_complexity': 0,
            'docker_image_size': 0,
            'lint_status': 'unknown',
            'coverage': 0.0,
            'build_success': False
        }
        
        # Check if codebase exists
        if not codebase_path.exists():
            return metrics
            
        # Run tests
        test_results = self._run_tests(codebase_path)
        metrics.update(test_results)
        
        # Calculate cyclomatic complexity
        complexity = self._calculate_complexity(codebase_path)
        metrics['cyclomatic_complexity'] = complexity
        
        # Check Docker image size
        docker_size = self._get_docker_size(codebase_path)
        metrics['docker_image_size'] = docker_size
        
        # Run linting
        lint_status = self._run_lint(codebase_path)
        metrics['lint_status'] = lint_status
        
        return metrics
    
    def _run_tests(self, codebase_path: Path) -> Dict:
        """Run tests and return pass rate."""
        results = {
            'test_pass_rate': 0.0,
            'coverage': 0.0,
            'build_success': False
        }
        
        # Look for test script or common test commands
        test_commands = [
            'npm test',
            'pytest',
            'make test',
            'cargo test',
            'go test ./...'
        ]
        
        for cmd in test_commands:
            try:
                result = subprocess.run(
                    cmd.split(),
                    cwd=codebase_path,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    results['build_success'] = True
                    # Parse test output for pass rate
                    output = result.stdout + result.stderr
                    
                    # Try to extract test stats
                    # Pattern for pytest
                    pytest_match = re.search(r'(\d+) passed.*?(\d+) failed', output)
                    if pytest_match:
                        passed = int(pytest_match.group(1))
                        failed = int(pytest_match.group(2))
                        total = passed + failed
                        if total > 0:
                            results['test_pass_rate'] = (passed / total) * 100
                    
                    # Pattern for Jest/npm
                    jest_match = re.search(r'Tests:.*?(\d+) passed.*?(\d+) total', output)
                    if jest_match:
                        passed = int(jest_match.group(1))
                        total = int(jest_match.group(2))
                        if total > 0:
                            results['test_pass_rate'] = (passed / total) * 100
                    
                    # Coverage pattern
                    coverage_match = re.search(r'coverage:.*?(\d+(?:\.\d+)?)\s*%', output, re.IGNORECASE)
                    if coverage_match:
                        results['coverage'] = float(coverage_match.group(1))
                    
                    break
                    
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                continue
                
        return results
    
    def _calculate_complexity(self, codebase_path: Path) -> int:
        """Calculate cyclomatic complexity."""
        total_complexity = 0
        file_count = 0
        
        # Find all source files
        patterns = ['*.py', '*.js', '*.ts', '*.jsx', '*.tsx', '*.go', '*.rs']
        
        for pattern in patterns:
            for file_path in codebase_path.rglob(pattern):
                if 'node_modules' in str(file_path) or 'vendor' in str(file_path):
                    continue
                    
                complexity = self._file_complexity(file_path)
                total_complexity += complexity
                file_count += 1
        
        # Return average complexity
        return total_complexity // max(file_count, 1)
    
    def _file_complexity(self, file_path: Path) -> int:
        """Calculate cyclomatic complexity for a single file."""
        # Simplified complexity calculation
        complexity = 1  # Base complexity
        
        try:
            content = file_path.read_text()
            
            # Count decision points
            keywords = [
                r'\bif\b', r'\belse\b', r'\belif\b', r'\bfor\b', r'\bwhile\b',
                r'\bcase\b', r'\bcatch\b', r'\btry\b', r'\bexcept\b',
                r'\&\&', r'\|\|', r'\?'
            ]
            
            for keyword in keywords:
                complexity += len(re.findall(keyword, content))
                
        except Exception:
            pass
            
        return complexity
    
    def _get_docker_size(self, codebase_path: Path) -> int:
        """Get Docker image size in MB."""
        dockerfile = codebase_path / 'Dockerfile'
        
        if not dockerfile.exists():
            return 0
            
        try:
            # Build image with unique tag
            tag = f"eval-{codebase_path.name}-{os.getpid()}"
            
            result = subprocess.run(
                ['docker', 'build', '-t', tag, '.'],
                cwd=codebase_path,
                capture_output=True,
                text=True,
                timeout=600
            )
            
            if result.returncode == 0:
                # Get image size
                size_result = subprocess.run(
                    ['docker', 'images', tag, '--format', '{{.Size}}'],
                    capture_output=True,
                    text=True
                )
                
                if size_result.returncode == 0:
                    size_str = size_result.stdout.strip()
                    # Parse size (e.g., "123MB", "1.2GB")
                    if 'GB' in size_str:
                        return int(float(size_str.replace('GB', '')) * 1024)
                    elif 'MB' in size_str:
                        return int(float(size_str.replace('MB', '')))
                    
                # Cleanup
                subprocess.run(['docker', 'rmi', tag], capture_output=True)
                
        except Exception:
            pass
            
        return 0
    
    def _run_lint(self, codebase_path: Path) -> str:
        """Run linting and return status."""
        lint_commands = [
            'npm run lint',
            'eslint .',
            'flake8',
            'pylint',
            'cargo clippy'
        ]
        
        for cmd in lint_commands:
            try:
                result = subprocess.run(
                    cmd.split(),
                    cwd=codebase_path,
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    return 'passed'
                else:
                    return 'failed'
                    
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError):
                continue
                
        return 'unknown'
    
    def _select_best_scaffold(self, baseline_results: Dict, cross_results: Dict) -> Dict:
        """Select the best scaffold based on criteria."""
        all_results = {}
        
        # Combine all results
        for model, metrics in baseline_results.items():
            all_results[f"baseline_{model}"] = metrics
            
        for experiment, metrics in cross_results.items():
            all_results[f"cross_{experiment}"] = metrics
        
        # Filter by test pass rate (100% priority)
        passing_scaffolds = {
            name: metrics for name, metrics in all_results.items()
            if metrics['test_pass_rate'] == 100.0
        }
        
        # If none have 100% tests, use highest pass rate
        if not passing_scaffolds:
            max_pass_rate = max(m['test_pass_rate'] for m in all_results.values())
            passing_scaffolds = {
                name: metrics for name, metrics in all_results.items()
                if metrics['test_pass_rate'] == max_pass_rate
            }
        
        # Among passing scaffolds, select by lowest complexity
        if passing_scaffolds:
            best_name = min(
                passing_scaffolds.keys(),
                key=lambda k: (
                    passing_scaffolds[k]['cyclomatic_complexity'],
                    passing_scaffolds[k]['docker_image_size']
                )
            )
            
            return {
                'name': best_name,
                'metrics': passing_scaffolds[best_name],
                'selection_criteria': {
                    'test_pass_rate': passing_scaffolds[best_name]['test_pass_rate'],
                    'cyclomatic_complexity': passing_scaffolds[best_name]['cyclomatic_complexity'],
                    'docker_image_size': passing_scaffolds[best_name]['docker_image_size']
                }
            }
        
        return {
            'name': 'none',
            'metrics': {},
            'selection_criteria': 'No valid scaffolds found'
        }


def main():
    """Main evaluation function."""
    if len(sys.argv) < 2:
        experiment_dir = Path('experiments') / sorted(os.listdir('experiments'))[-1]
    else:
        experiment_dir = Path(sys.argv[1])
    
    evaluator = ExperimentEvaluator(experiment_dir)
    results = evaluator.evaluate_all()
    
    # Write results to JSON
    output_file = experiment_dir / 'evaluation_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(json.dumps(results, indent=2))
    

if __name__ == '__main__':
    main() 