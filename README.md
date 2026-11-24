# Smart Campus - Room Availability Checker

Software Engineering Practice 12 (submission email subject: Practice 13, as specified on slide 34).

## Run
Open `index.html` in a desktop browser or publish the project with GitHub Pages. The Code-based application is dependency-free. `low-code.html` is a **local configuration-driven simulation**, not a deployed Appsmith application. Both pages use fictional Room 301 bookings on 1 December 2026 (UTC+05:00). The fixed date must still be in the future for the supplied test cases. For a later demonstration, update all booking dates, default inputs, test inputs and configuration consistently; do not change the rules.

## Files
- `index.html`: complete HTML, CSS, JS implementation, no server needed.
- `low-code.html`: local interpreter-based simulation with visible widget/rule configuration.
- `low-code-config.json`: declarative configuration reference (embedded in the preview, not an Appsmith export).
- `RoomChecker.js`: Appsmith JS Object source.
- `Appsmith-setup.md`: exact Appsmith widget bindings and deployment checklist.
- `run-tests.py`: reproducible Chromium tests; Python Playwright and Chromium required. Set `CHROMIUM_PATH` if Chromium is elsewhere.
- `test-results.json`: actual test results and timings; no live Appsmith test is claimed.
- `evidence/`: real browser screenshots generated during local testing.
- `Smart-Campus-Report.pdf`: report with contract, tests, comparison, security, AI reflection and incomplete items.
- `Test-Evidence.pdf`: screenshots of all functional and additional safety checks.

## Publish on GitHub
1. Create a public repository `smart-campus` at https://github.com/new (review personal information before making anything public).
2. Add file > Upload files; upload the extracted files, not a ZIP. Commit to `main`. You can upload the `evidence` folder as well or use the evidence PDF.
3. Settings > Pages > Build and deployment > Source: Deploy from a branch > `main` > `/ (root)` > Save.
4. Open the URL shown under Settings > Pages. Typical structure: `https://USERNAME.github.io/smart-campus/`. The simulation is at `/smart-campus/low-code.html`. Verify both in a private window.
5. Add the published URL and repository URL to the email and, if desired, to this README. No repository or public URL has been created by this preparation.

## Remaining Appsmith and submission steps
Rebuild using `Appsmith-setup.md`, run the same tests in Appsmith, capture screenshots, export the actual application JSON, measure platform effort and verify anonymous public sharing. Update the report with actual platform evidence. Never present the simulation as an Appsmith export. If unable to complete the platform work, retain the clear limitation in the report (slide 33 explicitly requires labeling incomplete/simulated behavior).

Email subject: `AI-Driven Software Engineering Practice #13, Meiirim Karken, 25B030203`. Recipient: `b.azimkhanov@kbtu.kz`. Add your real class day/time, AI name/model, links and individual report/export files. Do not send ZIP, WinRAR or OneDrive links.

## Evidence scope
New baseline authorized by the student, not a recovered previous-practice project. Test results are local Chromium browser interactions via Playwright, plus mocked Appsmith JS Object tests. No third-party system was scanned. Platform permissions, export and public sharing are unverified. No paid services were used locally; external pricing not measured.
