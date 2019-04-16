from flask import Blueprint, json, request, render_template, redirect, url_for
from flask import flash, current_app
from flask_login import login_required, login_user, logout_user, UserMixin, \
    current_user
from .. import db, login_manager
from ..utils import get_sha256
from ..models import User, File
import os
import requests


main = Blueprint('main', __name__)


class LoginUser(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter(User.user_id == user_id).first()
    if user is not None:
        curr_user = LoginUser()
        curr_user.id = user.user_id
        curr_user.name = user.name
        return curr_user
    else:
        return None


def make_json(o):
    return json.jsonify(o)


@main.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.name)


@main.route('/signup', methods=['post', 'get'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        pwd_original = request.form.get('pwd')
        pwd = get_sha256(pwd_original)
        user = User(name=name, pwd=pwd)

        try:
            db.session.add(user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            flash('注册失败!')
            return redirect(url_for('.signup'))
        flash('注册成功, 请登录!')
        return redirect(url_for('.login'))
    else:
        return render_template('signup.html')


@main.route('/login', methods=['post', 'get'], endpoint='login')
def login():
    if request.method == 'POST':
        name = request.form.get('name')
        pwd_original = request.form.get('pwd')
        pwd = get_sha256(pwd_original)

        user = User.query.filter(User.name == name, User.pwd == pwd).first()

        if not user:
            flash('用户名或密码错误!')
            return redirect(url_for('.login'))
        else:
            luser = LoginUser()
            luser.id = user.user_id
            login_user(luser, remember=True)
            flash('登录成功!')
            return redirect(url_for('.index'))
    else:
        return render_template('login.html')


@main.route('/logout', methods=['post', 'get'])
def logout():
    logout_user()
    flash('注销成功!')
    return redirect(url_for('.index'))


@main.route('/models', methods=['post', 'get'])
@login_required
def get_models():
    files = File.query.filter(File.user_id == current_user.id).all()
    if request.method == 'POST':
        return make_json({
            'list': list(map(lambda x: {
                'modelid': x.modelid,
                'filename': x.filename
            }, files))
        })
    else:
        return render_template(
            'models.html',
            name=current_user.name,
            files=files)


@main.route('/models/<modelid>', methods=['get'])
@login_required
def get_modelview(modelid):
    return render_template(
        'fileview.html',
        modelid=modelid,
        clientid=current_app.config['CLIENTID'],
        name=current_user.name)


@main.route('/models/delete/<modelid>', methods=['get'])
@login_required
def delete_model(modelid):
    stp_file = File.query.filter(
        File.modelid == modelid,
        File.user_id == current_user.id
    ).first()
    if stp_file is not None:
        db.session.delete(stp_file)
        return redirect(url_for('.get_models'))
    else:
        flash('File not found!')
        return redirect(url_for('.get_models'))


def upload2everxyz(filepath):
    files = {'stpfile': open(filepath, 'rb')}
    url = current_app.config['EVERCAD_UPLOAD_URL']
    username = current_app.config['EVERCAD_USERNAME']
    pwd = current_app.config['EVERCAD_PWD']
    clientid = current_app.config['CLIENTID']

    r = requests.post(url, files=files, data={
        "username": username,
        "pwd": pwd,
        "clientid": clientid
    })

    res = r.json()

    if 'error' in res:
        return None
    else:
        return res['modelid']


@main.route('/upload', methods=['post', 'get'])
@login_required
def upload():
    if request.method == 'POST':
        print(current_app.config)
        folder = current_app.config['FILE_FOLDER']
        rev_file = request.files.get('stpfile')

        if rev_file is None:
            flash('请上传文件!')
            return render_template('upload.html')

        if not os.path.exists(folder):
            os.mkdir(folder)

        filepath = '{}/{}'.format(folder, rev_file.filename)
        rev_file.save(filepath)

        modelid = upload2everxyz(filepath)
        if modelid is None:
            flash('上传失败!')
            return render_template('upload.html')

        stp_file = File(
            user_id=current_user.id,
            filename=rev_file.filename,
            modelid=modelid
        )
        try:
            db.session.add(stp_file)
            db.session.commit()
            return render_template('upload.html',
                                   stp_file=stp_file,
                                   name=current_user.name)
        except Exception:
            flash('上传失败!')
            return render_template('upload.html')

    else:
        return render_template('upload.html', name=current_user.name)
