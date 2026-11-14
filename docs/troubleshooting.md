# Diagnosing a PagePilot run

1. **Import or plugin error:** activate the same virtual environment used to
   install `requirements.txt`; invoke both pip and pytest through `python -m`.
2. **Browser executable missing:** run `python -m playwright install chromium`
   after installing or updating the pinned requirements.
3. **Unexpected page:** check whether `BASE_URL` is set. Unset it to return to
   the bundled demo; an override does not start or reset another application.
4. **Assertion timeout:** retain a trace with `--tracing retain-on-failure`.
   Open the generated trace ZIP with
   `python -m playwright show-trace /path/to/trace.zip` and inspect the action,
   locator, and page state before changing a timeout.
5. **Grid-only error:** check the Grid readiness response and logs, then verify
   that the Grid browser can reach the demo address. The documented local Docker
   command relies on Linux host networking.
6. **No tests selected:** run `python -m pytest --collect-only -q` and check
   marker expressions and working directory. An empty selection is not a passing suite.

Report the failing test, command, Python/Playwright versions, local or Grid mode,
and commit SHA. Traces and screenshots from real applications can contain secrets;
review them before attaching them to an issue.
