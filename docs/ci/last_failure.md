# CI Pipeline Failures - Analysis

## Date: 2025-07-21

### UI Tests Failure

**Run ID**: 16407081407  
**Job**: UI Tests  
**Step**: Run Playwright tests  
**Exit Code**: 1

**Error Details**:
```
Error: http://localhost:3000 is already used, make sure that nothing is running on the port/url or set reuseExistingServer:true in config.webServer.
```

**Root Cause**: The CI workflow is starting the Next.js server manually with `npx next start -p 3000` and then Playwright is trying to start another server on the same port through its webServer configuration.

**Fix Required**: Modify Playwright configuration to reuse the existing server in CI environment.

### Lighthouse CI Failures (Expected)

Based on the workflow configuration, Lighthouse CI is expected to fail due to:
1. Missing wait-on command before LHCI execution
2. Potential CHROME_INTERSTITIAL_ERROR requiring LHCI_SERVER_BASE_URL configuration
3. Need for --max-wait-for-load=60000 parameter

### Integration Tests Failures (Expected)

Docker compose services likely need health checks to ensure proper startup sequencing.

## Action Items

1. **UI Tests**: Update playwright.config.ts to set reuseExistingServer:true when CI=true
2. **Lighthouse**: Add wait-on step and proper configuration
3. **Docker**: Health checks already exist in docker-compose.test.yml
4. **Research**: Create research file to trigger experiment workflow

