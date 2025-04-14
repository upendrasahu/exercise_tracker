# Coach Service API

This document details the API endpoints provided by the AI Coach Service component.

## Advice Endpoints

### GET /api/advice

Retrieves personalized fitness advice based on recent exercise history.

**Query Parameters:**
- `days` (optional): Number of days of exercise history to analyze (default: 30)

**Response:**
```json
{
  "advice": "Based on your recent focus on upper body exercises, I recommend incorporating more leg workouts. Your bench press has shown good progression, but consider adding more variety to your routine. For next week, try adding 2-3 leg days with squats, lunges, and leg press. Also, make sure to allow adequate recovery time between sessions targeting the same muscle groups.",
  "generated_at": 1713127981.5
}
```

**Error Response:**
```json
{
  "error": "Error message describing what went wrong"
}
```

## Health Check Endpoint

### GET /health

Simple health check endpoint to verify the service is running.

**Response:**
```json
{
  "status": "healthy"
}
```

## Metrics Endpoints

### GET /metrics

Returns Prometheus metrics for the Coach Service.

**Metrics Provided:**
- `coach_service_request_count`: Total API requests by endpoint and status
- `coach_service_request_latency`: Request latency metrics
- `openai_request_count`: Count of requests made to OpenAI API
- `openai_request_latency`: Latency of OpenAI API requests
- `cache_hit_count`: Number of cache hits
- `cache_miss_count`: Number of cache misses