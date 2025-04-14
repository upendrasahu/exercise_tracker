# Installation Guide

This document provides detailed instructions for installing and setting up the Exercise Tracker application in different environments.

## Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Docker (for containerized deployment)
- Kubernetes and Helm (for Kubernetes deployment)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/exercise-tracker.git
cd exercise-tracker
```

### 2. Create a Virtual Environment

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)

Create a `.env` file in the root directory:

```
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///exercise_data.db
```

### 5. Initialize the Database

```bash
# The database will be automatically created when you start the application
flask run
```

### 6. Run the Application

```bash
flask run
```

The application will be available at http://127.0.0.1:5000.

## Docker Deployment

### 1. Build the Docker Image

```bash
docker build -t exercise-tracker .
```

### 2. Run the Container

```bash
docker run -p 5000:5000 -v exercise_data:/app/data exercise-tracker
```

The application will be available at http://localhost:5000.

## Kubernetes Deployment with Helm

### 1. Install Helm and kubectl

Ensure you have Helm and kubectl installed and configured to connect to your Kubernetes cluster.

### 2. Deploy using Helm

```bash
# From the project root directory
helm install exercise-tracker ./helm/exercise-tracker
```

### 3. Custom Configuration

You can customize the deployment by overriding values in the Helm chart:

```bash
helm install exercise-tracker ./helm/exercise-tracker \
  --set service.type=LoadBalancer \
  --set persistence.size=2Gi
```

### 4. Access the Application

If using a LoadBalancer service type:
```bash
kubectl get service exercise-tracker
```

Note the EXTERNAL-IP and access the application at that address.

## Troubleshooting

### Common Issues

1. **Database connection errors**
   - Verify that the database file is writable by the application
   - Check that the DATABASE_URL environment variable is set correctly

2. **Container not starting**
   - Check Docker logs: `docker logs [container_id]`
   - Verify port mapping and volume mounts

3. **Kubernetes pod not running**
   - Check pod status: `kubectl get pods`
   - View logs: `kubectl logs [pod_name]`