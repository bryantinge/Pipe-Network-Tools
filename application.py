from flask import Flask, render_template, redirect, url_for, send_file
from flask_wtf import FlaskForm
from wtforms.fields import MultipleFileField, SubmitField
from werkzeug import secure_filename
from utils import get_env, file_validate, create_folder_name
import os
import boto3
import pipe_design
import pipe_velocity
import gutter_spread

application = app = Flask(__name__)

SECRET_KEY = os.urandom(32)
ALLOWED_EXTENSIONS = ['.txt']
app.config['SECRET_KEY'] = SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024

s3 = boto3.client('s3')
S3_BUCKET = get_env('S3_BUCKET') 

class network_upload(FlaskForm):
    design_files = MultipleFileField('Select Pipe Design Files')
    design_submit = SubmitField('Format Pipe Design Files')

    velocity_files = MultipleFileField('Select Pipe Velocity Files')
    velocity_submit = SubmitField('Format Pipe Velocity Files')

    spread_files = MultipleFileField('Select Gutter Spread Files')
    spread_submit = SubmitField('Format Gutter Spread Files')   

@app.route('/', methods=['GET', 'POST'])
def index():
    form = network_upload()

    if form.validate_on_submit(): 

        if form.design_submit.data:
            if file_validate(form.design_files.data, ALLOWED_EXTENSIONS):
                design_files = form.design_files.data
                design_names = [secure_filename(file.filename) for file in design_files]
                folder_name = create_folder_name()
                s3_keys_csv = []
                for i, file in enumerate(design_files):
                    s3_key_csv = ''.join(['design', '/', folder_name, '/', 'csv', '/', design_names[i]])
                    s3.put_object(Bucket=S3_BUCKET, Key=s3_key_csv, Body=file)
                    s3_keys_csv.append(s3_key_csv)
                design_xlsx = pipe_design.main(s3, S3_BUCKET, s3_keys_csv, folder_name, design_names)
                return design_xlsx
            else:
                return redirect(url_for('index'))

        if form.velocity_submit.data:
            if file_validate(form.velocity_files.data, ALLOWED_EXTENSIONS):            
                velocity_files = form.velocity_files.data
                velocity_names = [secure_filename(file.filename) for file in velocity_files]
                folder_name = create_folder_name()
                s3_keys_csv = []
                for i, file in enumerate(velocity_files):
                    s3_key_csv = ''.join(['velocity', '/', folder_name, '/', 'csv', '/', velocity_names[i]])
                    s3.put_object(Bucket=S3_BUCKET, Key=s3_key_csv, Body=file)
                    s3_keys_csv.append(s3_key_csv)
                velocity_xlsx = pipe_velocity.main(s3, S3_BUCKET, s3_keys_csv, folder_name, velocity_names)    
                return velocity_xlsx
            else:
                return redirect(url_for('index'))

        if form.spread_submit.data:
            if file_validate(form.spread_files.data, ALLOWED_EXTENSIONS):
                spread_files = form.spread_files.data
                spread_names = [secure_filename(file.filename) for file in spread_files]
                folder_name = create_folder_name()
                s3_keys_csv = []
                for i, file in enumerate(spread_files):
                    s3_key_csv = ''.join(['spread', '/', folder_name, '/', 'csv', '/', spread_names[i]])
                    s3.put_object(Bucket=S3_BUCKET, Key=s3_key_csv, Body=file)
                    s3_keys_csv.append(s3_key_csv)
                spread_xlsx = gutter_spread.main(s3, S3_BUCKET, s3_keys_csv, folder_name, spread_names)
                return spread_xlsx
            else:
                return redirect(url_for('index'))

    return render_template('index.html', form=form)

@app.route('/design_report')
def design_report():
    return send_file('static/Design.rpt', mimetype='text/plain', 
    attachment_filename='Pipe Design.rpt', as_attachment=True)
	
@app.route('/velocity_report')
def velocity_report():
    return send_file('static/Velocity.rpt', mimetype='text/plain', 
    attachment_filename='Pipe Velocity.rpt', as_attachment=True)

@app.route('/spread_report')
def spread_report():
    return send_file('static/Spread.rpt', mimetype='text/plain', 
    attachment_filename='Gutter Spread.rpt', as_attachment=True)

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
    title = 'Files Not Valid'
    return render_template('500.html', title=title)

if __name__ == '__main__':
    app.debug = True
    app.run()
    