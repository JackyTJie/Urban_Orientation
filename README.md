# Urban Orientation Activity Platform

A web application built with Python, Flask, and SQLite for managing urban orientation activities. The platform allows administrators to create and manage activities with keywords, information, and bot interactions, while users can sign up, interact with bots, and maintain conversation histories.

## Features

### User Features
- User registration and login system
- Mobile-responsive design suitable for phone users with desktop compatibility
- WeChat-like conversation interface with activity bots
- Persistent conversation history for each user
- Activity browsing (displayed in reverse chronological order - latest first)
- Direct access to bot conversations from activity listings

### Administrator Features
- Single root admin account with full privileges
- Multi-level admin hierarchy:
  - Root admin can create, modify, and delete other admin accounts
  - Regular admins can only delete their own account and change their password
- Activity management (create, modify, delete activities)
- Keyword management for each activity
- Content management (text and photo uploads for keywords)
- Enhanced security: Root admins cannot demote themselves

### Activity System
- Activities can have multiple keywords with associated text and/or photo content
- Bot names can be set for each activity
- Content can include text descriptions and photo uploads
- Activities displayed in chronological order (latest first)
- Smart bot responses based on keyword matching
- Direct access to WeChat-like chat interface from activity listings

## Technical Architecture

### Technology Stack
- Backend: Python Flask (with Flask-SQLAlchemy for ORM)
- Database: SQLite (file-based for simplicity)
- Frontend: HTML/CSS/JavaScript with Bootstrap for responsive design
- Templates: Jinja2 for server-side rendering

### Database Schema
- **Users**: User data (ID, username, password hash, email, created_at)
- **Admins**: Admin account data (ID, username, password hash, role, created_at)
- **Activities**: Activity metadata (ID, title, description, bot_name, created_at, updated_at)
- **Keywords**: Activity keywords (ID, activity_id, keyword, created_at)
- **Content**: Text and photo content for keywords (ID, keyword_id, content_type, content_text, content_photo_path, created_at)
- **Conversations**: User conversation history (ID, user_id, activity_id, keyword_id, message, timestamp)

### Security Considerations
- Password hashing with bcrypt
- Session management with secure cookies
- Input validation and sanitization
- Access control based on user roles
- Protected admin role management
- File upload validation

## Project Structure
```
Urban_Orientation/
├── app.py                    # Main Flask application with all routes
├── models.py                 # Database models
├── config.py                 # Configuration settings
├── templates/                # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── index.html           # Home page with introduction
│   ├── activities.html      # Activity listing page
│   ├── activity_detail.html # Activity detail page
│   ├── activity_chat.html   # Chat interface with activity bot
│   ├── user/                # User-related templates
│   │   ├── login.html
│   │   ├── register.html
│   │   └── profile.html
│   └── admin/               # Admin-related templates
│       ├── admin_login.html
│       ├── dashboard.html
│       ├── manage_keywords.html
│       ├── create_keyword.html
│       ├── edit_keyword.html
│       ├── manage_content.html
│       └── create_content.html
├── static/                  # Static assets
│   ├── css/                 # Stylesheets
│   ├── js/                  # JavaScript files
│   └── images/              # Uploaded images
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/your-username/urban-orientation.git
cd urban-orientation
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- On Linux/Mac:
```bash
source venv/bin/activate
```
- On Windows:
```bash
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Set up the database (the application will create the database automatically on first run)

6. Run the application:
```bash
python app.py
```

7. Access the application at `http://localhost:5000`

## Environment Configuration

The application uses the following configuration variables which can be set as environment variables:

- `SECRET_KEY`: Secret key for session management (defaults to 'your-secret-key-change-in-production')
- `DATABASE_URL`: Database connection string (defaults to 'sqlite:///urban_orientation.db')

## Running the Application

### Development Mode
To run in development mode with auto-reload enabled:
```bash
python app.py
```
or
```bash
FLASK_ENV=development python app.py
```

### Production Mode
For production deployment, consider using a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Usage

### User Registration and Login
1. New users can register via the `/register` endpoint
2. Existing users can log in via the `/login` endpoint
3. Users can access their profile at `/profile` to view conversation history

### Admin Access
1. Admins log in at `/login` using admin credentials
2. Root admin can manage other admin accounts at `/admin/users`
3. Admins can manage activities, keywords, and content at `/admin/dashboard`

### Activity Management
- Users can browse activities at `/activities`
- Chat interfaces are accessible directly from activity listings
- Admins can create, edit, and delete activities through the admin dashboard

## Implementation Details

### Admin Hierarchy Implementation
- Root admin: Can create, modify, and delete any admin account
- Regular admin: Can only delete their own account and change their password
- Root admins are protected from demoting themselves to prevent access loss
- Implementation uses a role field in the Admins table with access control middleware

### Mobile-First Design
- Use Bootstrap's responsive grid system
- Folded navigation implemented with hamburger menu for mobile
- Touch-friendly interface elements
- Optimized for smaller screens first, then enhanced for larger screens
- WeChat-like chat interface optimized for mobile use

### Content Management
- File upload handling with validation for allowed extensions (png, jpg, jpeg, gif)
- Secure file storage with unique naming to prevent conflicts
- Image file storage in static/images directory
- Text content sanitization

### Conversation History
- Store both user messages and bot responses in database with timestamps
- Associate conversations with user, activity and keyword
- Implement smart keyword matching for relevant bot responses
- Conversation history display with clear distinction between user and bot messages

### WeChat-like Interface Implementation
- Left-aligned messages for bot with avatar display
- Right-aligned messages for user
- Direct access to chat from activity listings
- Optimized for mobile use with proper scrolling
- Welcome message for new conversations

### Security Enhancements
- Prevent root admins from demoting themselves
- Validate file types for uploads
- Implement proper session management
- Password confirmation for sensitive operations

## Security Best Practices Implemented
- Password hashing with bcrypt
- Input validation and sanitization
- Role-based access control
- Protection against privilege escalation
- File upload validation
- Session management with secure cookies
- SQL injection prevention via SQLAlchemy ORM

## Deployment Considerations
- SQLite is suitable for development and small-scale deployment
- For production, consider PostgreSQL migration
- Use environment variables for configuration
- Implement proper logging
- Set up proper security headers
- Consider using a WSGI server like Gunicorn for production