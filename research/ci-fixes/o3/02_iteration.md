---
topic: ci-fixes
model: o3
stage: research
version: 2
---

# CI Fixes Iteration 2 – 2025-01-21

## Progress Update

Successfully resolved the following issues:

### 1. UI Dependencies Fix
- Changed from `npm ci` to `npm install` to work around package-lock.json sync issues
- Root cause: Version conflicts between Storybook and Next.js dependencies (@swc/helpers)

### 2. Experiment Pipeline Fix
- Added missing dependency installation step in evaluation job
- Fixed defusedxml import error

### 3. Current Status
- UI Tests are now passing and generating playwright reports
- Experiment jobs are running successfully
- Evaluation script needs dependencies installed

### Next Steps
- Monitor full pipeline completion
- Verify local deployment works
- Address any remaining issues in subsequent iterations