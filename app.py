from flask import (
    Flask, render_template, redirect, url_for, flash)
from utils import get_env, create_folder_name, form_validate
from werkzeug import secure_filename
from boto3 import client
from forms import NetworkUpload
import os
from pipe_design import design_format
from pipe_velocity import velocity_format
from gutter_spread import spread_format

application = app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024

s3 = client('s3')
S3_BUCKET = get_env('S3_BUCKET')

format_error = 'File format not supported!'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NetworkUpload()

    if form.validate_on_submit():
        if form.design_submit.data:
            form_validation = form_validate(form.design_files.data, 21)
            if form_validation == 'validated':
                design_files = form.design_files.data
                design_names = [secure_filename(file.filename)
                                for file in design_files]
                folder_name = create_folder_name()
                s3_keys_csv = []
                for i, file in enumerate(design_files):
                    file.seek(0)
                    s3_key_csv = ''.join(['design', '/', folder_name, '/',
                                          'csv', '/', design_names[i]])
                    s3.put_object(Bucket=S3_BUCKET, Key=s3_key_csv, Body=file)
                    s3_keys_csv.append(s3_key_csv)
                hgl_toggle = (form.design_hgl_toggle.data)
                response = design_format(s3, S3_BUCKET, s3_keys_csv,
                                         folder_name, design_names,
                                         hgl_toggle)
                if not response:
                    flash(format_error, 'danger')
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('download',
                                            s3_key_xlsx=response))
            else:
                flash(form_validation, 'danger')
                return redirect(url_for('index'))

        if form.velocity_submit.data:
            form_validation = form_validate(form.velocity_files.data, 13)
            if form_validation == 'validated':
                velocity_files = form.velocity_files.data
                velocity_names = [secure_filename(file.filename)
                                  for file in velocity_files]
                folder_name = create_folder_name()
                s3_keys_csv = []
                for i, file in enumerate(velocity_files):
                    file.seek(0)
                    s3_key_csv = ''.join(['velocity', '/', folder_name, '/',
                                          'csv', '/', velocity_names[i]])
                    s3.put_object(Bucket=S3_BUCKET, Key=s3_key_csv, Body=file)
                    s3_keys_csv.append(s3_key_csv)
                fps_toggle = (form.velocity_fps_toggle.data)
                response = velocity_format(s3, S3_BUCKET, s3_keys_csv,
                                           folder_name, velocity_names,
                                           fps_toggle)
                if not response:
                    flash(format_error, 'danger')
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('download',
                                            s3_key_xlsx=response))
            else:
                flash(form_validation, 'danger')
                return redirect(url_for('index'))

        if form.spread_submit.data:
            form_validation = form_validate(form.spread_files.data, 14)
            if form_validation == 'validated':
                spread_files = form.spread_files.data
                spread_names = [secure_filename(file.filename)
                                for file in spread_files]
                folder_name = create_folder_name()
                s3_keys_csv = []
                for i, file in enumerate(spread_files):
                    file.seek(0)
                    s3_key_csv = ''.join(['spread', '/', folder_name, '/',
                                          'csv', '/', spread_names[i]])
                    s3.put_object(Bucket=S3_BUCKET, Key=s3_key_csv, Body=file)
                    s3_keys_csv.append(s3_key_csv)
                bypass_toggle = (form.spread_bypass_toggle.data)
                response = spread_format(s3, S3_BUCKET, s3_keys_csv,
                                         folder_name, spread_names,
                                         bypass_toggle)
                if not response:
                    flash(format_error, 'danger')
                    return redirect(url_for('index'))
                else:
                    return redirect(url_for('download',
                                            s3_key_xlsx=response))
            else:
                flash(form_validation, 'danger')
                return redirect(url_for('index'))

    return render_template('index.html', form=form)


@app.route('/download/<path:s3_key_xlsx>')
def download(s3_key_xlsx):
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET,
                'Key': s3_key_xlsx},
        ExpiresIn=100
    )
    return redirect(url, code=302)


@app.route('/design_report')
def design_report():
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET,
                'Key': 'static/design.rpt'},
        ExpiresIn=100
    )
    return redirect(url, code=302)


@app.route('/velocity_report')
def velocity_report():
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET,
                'Key': 'static/velocity.rpt'},
        ExpiresIn=100
    )
    return redirect(url, code=302)


@app.route('/spread_report')
def spread_report():
    url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': S3_BUCKET,
                'Key': 'static/spread.rpt'},
        ExpiresIn=100
    )
    return redirect(url, code=302)


@app.errorhandler(404)
def page_not_found(error):
    title = 'Page Not Found'
    return render_template('404.html', title=title)


@app.errorhandler(413)
def files_too_large(error):
    title = 'Files Too Large'
    return render_template('413.html', title=title)


@app.errorhandler(500)
def internal_error(error):
    title = 'Internal Server Error'
    return render_template('500.html', title=title)


if __name__ == '__main__':
    app.debug = True
    app.run()
