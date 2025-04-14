# Development Guide

This document provides guidelines and information for developers who want to contribute to the Exercise Tracker application.

## Development Environment Setup

1. Follow the installation steps in the [Installation Guide](INSTALLATION.md) to set up your local development environment.

2. Additional development dependencies:
   ```bash
   pip install pytest pytest-flask flake8 black
   ```

## Project Structure

The application follows a standard Flask application structure:

```
exercise_tracker/
├── app/                  # Application package
│   ├── __init__.py       # App initialization with Flask factory pattern
│   ├── models.py         # SQLAlchemy database models
│   └── routes.py         # Flask routes and view functions
├── static/               # Static assets
│   ├── css/              # CSS stylesheets
│   └── js/               # JavaScript files
├── templates/            # Jinja2 HTML templates
├── tests/                # Test directory
├── app.py                # Application entry point
└── requirements.txt      # Dependencies
```

## Code Style Guidelines

- Follow PEP 8 style guidelines for Python code
- Use Black for automatic code formatting
- Use meaningful variable and function names
- Write docstrings for all functions, classes, and modules
- Keep functions small and focused on a single responsibility

## Database Schema

The application uses SQLAlchemy with a simple schema:

```python
class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float)  # Weight in kg/lbs
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## Testing

### Running Tests

```bash
pytest
```

### Writing Tests

- Place test files in the `tests/` directory
- Use descriptive test names that explain what's being tested
- Test both success and failure conditions
- Mock external dependencies when necessary

Example test structure:

```python
def test_add_exercise():
    # Test adding a new exercise
    pass

def test_edit_exercise():
    # Test editing an existing exercise
    pass
```

## Docker Development

For testing Docker-related changes:

```bash
# Build the image
docker build -t exercise-tracker-dev .

# Run with development settings
docker run -p 5000:5000 -e FLASK_ENV=development -v $(pwd):/app exercise-tracker-dev
```

## Kubernetes Development

For local Kubernetes development, consider using:
- Minikube
- Kind (Kubernetes in Docker)

Install the Helm chart locally:
```bash
helm install exercise-tracker-dev ./helm/exercise-tracker --set image.tag=latest
```

## CI/CD Pipeline

The GitHub Actions workflow in `.github/workflows/build-and-deploy.yml` handles:

1. Running tests and linting on pull requests
2. Building the Docker image
3. Pushing the image to GitHub Container Registry
4. Deploying to Kubernetes (on main branch merges)

## Making Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests to ensure they pass
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to your branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Performance Considerations

- Keep database queries efficient
- Use pagination for large data sets
- Consider caching for frequently accessed data

## Security Best Practices

- Validate all user inputs
- Use parameterized queries (handled by SQLAlchemy)
- Keep dependencies updated
- Don't expose sensitive information in logs or error messages