import os

from flask import Flask, redirect, jsonify, request, Response, render_template, session, url_for
from flask_pymongo import PyMongo
from flask_session import Session

from repositories.member_repo import MemberRepository
from bson.objectid import ObjectId
from .config import Config
from .oauth import get_redirect_to_authorise_url, get_user_access_token, get_user_oauth_session, get_sso_attributes, get_request_token_with_callback

import hashlib

app = Flask(__name__)

app.config.from_object(Config)

mongo = PyMongo(app)
members = MemberRepository(mongo.db)

app.config['SESSION_MONGODB'] = mongo.db

Session(app)

@app.route('/redirect/<id>')
def get_redirect(id):
    if not ObjectId.is_valid(id):
        return render_template('error_id.html')

    session['id'] = id

    return render_template('redirect.html', title='Authorize')

@app.route('/oauth/begin')
def get_begin_oauth():
    id = session.get('id')

    if not id:
        return render_template('error_id.html')

    record = members.find_record_for_id(id)

    if not record:
        return render_template('error_id.html')

    if record['isVerified']:
        return render_template('success.html', title='Success')
    else:
        request_token = get_request_token_with_callback(id, f'{Config.BASE_URL}/oauth/authorized')
        session['request_token_secret'] = request_token['secret']

        return get_redirect_to_authorise_url(request_token['token'])

@app.route('/oauth/authorized')
def get_authorised_oauth():
    request_token_secret = session.get('request_token_secret')

    if not request_token_secret:
        raise Exception('Invalid request OAuth secret')

    access_token = get_user_access_token(request_token_secret)
    oauth_session = get_user_oauth_session(access_token['token'], access_token['secret'])
    ww_data = get_sso_attributes(oauth_session)

    id = session.get('id')

    student_id_hash = hashlib.sha256(ww_data['id'].encode('utf-8')).hexdigest()

    if members.find_record_for_student_id_hash(student_id_hash):
        return render_template('error.html', title='Already in use',
            message='This Warwick ITS account has already been used to verify a Discord account. Please use a different Warwick ITS account.',
            contact=False)

    if ww_data['member'] == 'true':
        members.verify_member(id, True)
        members.set_student_id_hash(id, student_id_hash)

        session.clear()
        return render_template('success.html', title='Success')
    
    return render_template('error.html', title='Not affiliated',
            message='Unfortunately you\'re not a member of the university and hence cannot be verified.',
            contact=False)

@app.route('/privacy')
def get_privacy_policy():
    return render_template('privacy.html', title='Privacy Policy')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', title='Page not found', message='The page you\'re looking for was not found!', contact=False), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', title='Internal error', message='An internal error ocurred.', contact=True), 500