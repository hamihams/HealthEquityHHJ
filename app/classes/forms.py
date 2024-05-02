# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

#HARRISON --> RUN THIS IN YOUR TERMINAL IF IT DOESNT WORK 
# python3 -m pip install --upgrade wtforms

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired, NumberRange
from wtforms.validators import URL, Email, DataRequired
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField, BooleanField, URLField, DateField, TimeField, EmailField, RadioField


class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Save')
    role = SelectField('Role',choices=[("Patient","Patient"),("Family Member","Family Member"), ("Healthcare Staff", "Healthcare Staff")])
    age = IntegerField('Age', validators=[NumberRange(min=15,max=110, message="Enter a number between 15 and 110.")])

class ConsentForm(FlaskForm):
    adult_fname = StringField('First Name',validators=[DataRequired()])
    adult_lname = StringField('Last Name',validators=[DataRequired()])
    adult_email = EmailField('Email',validators=[Email()])
    consent = RadioField('Do you allow your information ', choices=[(True,"True"),(False,"False")])
    submit = SubmitField('Submit')

class SleepForm(FlaskForm):
    rating = SelectField("How would you rate your sleep: 5 is great, 1 is poor", choices=[(None,'---'),(1,1),(2,2),(3,3),(4,4),(5,5)], validators=[DataRequired()])
    starttime = TimeField("Start Time")   
    endtime = TimeField("End Time")   
    feel = SelectField("How did you feel when you woke up: 5 is great, 1 is poor", choices=[(None,'---'),(1,1),(2,2),(3,3),(4,4),(5,5)], validators=[DataRequired()])
    sleep_date = DateField("What date did you go to sleep")
    wake_date = DateField("What date did you wake up")
    minstosleep = IntegerField("How many minutes did it take you to fall asleep?", validators=[NumberRange(min=0,max=180, message="Enter a number between 0 and 180.")])
    submit = SubmitField("Submit")

class BlogForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Blog', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    submit = SubmitField('Blog')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class ClinicForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streetAddress = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode',validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')

class HospitalForm(FlaskForm):
    type = SelectField('Type',choices=[("Public","Public"),("Private","Private"), ("Non Profit", "Non Profit")])
    image = FileField("Image") 
    safeNet = RadioField('Is it a Safety-Net Hospital?', choices=[(True,"Yes"),(False,"No/Unsure")])
    name = SelectField('Name',choices=[("Wilma Chan Highland Hospital","Wilma Chan Highland Hospital"),("Alta Bates Summit Medical Center","Alta Bates Summit Medical Center"), ("UCSF Benioff Children's Hospital", "UCSF Benioff Children's Hospital"), ("Kaiser Permanente", "Kaiser Permanente"), ("Fairmont Rehabilitation & Wellness", "Fairmont Rehabilitation & Wellness"), ("John George Psychiatric Pavilion", "John George Psychiatric Pavilion"), ("Alameda Hospital", "Alameda Hospital"), ("San Leandro Hospital","San Leandro Hospital")])
    street = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode',validators=[DataRequired()])
    rating = IntegerField('Rate your experience: 0 is terrible, 5 is amazing', validators=[NumberRange(min=0,max=5, message="Enter a number between 0 and 5.")])
    submit = SubmitField('Submit')

class ReviewForm(FlaskForm):
    name = SelectField('Hospital Name',choices=[("Wilma Chan Highland Hospital","Wilma Chan Highland Hospital"),("Alta Bates Summit Medical Center","Alta Bates Summit Medical Center"), ("UCSF Benioff Children's Hospital", "UCSF Benioff Children's Hospital"), ("Kaiser Permanente", "Kaiser Permanente"),])
    text = TextAreaField('Write your Review', validators=[DataRequired()])
    subject = SelectField('Exoeriences',choices=[("Patient Care", "Patient Care"), ("Visitor","Visitor"),("Waiting Duration","Waiting Duration"), ("Internship/Leanring Programs", "Internship/Leanring Programs"), ("Volunteer", "Volunteer"), ("Patient", "Patient"), ("Hospitality", "Hospitality"), ("Other","Other")])
    rating = IntegerField('Rate your experience: 0 is terrible, 10 is amazing', validators=[NumberRange(min=0,max=10, message="Enter a number between 0 and 10.")])
    submit = SubmitField('Post Review')

class ReplyForm(FlaskForm):
    text = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Post')