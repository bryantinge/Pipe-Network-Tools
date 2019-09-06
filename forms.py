from flask_wtf import FlaskForm
from wtforms.fields import MultipleFileField, BooleanField, SubmitField


class NetworkUpload(FlaskForm):
    design_files = MultipleFileField('Upload Pipe Design Files',
                                     id='design_input')
    design_hgl_toggle = BooleanField('Display HGL Elevations')
    design_submit = SubmitField('Format Pipe Design Files')

    velocity_files = MultipleFileField('Upload Pipe Velocity Files',
                                       id='velocity_input')
    velocity_fps_toggle = BooleanField('Highlight Velocities')
    velocity_submit = SubmitField('Format Pipe Velocity Files')

    spread_files = MultipleFileField('Upload Gutter Spread Files',
                                     id='spread_input')
    spread_bypass_toggle = BooleanField('Display Bypass Data')
    spread_submit = SubmitField('Format Gutter Spread Files')
