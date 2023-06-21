#!/usr/bin/env python3
"""Forms for the Flask application"""
# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from wtforms.fields import SelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms_alchemy import ModelForm as WTFormsAlchemyModelForm
from uuid import UUID
from app.models import User, Store, Strain


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


class ModelForm(WTFormsAlchemyModelForm, FlaskForm):
    pass


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


class StrainForm(ModelForm):
    class Meta:
        model = Strain


class AddStrainForm(StrainForm):
    submit = SubmitField('Add Strain')


class UpdateStrainForm(StrainForm):
    strain = SelectField('Strain to Update', coerce=str)
    submit = SubmitField('Update Strain')


class DeleteStrainForm(FlaskForm):
    strain = SelectField('Strain to Delete', coerce=str)
    submit = SubmitField('Delete Strain')


class StoreForm(ModelForm):
    class Meta:
        model = Store


class AddStoreForm(StoreForm):
    submit = SubmitField('Add Store')
    related_strains = MultiCheckboxField(
        'Related Strains', choices=[], validators=[at_least_one_checkbox])


class UpdateStoreForm(StoreForm):
    store = SelectField('Store to Update', coerce=str)
    submit = SubmitField('Update Store')
    related_strains = MultiCheckboxField(
        'Related Strains', coerce=str, validators=[at_least_one_checkbox])


class DeleteStoreForm(FlaskForm):
    store = SelectField('Store to Delete', coerce=str)
    submit = SubmitField('Delete Store')


class UserForm(ModelForm):
    class Meta:
        model = User
        exclude = ['password_hash', 'verification_token', 'verified']


class AddUserForm(UserForm):
    role = SelectField('Role', choices=[('CLOUD_CONSUMER', 'Cloud Consumer'), (
        'CLOUD_PRODUCER', 'Cloud Producer'), ('CLOUD_VENDOR', 'Cloud Vendor')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Add User')


class UpdateUserForm(UserForm):
    user = SelectField('User', coerce=str, validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('CLOUD_CONSUMER', 'Cloud Consumer'), (
        'CLOUD_PRODUCER', 'Cloud Producer'), ('CLOUD_VENDOR', 'Cloud Vendor')], validators=[DataRequired()])
    submit = SubmitField('Update User')


class DeleteUserForm(FlaskForm):
    user = SelectField('User', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Delete User')


class StrainFilterForm(FlaskForm):
    strains = SelectMultipleField('Strains', coerce=str)
    submit = SubmitField('Filter')
