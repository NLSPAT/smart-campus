export default {
  bookings: [
  {
    "id": "B001",
    "start": "2026-12-01T10:00:00+05:00",
    "end": "2026-12-01T11:00:00+05:00"
  },
  {
    "id": "B002",
    "start": "2026-12-01T12:00:00+05:00",
    "end": "2026-12-01T13:30:00+05:00"
  },
  {
    "id": "B003",
    "start": "2026-12-01T15:00:00+05:00",
    "end": "2026-12-01T16:00:00+05:00"
  }
],
  check(startValue, durationValue, blocked) {
    const start = Date.parse(startValue || '');
    const raw = String(durationValue ?? '').trim();
    const duration = Number(raw);
    const result = (available, reason, message) => ({available, reason, message});
    if (!Number.isFinite(start)) return result(false, 'INVALID_DATE', 'Validation error: Select a valid start time.');
    if (start <= Date.now()) return result(false, 'PAST_START', 'Validation error: Start time must be in the future.');
    if (!/^(?:\d+(?:\.\d+)?|\.\d+)$/.test(raw) || !Number.isFinite(duration) || duration <= 0 || duration > 120) return result(false, 'INVALID_DURATION', 'Validation error: Duration must be greater than 0 and at most 120 minutes.');
    if (blocked) return result(false, 'ROOM_BLOCKED', 'Unavailable: The room is blocked.');
    const end = start + duration * 60000;
    const conflict = this.bookings.find(b => start < Date.parse(b.end) && end > Date.parse(b.start));
    if (conflict) return result(false, 'BOOKING_OVERLAP', 'Unavailable: Conflicts with booking ' + conflict.id + '.');
    return result(true, 'AVAILABLE', 'Available: No conflicting bookings found.');
  },
  async run() {
    const before = JSON.stringify(this.bookings);
    const r = this.check(StartTime.selectedDate, Duration.text, Blocked.isSwitchedOn);
    await storeValue('availabilityResult', {...r, bookingsUnchanged: before === JSON.stringify(this.bookings)}, false);
    return r;
  }
};
