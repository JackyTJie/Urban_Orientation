from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urban_orientation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize database
db = SQLAlchemy(app)

# Import models after db initialization to avoid circular imports
from models import User, Admin, Activity, Keyword, Content, Conversation

# Create tables
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def index():
    """Home page with introduction to 城市定向社团"""
    return render_template('index.html')

@app.route('/activities')
def activities():
    """Display all activities in chronological order (latest first)"""
    activities_list = Activity.query.order_by(Activity.created_at.desc()).all()
    return render_template('activities.html', activities=activities_list)

@app.route('/activity/<int:activity_id>')
def activity_detail(activity_id):
    """Redirect to chat interface for the activity"""
    return redirect(url_for('activity_chat', activity_id=activity_id))


@app.route('/activity/<int:activity_id>/chat', methods=['GET', 'POST'])
def activity_chat(activity_id):
    """Chat with the activity bot"""
    if 'user_id' not in session:
        flash('Please login to chat with the bot')
        return redirect(url_for('login'))

    activity = Activity.query.get_or_404(activity_id)
    user_id = session['user_id']

    if request.method == 'POST':
        user_message = request.form['message']
        if user_message.strip():
            # Find the keyword that matches the user message
            keyword = Keyword.query.filter(
                Keyword.activity_id == activity_id,
                db.func.lower(Keyword.keyword) == db.func.lower(user_message)
            ).first()

            if not keyword:
                # Try to find partial match
                keyword = Keyword.query.filter(
                    Keyword.activity_id == activity_id,
                    db.func.lower(Keyword.keyword).contains(db.func.lower(user_message))
                ).first()

            # Use first keyword if no match found
            if not keyword:
                keyword = Keyword.query.filter_by(activity_id=activity_id).first()

            keyword_id = keyword.id if keyword else 1  # Default to 1 if no keywords exist

            # Save user message to conversation
            user_conversation = Conversation(
                user_id=user_id,
                activity_id=activity.id,
                keyword_id=keyword_id,
                message=user_message,
                timestamp=datetime.utcnow()
            )
            db.session.add(user_conversation)

            # Generate bot response based on keywords and content
            bot_response = "抱歉，我没有理解您的问题。"
            if keyword:
                # Get content associated with the matched keyword
                content_items = Content.query.filter_by(keyword_id=keyword_id).all()
                if content_items:
                    # Combine all text content for the response
                    responses = []
                    for content in content_items:
                        if content.content_type == 'text' and content.content_text:
                            responses.append(content.content_text)
                        elif content.content_type == 'photo' and content.content_photo_path:
                            responses.append(f"图片: {content.content_photo_path}")

                    bot_response = " ".join(responses) if responses else bot_response

            # Save bot response to conversation
            bot_conversation = Conversation(
                user_id=user_id,  # Same user_id since it's associated with the user's chat session
                activity_id=activity.id,
                keyword_id=keyword_id,
                message=bot_response,
                timestamp=datetime.utcnow()
            )
            db.session.add(bot_conversation)

            db.session.commit()

            return redirect(url_for('activity_chat', activity_id=activity_id))

    # Get conversation history
    conversations = Conversation.query.filter_by(
        user_id=user_id,
        activity_id=activity_id
    ).order_by(Conversation.timestamp).all()

    return render_template('activity_chat.html', activity=activity, conversations=conversations)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['user_type'] = 'user'
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    
    return render_template('user/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('user/register.html')
        
        # Create new user
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            password_hash=hashed_password,
            email=email,
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful')
        return redirect(url_for('login'))
    
    return render_template('user/register.html')

@app.route('/profile')
def user_profile():
    """User profile with conversation history"""
    if 'user_id' not in session:
        flash('Please login to view your profile')
        return redirect(url_for('login'))

    user = User.query.get_or_404(session['user_id'])
    # Get all conversations for this user
    conversations = db.session.query(Conversation, Activity) \
                    .join(Activity) \
                    .filter(Conversation.user_id == user.id) \
                    .order_by(Conversation.timestamp.desc()) \
                    .all()

    # Group conversations by activity
    conversations_by_activity = {}
    for conv, activity in conversations:
        if activity.id not in conversations_by_activity:
            conversations_by_activity[activity.id] = {
                'activity': activity,
                'messages': []
            }
        conversations_by_activity[activity.id]['messages'].append(conv)

    return render_template('user/profile.html',
                         user=user,
                         conversations_by_activity=conversations_by_activity)


@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('user_id', None)
    session.pop('user_type', None)
    return redirect(url_for('index'))

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            session['admin_role'] = admin.role
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin username or password')
    
    return render_template('admin/admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Logout admin"""
    session.pop('admin_id', None)
    session.pop('admin_role', None)
    return redirect(url_for('index'))

@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard - only accessible to logged-in admins"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))
    
    # Get all activities
    activities = Activity.query.all()
    return render_template('admin/dashboard.html', activities=activities, admin_role=session['admin_role'])

@app.route('/admin/activity/new', methods=['GET', 'POST'])
def create_activity():
    """Create new activity - only accessible to admins"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        bot_name = request.form.get('bot_name', 'Default Bot')
        
        new_activity = Activity(
            title=title,
            description=description,
            bot_name=bot_name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(new_activity)
        db.session.commit()
        
        flash('Activity created successfully')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/create_activity.html')

@app.route('/admin/activity/<int:activity_id>/edit', methods=['GET', 'POST'])
def edit_activity(activity_id):
    """Edit an activity - only accessible to admins"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))
    
    activity = Activity.query.get_or_404(activity_id)
    
    if request.method == 'POST':
        activity.title = request.form['title']
        activity.description = request.form['description']
        activity.bot_name = request.form.get('bot_name', 'Default Bot')
        activity.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Activity updated successfully')
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin/edit_activity.html', activity=activity)

@app.route('/admin/activity/<int:activity_id>/delete', methods=['POST'])
def delete_activity(activity_id):
    """Delete an activity - only accessible to admins"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))

    activity = Activity.query.get_or_404(activity_id)

    # Delete related keywords and content
    keywords = Keyword.query.filter_by(activity_id=activity_id).all()
    for keyword in keywords:
        # Delete related content
        Content.query.filter_by(keyword_id=keyword.id).delete()
        db.session.delete(keyword)

    db.session.delete(activity)
    db.session.commit()

    flash('Activity deleted successfully')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/activity/<int:activity_id>/keywords', methods=['GET'])
def manage_keywords(activity_id):
    """Manage keywords for an activity - only accessible to admins"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))

    activity = Activity.query.get_or_404(activity_id)
    keywords = Keyword.query.filter_by(activity_id=activity_id).all()

    return render_template('admin/manage_keywords.html', activity=activity, keywords=keywords)


@app.route('/admin/activity/<int:activity_id>/keyword/new', methods=['GET', 'POST'])
def create_keyword(activity_id):
    """Create a new keyword for an activity - only accessible to admins"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))

    activity = Activity.query.get_or_404(activity_id)

    if request.method == 'POST':
        keyword_text = request.form['keyword']

        # Check if keyword already exists for this activity
        if Keyword.query.filter_by(activity_id=activity_id, keyword=keyword_text).first():
            flash('Keyword already exists for this activity')
            return redirect(url_for('create_keyword', activity_id=activity_id))

        new_keyword = Keyword(
            activity_id=activity_id,
            keyword=keyword_text,
            created_at=datetime.utcnow()
        )

        db.session.add(new_keyword)
        db.session.commit()

        flash('Keyword created successfully')
        return redirect(url_for('manage_keywords', activity_id=activity_id))

    return render_template('admin/create_keyword.html', activity=activity)


@app.route('/admin/keyword/<int:keyword_id>/edit', methods=['GET', 'POST'])
def edit_keyword(keyword_id):
    """Edit a keyword - only accessible to admins"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))

    keyword = Keyword.query.get_or_404(keyword_id)

    if request.method == 'POST':
        keyword.keyword = request.form['keyword']
        db.session.commit()
        flash('Keyword updated successfully')
        return redirect(url_for('manage_keywords', activity_id=keyword.activity_id))

    return render_template('admin/edit_keyword.html', keyword=keyword)


@app.route('/admin/keyword/<int:keyword_id>/delete', methods=['POST'])
def delete_keyword(keyword_id):
    """Delete a keyword - only accessible to admins"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))

    keyword = Keyword.query.get_or_404(keyword_id)
    activity_id = keyword.activity_id

    # Delete related content
    Content.query.filter_by(keyword_id=keyword_id).delete()

    db.session.delete(keyword)
    db.session.commit()

    flash('Keyword deleted successfully')
    return redirect(url_for('manage_keywords', activity_id=activity_id))


@app.route('/admin/keyword/<int:keyword_id>/content', methods=['GET'])
def manage_content(keyword_id):
    """Manage content for a keyword - only accessible to admins"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))

    keyword = Keyword.query.get_or_404(keyword_id)
    content_items = Content.query.filter_by(keyword_id=keyword_id).all()

    return render_template('admin/manage_content.html', keyword=keyword, content_items=content_items)


@app.route('/admin/keyword/<int:keyword_id>/content/new', methods=['GET', 'POST'])
def create_content(keyword_id):
    """Create content for a keyword - only accessible to admins"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))

    keyword = Keyword.query.get_or_404(keyword_id)

    if request.method == 'POST':
        content_type = request.form['content_type']

        if content_type == 'text':
            content_text = request.form['content_text']
            new_content = Content(
                keyword_id=keyword_id,
                content_type=content_type,
                content_text=content_text,
                created_at=datetime.utcnow()
            )
        elif content_type == 'photo' and 'photo' in request.files:
            photo = request.files['photo']
            if photo and photo.filename != '':
                # Validate file extension
                allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
                if '.' in photo.filename and \
                   photo.filename.rsplit('.', 1)[1].lower() in allowed_extensions:

                    # Generate unique filename
                    import uuid
                    filename = f"{uuid.uuid4()}_{photo.filename}"
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

                    photo.save(filepath)

                    new_content = Content(
                        keyword_id=keyword_id,
                        content_type=content_type,
                        content_photo_path=f"images/{filename}",
                        created_at=datetime.utcnow()
                    )
                else:
                    flash('Invalid file type. Only PNG, JPG, JPEG, GIF files allowed.')
                    return redirect(url_for('create_content', keyword_id=keyword_id))
            else:
                flash('Please select a photo file')
                return redirect(url_for('create_content', keyword_id=keyword_id))
        else:
            flash('Invalid content type or missing content')
            return redirect(url_for('create_content', keyword_id=keyword_id))

        db.session.add(new_content)
        db.session.commit()

        flash('Content created successfully')
        return redirect(url_for('manage_content', keyword_id=keyword_id))

    return render_template('admin/create_content.html', keyword=keyword)

@app.route('/admin/users')
def manage_users():
    """Manage admin accounts - only accessible to root admin"""
    if 'admin_id' not in session or session.get('admin_role') != 'root':
        flash('Access denied')
        return redirect(url_for('admin_login'))
    
    admins = Admin.query.all()
    return render_template('admin/manage_users.html', admins=admins)

@app.route('/admin/user/new', methods=['GET', 'POST'])
def create_admin():
    """Create new admin account - only accessible to root admin"""
    if 'admin_id' not in session or session.get('admin_role') != 'root':
        flash('Access denied')
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'regular')
        
        # Check if admin already exists
        if Admin.query.filter_by(username=username).first():
            flash('Admin username already exists')
            return render_template('admin/create_admin.html')
        
        # Create new admin
        hashed_password = generate_password_hash(password)
        new_admin = Admin(
            username=username,
            password_hash=hashed_password,
            role=role,
            created_at=datetime.utcnow()
        )
        
        db.session.add(new_admin)
        db.session.commit()
        
        flash('Admin account created successfully')
        return redirect(url_for('manage_users'))
    
    return render_template('admin/create_admin.html')

@app.route('/admin/user/<int:admin_id>/edit', methods=['GET', 'POST'])
def edit_admin(admin_id):
    """Edit admin account - only accessible to root admin"""
    if 'admin_id' not in session or session.get('admin_role') != 'root':
        flash('Access denied')
        return redirect(url_for('admin_login'))

    admin = Admin.query.get_or_404(admin_id)

    # Prevent root admin from changing their role to regular
    if admin.id == session['admin_id'] and admin.role == 'root':
        current_role = admin.role
    else:
        current_role = admin.role

    if request.method == 'POST':
        # Prevent root admin from demoting themselves
        form_role = request.form.get('role', 'regular')
        if admin.id == session['admin_id'] and current_role == 'root' and form_role != 'root':
            flash("Root admins cannot change their role")
            return redirect(url_for('edit_admin', admin_id=admin_id))

        admin.username = request.form['username']
        new_password = request.form.get('password')
        if new_password:  # Only update password if provided
            admin.password_hash = generate_password_hash(new_password)
        # Only update role if it's not a root admin trying to demote themselves
        if admin.id != session['admin_id'] or form_role == 'root':
            admin.role = form_role

        db.session.commit()
        flash('Admin account updated successfully')
        return redirect(url_for('manage_users'))

    return render_template('admin/edit_admin.html', admin=admin)

@app.route('/admin/user/<int:admin_id>/delete', methods=['POST'])
def delete_admin(admin_id):
    """Delete admin account - only accessible to root admin"""
    if 'admin_id' not in session or session.get('admin_role') != 'root':
        flash('Access denied')
        return redirect(url_for('admin_login'))
    
    admin = Admin.query.get_or_404(admin_id)
    
    # Prevent root admin from deleting themselves
    if admin.id == session['admin_id']:
        flash("You can't delete your own account")
        return redirect(url_for('manage_users'))
    
    db.session.delete(admin)
    db.session.commit()
    
    flash('Admin account deleted successfully')
    return redirect(url_for('manage_users'))

@app.route('/admin/profile', methods=['GET', 'POST'])
def admin_profile():
    """Admin profile - for regular admins to change password"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))

    admin = Admin.query.get_or_404(session['admin_id'])

    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        # Verify current password
        if not check_password_hash(admin.password_hash, current_password):
            flash('Current password is incorrect')
            return render_template('admin/profile.html', admin=admin)

        # Check if new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match')
            return render_template('admin/profile.html', admin=admin)

        # Update password
        admin.password_hash = generate_password_hash(new_password)
        db.session.commit()
        flash('Password updated successfully')

    return render_template('admin/profile.html', admin=admin)


@app.route('/admin/profile/delete', methods=['POST'])
def delete_own_admin_account():
    """Allow regular admins to delete their own account"""
    if 'admin_id' not in session:
        flash('Please login as admin')
        return redirect(url_for('admin_login'))

    admin = Admin.query.get_or_404(session['admin_id'])
    admin_role = session.get('admin_role')

    # Regular admins can delete their own account, root admins can only delete via manage_users
    if admin_role == 'regular':
        db.session.delete(admin)
        db.session.commit()
        session.clear()  # Clear session after account deletion
        flash('Your admin account has been deleted successfully')
        return redirect(url_for('index'))
    else:
        flash('Root admins cannot delete their account from this page')
        return redirect(url_for('admin_profile'))

if __name__ == '__main__':
    app.run(debug=True)