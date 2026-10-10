# PagePilot

**Python + Playwright + Page Object Model**, with GitHub Actions running Chrome on Selenium Grid 4.

Six deterministic example tests exercise a bundled task-board application. Page objects encapsulate user actions and semantic locators; tests express expected behavior using Playwright's retrying assertions. Pytest creates a fresh browser context for each test and a temporary local demo server for each run.

## Quick start
Python 3.12+:
```sh
python -m venv .venv
# Linux/macOS: source .venv/bin/activate
# Windows PowerShell: .venv/Scripts/Activate.ps1
python -m pip install -r requirements.txt
python -m playwright install chromium
python -m pytest --browser chromium --tracing retain-on-failure --screenshot only-on-failure
```
The demo starts and stops automatically. No external test account or public demo site is required. `python -m pytest -m smoke` runs the smoke subset. `--headed` opens a visible local browser. `BASE_URL` may point to another deployment of the same demo; arbitrary websites require their own page objects.

## GitHub Actions + Selenium Grid
The [workflow](.github/workflows/grid-tests.yml) runs on main pushes, pull requests, and manual dispatch. It provisions a pinned Selenium Chrome container, checks readiness, runs pytest via `SELENIUM_REMOTE_URL`, and uploads JUnit XML, failure screenshots/traces, and Grid logs. Test failures fail the job. Artifacts are retained for seven days.

Linux host networking lets both the test runner and Grid browser reach the same loopback demo server and CDP endpoint. The Grid port is ephemeral to the hosted runner; never expose an unauthenticated Grid publicly. No GitHub secrets are needed for this demo.

To reproduce on a Linux machine with Docker:
```sh
docker run -d --name pagepilot-grid --network host --shm-size=2g -e SE_NODE_GRID_URL=http://localhost:4444 selenium/standalone-chrome:4.49.0-20260909
# Wait until http://localhost:4444/status reports value.ready=true.
SELENIUM_REMOTE_URL=http://localhost:4444 python -m pytest --browser chromium
docker rm -f pagepilot-grid
```
On Windows/macOS use local Playwright for the simplest setup, or configure a Grid and demo address reachable by both machines. Container localhost and host localhost are normally different without Linux host networking.

**Grid support is experimental:** Playwright's integration uses Selenium 4's CDP endpoint and supports Chrome/Edge, not Firefox or WebKit. See [the official integration guide](https://playwright.dev/python/docs/selenium-grid). Local execution uses Playwright's own browser binaries. Update and validate the Playwright and Grid versions together.

## Structure
- `pages/task_board.py`: page object and user actions.
- `tests/test_tasks.py`: add, complete/reopen, blank-input, selective deletion, and clean-state checks.
- `conftest.py`: demo server lifecycle and page-object fixture.
- `demo/`: standalone sample app; no backend or persistence.
- `.github/workflows/grid-tests.yml`: Grid-based CI and test evidence.

## Add a new journey
Add semantic locators and reusable actions to a page object, then write assertions in a test. Avoid fixed sleeps, shared mutable pages, and test-order dependencies. Run `python -m ruff check .` before pushing. Keep real credentials in CI secrets; screenshots and traces may contain application data when adapting this starter.
