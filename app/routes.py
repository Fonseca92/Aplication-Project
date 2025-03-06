from flask import Blueprint, render_template, url_for, flash, redirect, request, current_app
from app import db
from app.models import User, Post
from app.forms import PostForm
import os
from werkzeug.utils import secure_filename
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

bp = Blueprint('main', __name__)

@bp.route('/')
@bp.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

@bp.route('/upload', methods=['GET', 'POST'])
def upload():
    form = PostForm()
    if form.validate_on_submit():
        if form.image.data:
            filename = secure_filename(form.image.data.filename)
            blob_service_client = BlobServiceClient.from_connection_string(
                f"DefaultEndpointsProtocol=https;AccountName={current_app.config['BLOB_ACCOUNT_NAME']};"
                f"AccountKey={current_app.config['BLOB_ACCOUNT_KEY']};EndpointSuffix=core.windows.net"
            )
            blob_client = blob_service_client.get_blob_client(
                container=current_app.config['BLOB_CONTAINER_NAME'],
                blob=filename
            )
            blob_client.upload_blob(form.image.data)
            image_url = blob_client.url
        else:
            image_url = None

        post = Post(
            title=form.title.data,
            author=form.author.data,
            body=form.body.data,
            image_path=image_url,
            user_id=1  # Change user_id as needed
        )
        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('upload.html', form=form)