# User Guide

This guide explains how to use the Exercise Tracker application to log and track your daily exercise routines.

## Getting Started

After installing the application as described in the [Installation Guide](INSTALLATION.md), open your web browser and navigate to the application URL:

- Local development: http://127.0.0.1:5000
- Docker deployment: http://localhost:5000
- Kubernetes: Use the external IP or domain assigned to the service

## Main Interface

The main interface displays a list of all your previously logged exercises, ordered by date (most recent first).

![Main Interface](images/main_interface.png)

### Key Elements of the Interface:

- **Navigation Bar**: Access different sections of the application
- **Exercise List**: View all logged exercises in a tabular format
- **Add Exercise Button**: Quickly add a new exercise entry

## Adding a New Exercise

To add a new exercise to your log:

1. Click the **Add Exercise** button on the main page or select "Add Exercise" from the navigation menu.
2. Fill in the exercise details:
   - **Exercise Name**: Name of the exercise (e.g., "Bench Press", "Squats", "Running")
   - **Date**: Date when the exercise was performed (defaults to today)
   - **Sets**: Number of sets performed
   - **Reps**: Number of repetitions per set
   - **Weight**: Weight used in kilograms (optional)
   - **Notes**: Any additional information about the exercise (optional)
3. Click the **Save Exercise** button to submit the form.

## Viewing Your Exercise History

The main page displays your complete exercise history, ordered by date with the most recent entries at the top.

You can:
- View all exercise details directly in the table
- Sort by clicking on column headers
- Use the browser's search function (Ctrl+F / Cmd+F) to find specific exercises

## Editing an Exercise Entry

To edit an existing exercise entry:

1. Locate the exercise in the table on the main page.
2. Click the **Edit** button in the Actions column.
3. Modify any details in the form that appears.
4. Click **Update Exercise** to save your changes.

## Deleting an Exercise Entry

To delete an exercise from your log:

1. Find the exercise in the table on the main page.
2. Click the **Delete** button in the Actions column.
3. Confirm the deletion when prompted.

Note: Deletion is permanent and cannot be undone.

## Tips for Effective Tracking

- Be consistent with exercise names to make tracking progress easier
- Use the notes field to record how the exercise felt, any pain points, or goals for next time
- Track your progress over time by reviewing historical data for specific exercises

## Data Security and Privacy

All your exercise data is stored locally in the database. The application does not share your data with any external services.

## Troubleshooting

If you encounter any issues while using the application:

- Make sure you're using a supported web browser (Chrome, Firefox, Safari, Edge)
- Clear your browser cache if you see outdated information
- Refer to the [Installation Guide](INSTALLATION.md) for application-specific troubleshooting

For additional help, please open an issue on the project's GitHub repository.