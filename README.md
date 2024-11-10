# Django Project Name

A production-ready Django application deployed on Railway.

## Tech Stack

### Backend
- Python 3.11.10
- Django
- PostgreSQL (Production)
- SQLite (Development)
- Gunicorn (Production Server)

### Deployment
- Railway
- GitHub (Version Control)

## Project Structure

### Settings Configuration
The project uses a split settings configuration:
- `base.py`: Common settings shared across environments
- `development.py`: Local development settings
- `production.py`: Production environment settings

## Environment Variables
This project uses environment variables for sensitive configuration. Ensure you have the following set up:
- `.env` file for local development
- Railway environment variables for production deployment

## Local Development
1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up your `.env` file
5. Run migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Deployment
This project is deployed using Railway CLI:
1. Install Railway CLI
2. Link to your Railway project:
   ```bash
   railway link
   ```
3. Deploy:
   ```bash
   railway up
   ```

## Development Workflow
1. Make changes locally
2. Test in development environment
3. Commit and push to GitHub for version control
4. Deploy to Railway using Railway CLI

## Contributing
[Add contributing guidelines if needed]

## License
[Add license information if applicable]
