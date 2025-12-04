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

## Key Improvements Implemented

### 1. Complete Activity Management
- Fixed missing activity detail route and template
- Implemented keyword management system
- Added content management for keywords (text and photo uploads)
- Created smart bot response system based on keyword matching

### 2. Enhanced Security Features
- Implemented protection against root admin role demotion
- Added file upload validation with allowed extensions
- Improved input sanitization

### 3. Content Management System
- Full CRUD operations for keywords and content
- Support for both text and photo content
- User interface for managing content by keywords

### 4. WeChat-like Chat Interface
- Implemented WeChat-style messaging interface
- Direct access to chat from activity listings
- Left-aligned bot messages with avatar, right-aligned user messages
- Improved conversation flow and user experience
- Smart keyword matching for bot responses

### 5. User Experience Improvements
- Intuitive content management
- Better error handling and user feedback
- Mobile-optimized chat interface

## Development Milestones

### Phase 1: Basic Setup and Authentication (Weeks 1-2)
1. Set up Flask application with SQLite database
2. Create database models for Users, Admins, Activities, etc.
3. Implement user registration and login system
4. Create admin authentication system with role-based access
5. Build basic responsive HTML templates with Bootstrap
6. Implement navigation system (folded navigation for mobile)

#### Deliverables:
- Working Flask application
- Basic database schema
- User authentication system
- Responsive layout with Bootstrap

### Phase 2: Activity Management (Weeks 3-4)
1. Implement admin dashboard for activity creation
2. Create forms for adding/modifying activities
3. Implement keyword management for activities
4. Add content management (text and photo uploads)
5. Build activity listing page with chronological sorting
6. Implement activity detail pages

#### Deliverables:
- Admin panel for activity management
- CRUD operations for activities
- Content upload functionality
- Activity browsing interface

### Phase 3: Bot Interaction and Conversation (Weeks 5-6)
1. Implement bot conversation system
2. Create conversation history storage
3. Build WeChat-like user interface for chatting with bots
4. Link conversations to specific keywords and activities
5. Display conversation history for users
6. Implement smart keyword-based responses
7. Design direct access from activity listings to chat interface

#### Deliverables:
- Working bot conversation system
- Persistent conversation history
- WeChat-like chat interface with intelligent responses

### Phase 4: Admin Account Management (Weeks 7)
1. Implement root admin account creation
2. Create admin hierarchy system
3. Build admin account management interface
4. Implement password change and account deletion features
5. Add security measures to prevent role demotion

#### Deliverables:
- Multi-level admin system
- Account management features
- Enhanced security measures

### Phase 5: Content Management and Optimization (Weeks 8-9)
1. Implement full content management system
2. Add photo upload capabilities
3. Create keyword-based content organization
4. Optimize performance
5. Mobile responsiveness refinement
6. Security review and implementation

#### Deliverables:
- Complete content management system
- Optimized performance
- Production-ready code

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

## Deployment Considerations
- SQLite is suitable for development and small-scale deployment
- For production, consider PostgreSQL migration
- Use environment variables for configuration
- Implement proper logging
- Set up proper security headers
- Consider using a WSGI server like Gunicorn for production

## Security Best Practices Implemented
- Password hashing with bcrypt
- Input validation and sanitization
- Role-based access control
- Protection against privilege escalation
- File upload validation
- Session management with secure cookies
- SQL injection prevention via SQLAlchemy ORM