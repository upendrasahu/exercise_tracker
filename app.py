from app import create_app
from datetime import datetime

app = create_app()

# Add template context processor for current year
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.now().year}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)