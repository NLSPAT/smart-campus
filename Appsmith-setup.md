# Appsmith reconstruction (not an Appsmith export)

Create a blank application named Smart Campus Room Availability Checker. Use the UI builder with Text, Datepicker, Input, Switch, Button, Text and Table widgets. No datasource or external dependency is required. The platform has not been run in this environment.

| Widget | Name | Configuration |
|---|---|---|
| Text | TitleText | Smart Campus / Room 301 |
| Datepicker | StartTime | Label: Start date and time (UTC+05:00); time precision Minute; no minimum date; default `{{ "2026-12-01T09:00:00+05:00" }}` |
| Input | Duration | Text type; label Duration (minutes); default 60; Required off |
| Switch | Blocked | Room blocked; default off |
| Button | CheckButton | Check availability; onClick `{{ RoomChecker.run() }}` |
| Text | ResultText | Binding below |
| Table | BookingsTable | Binding below; disable editable columns |

Under JS, create a JS Object named `RoomChecker` and paste the entire `RoomChecker.js` file. Bind ResultText.Text to:

```javascript
{{ appsmith.store.availabilityResult ? appsmith.store.availabilityResult.message + "\nReason: " + appsmith.store.availabilityResult.reason + "\nBookings unchanged: " + (appsmith.store.availabilityResult.bookingsUnchanged ? "YES" : "NO") : "Waiting for input" }}
```

Bind BookingsTable.Table Data to:

```javascript
{{ RoomChecker.bookings.map(b => ({"Booking ID":b.id, "Date":b.start.slice(0,10), "Start":b.start.slice(11,16), "End":b.end.slice(11,16)})) }}
```

Set ResultText text color (optional): `{{ !appsmith.store.availabilityResult ? "#64748B" : appsmith.store.availabilityResult.available ? "#16A34A" : "#DC2626" }}`.

Confirm the Datepicker displays Kazakhstan local time (UTC+05:00); if not, change the displayed timezone/convert the input before using the test cases. Use the same dates and values from `test-results.json`. Capture initial and final table, all seven decision checks, and security settings. Measure setup, implementation, debugging and testing separately. Deploy, then use App Settings > Share & Embed > Make application public if available; verify anonymous view in a private browser. Export the actual Appsmith application JSON from the workspace menu. Do not submit the local configuration as an Appsmith export.

The local preview (`low-code.html`) is a separate configuration-driven simulation; it does not establish Appsmith runtime behavior. Replace the report's pending platform items with actual observations after deployment.
