# Main Application API

This document provides technical details about the Exercise Tracker's main API endpoints.

## Exercise Management Endpoints

### GET /api/exercises

Retrieves a list of exercises, optionally filtered by a date range.

**Query Parameters:**
- `days` (optional): Number of days to include in the result (default: 30)

**Response:**
```json
[
  {
    "id": 1,
    "name": "Bench Press",
    "date": "2025-04-10",
    "sets": 3,
    "reps": 10,
    "weight": 75.0,
    "notes": "Increased weight from last session"
  },
  {
    "id": 2,
    "name": "Squats",
    "date": "2025-04-10",
    "sets": 3,
    "reps": 12,
    "weight": 100.0,
    "notes": "Focused on form"
  }
]
```

## Metrics Endpoints

### GET /metrics

Returns Prometheus metrics for the application. This endpoint requires proper authentication in production environments.

**Metrics Provided:**
- `exercise_tracker_request_count`: Total API requests by endpoint and status
- `exercise_tracker_request_latency_seconds`: Request latency metrics
- `exercise_tracker_db_operation_count`: Database operation counts by type
- `exercise_tracker_active_exercises_count`: Total number of exercises in the database