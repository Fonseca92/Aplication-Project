from flask import Blueprint, render_template, redirect, url_for, session, request
import msal
import uuid
from app import db
from app.models import User, Article
from config import Config
import logging

views_bp = Blueprint('views', __name__)

def _build_msal_app(cache=None):
    return msal.ConfidentialClientApplication(
        Config.CLIENT_ID, authority=Config.AUTHORITY,
        client_credential=Config.CLIENT_SECRET, token_cache=cache)

def _build_auth_url(scopes=None, state=None):
    return _build_msal_app().get_authorization_request_url(
        scopes or [],
        state=state or str(uuid.uuid4()),
        redirect_uri=url_for('views.auth_response', _external=True))

@views_bp.route('/login')
def login():
    session['state'] = str(uuid.uuid4())
    auth_url = _build_auth_url(scopes=Config.SCOPE, state=session['state'])
    return render_template('login.html', auth_url=auth_url)

@views_bp.route(Config.REDIRECT_PATH)
def auth_response():
    if request.args.get('state') != session.get('state'):
        logging.warning("Invalid state parameter during Microsoft Sign-In")
        return redirect(url_for('main.index'))

    if 'error' in request.args:
        logging.error(f"Microsoft Sign-In error: {request.args['error']}")
        return redirect(url_for('main.index'))

    client = _build_msal_app()
    token_response = client.acquire_token_by_authorization_code(
        request.args['code'],
        scopes=Config.SCOPE,
        redirect_uri=url_for('views.auth_response', _external=True)
    )

    if 'access_token' in token_response:
        session['user'] = token_response.get('id_token_claims')
        logging.info(f"User {session['user']['name']} logged in successfully")
        return redirect(url_for('views.dashboard'))
    else:
        logging.warning("Failed to acquire access token during Microsoft Sign-In")
        return redirect(url_for('main.index'))

@views_bp.route('/dashboard')
def dashboard():
    if 'user' not in session:
        logging.warning("Unauthorized access attempt to dashboard")
        return redirect(url_for('main.index'))
    return render_template('dashboard.html', user=session['user'])

@views_bp.route('/logout')
def logout():
    session.pop('user', None)
    logging.info("User logged out successfully")
    return redirect(url_for('main.index'))

@views_bp.route('/create', methods=['GET', 'POST'])
def create_article():
    if 'user' not in session:
        logging.warning("Unauthorized access attempt to create article")
        return redirect(url_for('main.index'))

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        image = request.files['image']

        if image:
            blob_service_client = BlobServiceClient.from_connection_string(Config.BLOB_CONNECTION_STRING)
            blob_client = blob_service_client.get_blob_client(container=Config.BLOB_CONTAINER_NAME, blob=image.filename)
            blob_client.upload_blob(image)
            image_url = blob_client.url
        else:
            image_url = None

        article = Article(title=title, content=content, user_id=1, image_url=image_url)  # Change user_id as needed
        db.session.add(article)
        db.session.commit()
        logging.info(f"Article '{title}' created by {session['user']['name']}")
        return redirect(url_for('views.dashboard'))

    return render_template('create.html')