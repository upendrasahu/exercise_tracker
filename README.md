# Exercise Tracker Application

A Flask-based web application to track daily exercise routines, sets, reps, and weights, with AI-powered fitness coaching.

## Features

- Log your daily exercise routines
- Track exercise details including sets, reps, and weights
- View historical exercise data
- **AI-Powered Coaching**: Get personalized fitness advice based on your workout history
- Simple and responsive UI
- Docker support for containerization
- Kubernetes deployment with Helm charts

## Services

This application consists of two microservices:

1. **Exercise Tracker Service**: Manages exercise logs and provides a web UI
2. **Coach Service**: AI-powered service that provides personalized fitness advice using OpenAI's GPT models

## Quick Start

### Local Development

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/exercise-tracker.git
   cd exercise-tracker
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   flask run
   ```

4. Open your browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### Using Docker

1. Build the Docker images:
   ```
   # Build exercise tracker image
   docker build -t exercise-tracker .

   # Build coach service image
   docker build -t exercise-tracker-coach ./coach_service
   ```

2. Run the containers:
   ```
   # Run exercise tracker
   docker run -p 5000:5000 exercise-tracker

   # Run coach service (requires OpenAI API key)
   docker run -p 5001:5001 -e OPENAI_API_KEY=your-api-key -e EXERCISE_SERVICE_URL=http://host.docker.internal:5000 exercise-tracker-coach
   ```

3. Access the applications at:
   - Exercise Tracker: [http://localhost:5000](http://localhost:5000)
   - Coach API: [http://localhost:5001/api/advice](http://localhost:5001/api/advice)

## Deploying to Kubernetes with Helm

1. Make sure you have kubectl and helm installed and configured for your cluster.

2. Deploy the application:
   ```
   helm install exercise-tracker ./helm/exercise-tracker
   ```

3. For custom configuration, you can override values:
   ```
   helm install exercise-tracker ./helm/exercise-tracker \
     --set exerciseTracker.service.type=LoadBalancer \
     --set coachService.openaiApiKey=your-openai-api-key
   ```

## Project Structure

```
exercise_tracker/
├── app/                    # Exercise tracker app package
│   ├── __init__.py         # App initialization
│   ├── models.py           # Database models
│   └── routes.py           # Application routes
├── coach_service/          # Coach service app
│   ├── app/                # Coach service package
│   │   ├── __init__.py     # App initialization
│   │   └── routes.py       # Coach service routes
│   ├── app.py              # Coach service entry point
│   ├── Dockerfile          # Docker configuration for coach service
│   └── requirements.txt    # Python dependencies for coach service
├── docs/                   # Documentation
├── helm/                   # Helm chart for Kubernetes deployment
├── static/                 # Static assets (CSS, JS)
├── templates/              # HTML templates
├── .github/workflows/      # GitHub Actions workflows
├── app.py                  # Application entry point
├── Dockerfile              # Docker configuration for exercise tracker
└── requirements.txt        # Python dependencies for exercise tracker
```

## Documentation

For more detailed documentation, please see the [docs](./docs) directory:
- [Coach Service](./docs/COACH_SERVICE.md): Details about the AI-powered fitness coach
- [Development Guide](./docs/DEVELOPMENT.md): Information for developers
- [Installation Guide](./docs/INSTALLATION.md): Detailed installation instructions
- [User Guide](./docs/USER_GUIDE.md): Guide for end users

## CI/CD Pipeline

This project uses GitHub Actions for continuous integration and deployment:
- Automatically runs tests and linting on pull requests
- Builds and pushes Docker image to GitHub Container Registry
- Deploys to Kubernetes using Helm

## License

MIT