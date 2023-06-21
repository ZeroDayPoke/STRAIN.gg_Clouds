#!/usr/bin/env python3
"""Forms for the Flask application"""
# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from uuid import UUID
from app.models import User, Store, Strain, Role

# Custom form fields
class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [str(UUID(x)) for x in valuelist]
        else:
            self.data = []

    def process_data(self, value):
        if value:
            self.data = [str(x) for x in value]
        else:
            self.data = []


def at_least_one_checkbox(form, field):
    if not any(field.data):
        raise ValidationError("At least one checkbox should be checked.")

# Auth Forms
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('CLOUD_CONSUMER', 'Cloud Consumer'), (
        'CLOUD_PRODUCER', 'Cloud Producer'), ('CLOUD_VENDOR', 'Cloud Vendor')], validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class SigninForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')

# Strain Forms
class AddStrainForm(FlaskForm):
    name = StringField('Strain Name', validators=[DataRequired()])
    type = StringField('Type')
    delta_nine_concentration = StringField('Delta Nine Concentration')
    cbd_concentration = StringField('CBD Concentration')
    terpene_profile = StringField('Terpene Profile')
    effects = StringField('Effects')
    uses = StringField('Uses')
    flavor = StringField('Flavor')
    submit = SubmitField('Submit')


class UpdateStrainForm(FlaskForm):
    strain = SelectField('Strain to Update', coerce=str)
    name = StringField('Updated Strain Name', validators=[DataRequired()])
    type = StringField('Updated Type')
    delta_nine_concentration = StringField('Updated Delta Nine Concentration')
    cbd_concentration = StringField('Updated CBD Concentration')
    terpene_profile = StringField('Updated Terpene Profile')
    effects = StringField('Updated Effects')
    uses = StringField('Updated Uses')
    flavor = StringField('Updated Flavor')
    submit = SubmitField('Update Strain')


class DeleteStrainForm(FlaskForm):
    strain = SelectField('Strain to Delete', coerce=str)
    submit = SubmitField('Delete Strain')

# Store Forms
class AddStoreForm(FlaskForm):
    name = StringField('Store Name', validators=[DataRequired()])
    location = StringField('Location')
    operating_hours = StringField('Operating Hours')
    submit = SubmitField('Submit')
    related_strains = MultiCheckboxField('Related Strains', coerce=str, validators=[at_least_one_checkbox])


class UpdateStoreForm(FlaskForm):
    store = SelectField('Store to Update', coerce=str)
    name = StringField('Updated Store Name', validators=[DataRequired()])
    location = StringField('Updated Location')
    operating_hours = StringField('Updated Operating Hours')
    submit = SubmitField('Update Store')
    related_strains = MultiCheckboxField('Related Strains', coerce=str, validators=[at_least_one_checkbox])

class DeleteStoreForm(FlaskForm):
    store = SelectField('Store to Delete', coerce=str)
    submit = SubmitField('Delete Store')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class UpdateUserForm(FlaskForm):
    user = SelectField('User', coerce=str, validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Update User')
    password = PasswordField('Password')
    roles = MultiCheckboxField('Roles', coerce=str, validators=[at_least_one_checkbox])

class DeleteUserForm(FlaskForm):
    user = SelectField('User', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Delete User')


class StrainFilterForm(FlaskForm):
    strains = SelectMultipleField('Strains', coerce=str)
    submit = SubmitField('Filter')

class AddUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('CLOUD_CONSUMER', 'CLOUD_CONSUMER'), ('CLOUD_PRODUCER', 'CLOUD_PRODUCER'), ('CLOUD_VENDOR', 'CLOUD_VENDOR')])
    submit = SubmitField('Add User')
