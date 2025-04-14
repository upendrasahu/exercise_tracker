# Coach Service

The Coach Service is an intelligent fitness advisor that works alongside the Exercise Tracker application. It leverages OpenAI's GPT models to provide personalized fitness advice, suggestions for improvement, and workout plans based on your recent exercise history.

## Features

- **AI-Powered Fitness Advice**: Get intelligent feedback and recommendations from GPT models
- **Personalized Workout Plans**: Receive personalized suggestions based on your exercise history
- **Caching**: Optional caching for advice responses when workout logs haven't changed (requires Redis)
- **RESTful API**: Simple API to integrate with other applications

## API Endpoints

### GET /api/advice

Returns personalized fitness advice based on recent workout data.

**Query Parameters:**
- `days` (optional): Number of days of exercise history to analyze (default: 30)

**Response:**
```json
{
  "advice": "Your personalized fitness advice...",
  "generated_at": 1618317826.5
}
```

### GET /health

Health check endpoint to verify the service is running.

**Response:**
```json
{
  "status": "healthy"
}
```

## Configuration

The Coach Service uses the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `EXERCISE_SERVICE_URL`: URL of the Exercise Tracker service (default: http://exercise-tracker-service:5000)
- `REDIS_URL`: URL for Redis cache (optional)
- `FLASK_APP`: Application entry point (default: app.py)
- `FLASK_ENV`: Environment setting (development/production)
- `DEBUG`: Enable debug mode (true/false)

## Deployment

The Coach Service is deployed alongside the Exercise Tracker service using Helm. The Helm chart defines both services as separate deployments that can communicate with each other within the Kubernetes cluster.

### Helm Deployment

```bash
helm upgrade --install exercise-tracker ./helm/exercise-tracker \
  --set exerciseTracker.image.repository=ghcr.io/yourusername/exercise-tracker \
  --set exerciseTracker.image.tag=latest \
  --set coachService.image.repository=ghcr.io/yourusername/exercise-tracker-coach \
  --set coachService.image.tag=latest \
  --set coachService.openaiApiKey=sk-yourapikeyhere \
  --namespace default
```

## Development

To run the Coach Service locally:

1. Navigate to the coach_service directory
2. Install dependencies: `pip install -r requirements.txt`
3. Set the required environment variables:
   ```bash
   export OPENAI_API_KEY=your-openai-api-key
   export EXERCISE_SERVICE_URL=http://localhost:5000
   ```
4. Run the application: `python app.py`

The service will be available at http://localhost:5001.