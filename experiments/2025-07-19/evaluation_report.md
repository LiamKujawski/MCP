# Experiment Evaluation Report

Date: 2025-07-19
Generated: 2025-07-19T21:30:03.151871

## Summary

- Total Experiments: 5
- Baseline Experiments: 3
- Cross-Model Experiments: 2
- **Best Overall: o3-prompt-sonnet-model** (score: 88.98)

## Baseline Results

| Model | Tests | Pass % | Complexity | Lines | Score |
|-------|-------|--------|------------|-------|-------|
| o3 | 18 | 85.0% | 3.33 | 492 | 85.8 |
| opus | 20 | 75.0% | 1.78 | 791 | 81.4 |
| sonnet | 18 | 80.0% | 2.22 | 767 | 84.6 |

## Cross-Model Results

| Combination | Tests | Pass % | Complexity | Lines | Score |
|-------------|-------|--------|------------|-------|-------|
| o3-prompt-opus-model | 24 | 85.0% | 3.29 | 629 | 85.9 |
| o3-prompt-sonnet-model | 26 | 85.0% | 1.76 | 806 | 89.0 |

## Winner Analysis

The winning implementation is **o3-prompt-sonnet-model** with a score of 88.98

### Key Metrics:
- Test Count: 26
- Test Pass Rate: 85.0%
- Avg Complexity: 1.76
- Total Lines: 806
- Files Analyzed: 2
