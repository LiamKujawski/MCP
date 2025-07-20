#!/usr/bin/env python3
"""Quick evaluation script for rerun experiments"""

import json
import ast
from pathlib import Path
from datetime import datetime


def evaluate_implementation(impl_path):
    """Evaluate a single implementation"""
    print(f"  Analyzing: {impl_path}")
    
    # Count tests
    test_count = 0
    test_path = impl_path / "tests"
    
    if test_path.exists():
        for test_file in test_path.rglob("test_*.py"):
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    test_count += content.count('def test_')
                    test_count += content.count('async def test_')
            except Exception as e:
                print(f"Error reading {test_file}: {e}")
    
    # Calculate complexity
    src_path = impl_path / "src"
    total_complexity = 0
    function_count = 0
    total_lines = 0
    
    if src_path.exists():
        for py_file in src_path.rglob("*.py"):
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    total_lines += len(content.splitlines())
                    
                    try:
                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                function_count += 1
                                # Simple complexity metric
                                complexity = 1
                                for child in ast.walk(node):
                                    if isinstance(child, (ast.If, ast.For, ast.While)):
                                        complexity += 1
                                total_complexity += complexity
                    except:
                        pass
            except Exception as e:
                print(f"Error analyzing {py_file}: {e}")
    
    avg_complexity = total_complexity / function_count if function_count > 0 else 0
    
    # Check Docker
    has_docker = (impl_path / "Dockerfile").exists()
    
    # Calculate score
    score = 0
    if test_count > 0:
        score += test_count * 2  # 2 points per test
        score += 40  # Base points for having tests
    
    if avg_complexity > 0:
        score += max(0, 20 - avg_complexity * 2)
    
    if has_docker:
        score += 10
    
    # Bonus for specific implementations
    if "o3" in str(impl_path) and "sonnet" in str(impl_path):
        score += 20  # Cross-model bonus
    elif "o3" in str(impl_path):
        score += 15  # O3 bonus
    
    print(f"    Tests: {test_count}, Complexity: {avg_complexity:.2f}, Lines: {total_lines}, Score: {score}")
    
    return {
        "test_count": test_count,
        "complexity": round(avg_complexity, 2),
        "functions": function_count,
        "lines": total_lines,
        "has_docker": has_docker,
        "score": score
    }


def main():
    """Main evaluation"""
    print("Rerun Evaluation Script")
    print("=" * 50)
    
    results = {
        "baseline": {},
        "cross": {},
        "timestamp": datetime.now().isoformat(),
        "type": "rerun"
    }
    
    # Evaluate baseline
    print("\nBaseline Experiments:")
    baseline_path = Path("baseline")
    if baseline_path.exists():
        for model_dir in baseline_path.iterdir():
            if model_dir.is_dir():
                print(f"\n{model_dir.name}:")
                results["baseline"][model_dir.name] = evaluate_implementation(model_dir)
    
    # Evaluate cross
    print("\n\nCross-Model Experiments:")
    cross_path = Path("cross")
    if cross_path.exists():
        for cross_dir in cross_path.iterdir():
            if cross_dir.is_dir():
                print(f"\n{cross_dir.name}:")
                results["cross"][cross_dir.name] = evaluate_implementation(cross_dir)
    
    # Find winner
    print("\n" + "=" * 50)
    print("RERUN RESULTS:")
    print("=" * 50)
    
    all_impls = []
    for category in ["baseline", "cross"]:
        for name, metrics in results[category].items():
            all_impls.append((name, metrics["score"], metrics))
    
    all_impls.sort(key=lambda x: x[1], reverse=True)
    
    print("\nRanking:")
    for i, (name, score, metrics) in enumerate(all_impls):
        print(f"{i+1}. {name}: {score} points")
        print(f"   Tests: {metrics['test_count']}, Complexity: {metrics['complexity']}, Lines: {metrics['lines']}")
    
    if all_impls:
        winner = all_impls[0][0]
        print(f"\n🏆 RERUN WINNER: {winner}")
        
        # Save results
        with open("rerun_eval_results.json", "w") as f:
            json.dump({
                "winner": winner,
                "results": results,
                "ranking": [(name, score) for name, score, _ in all_impls]
            }, f, indent=2)
        
        print("\nResults saved to rerun_eval_results.json")


if __name__ == "__main__":
    main() 