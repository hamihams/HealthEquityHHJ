from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Hospital
from app.classes.forms import HospitalForm
from flask_login import login_required
import datetime as dt

@app.route('/hospital/new', methods=['GET', 'POST'])
# This means the user must be logged in to see this page
@login_required
# This is a function that is run when the user requests this route.
def hospitalNew():
    # This gets the form object from the form.py classes that can be displayed on the template.
    form = HospitalForm()

    # This is a conditional that evaluates to 'True' if the user submitted the form successfully.
    # validate_on_submit() is a method of the form object. 
    if form.validate_on_submit():

        # This stores all the values that the user entered into the new blog form. 
        # Blog() is a mongoengine method for creating a new blog. 'newBlog' is the variable 
        # that stores the object that is the result of the Blog() method.  
        newHospital = Hospital(
            # the left side is the name of the field from the data table
            # the right side is the data the user entered which is held in the form object.
            type = form.type.data,
            image = form.image.data,
            name = form.name.data,
            safeNet = form.safeNet.data,
            city = form.city.data,
            street = form.street.data,
            state = form.state.data,
            zipcode = form.zipcode.data,
            rating = form.rating.data,
            author = current_user.id,
            # This sets the modifydate to the current datetime.
            modify_date = dt.datetime.utcnow
        )
        # This is a method that saves the data to the mongoDB database.
        newHospital.save()

        # Once the new blog is saved, this sends the user to that blog using redirect.
        # and url_for. Redirect is used to redirect a user to different route so that 
        # routes code can be run. In this case the user just created a blog so we want 
        # to send them to that blog. url_for takes as its argument the function name
        # for that route (the part after the def key word). You also need to send any
        # other values that are needed by the route you are redirecting to.
        return redirect(url_for('hospital',hospitalID=newHospital.id))

    # if form.validate_on_submit() is false then the user either has not yet filled out
    # the form or the form had an error and the user is sent to a blank form. Form errors are 
    # stored in the form object and are displayed on the form. take a look at blogform.html to 
    # see how that works.
    return render_template('hospitalsform.html',form=form)

@app.route('/hospital/<hospitalID>')
# This route will only run if the user is logged in.
@login_required
def hospital(hospitalID):
    # retrieve the blog using the blogID
    thisHospital = Hospital.objects.get(id=hospitalID)
    # If there are no comments the 'comments' object will have the value 'None'. Comments are 
    # related to blogs meaning that every comment contains a reference to a blog. In this case
    # there is a field on the comment collection called 'blog' that is a reference the Blog
    # document it is related to.  You can use the blogID to get the blog and then you can use
    # the blog object (thisBlog in this case) to get all the comments.
    
    # Send the blog object and the comments object to the 'blog.html' template.
    return render_template('hospital.html',hospital=thisHospital)

@app.route('/hospital/list')
@app.route('/hospitals')
# This means the user must be logged in to see this page
@login_required
def hospitalList():
    # This retrieves all of the 'blogs' that are stored in MongoDB and places them in a
    # mongoengine object as a list of dictionaries name 'blogs'.
    hospitals = Hospital.objects()
    # This renders (shows to the user) the blogs.html template. it also sends the blogs object 
    # to the template as a variable named blogs.  The template uses a for loop to display
    # each blog.
    return render_template('hospitals.html',hospitals=hospitals)

@app.route('/hospital/edit/<hospitalID>', methods=['GET', 'POST'])
@login_required
def hospitalEdit(hospitalID):
    editHospital = Hospital.objects.get(id=hospitalID)
    # if the user that requested to edit this blog is not the author then deny them and
    # send them back to the blog. If True, this will exit the route completely and none
    # of the rest of the route will be run.
    if current_user != editHospital.author:
        flash("You can't edit a post you don't own.")
        return redirect(url_for('hospital',hospitalID=hospitalID))
    # get the form object
    form = HospitalForm()
    # If the user has submitted the form then update the blog.
    if form.validate_on_submit():
        # update() is mongoengine method for updating an existing document with new data.
        editHospital.update(
            type = form.type.data,
            name = form.name.data,
            safeNet = form.safeNet.data,
            street = form.street.data,
            city = form.city.data,
            state = form.state.data,
            zipcode = form.zipcode.data,
            rating = form.rating.data,
            modify_date = dt.datetime.utcnow
        )

        if form.image.data:
            if editHospital.image:
                editHospital.image.delete()
            editHospital.image.put(form.image.data, content_type = 'image/jpeg')
            # This saves all the updates
            editHospital.save()
        # After updating the document, send the user to the updated blog using a redirect.
        return redirect(url_for('hospital',hospitalID=hospitalID))

    # if the form has NOT been submitted then take the data from the editBlog object
    # and place it in the form object so it will be displayed to the user on the template.
    form.type.data = editHospital.type
    form.image.data = editHospital.image
    form.name.data = editHospital.name
    form.safeNet.data = editHospital.safeNet
    form.street.data = editHospital.street
    form.city.data = editHospital.city
    form.state.data = editHospital.state
    form.zipcode.data = editHospital.zipcode
    form.rating.data = editHospital.rating
    
    return render_template('hospitalsform.html',form=form, hospital=editHospital)

@app.route('/hospital/delete/<hospitalID>')
# Only run this route if the user is logged in.
@login_required
def hospitalDelete(hospitalID):
    # retrieve the blog to be deleted using the blogID
    deleteHospital = Hospital.objects.get(id=hospitalID)
    # check to see if the user that is making this request is the author of the blog.
    # current_user is a variable provided by the 'flask_login' library.
    if current_user == deleteHospital.author:
        # delete the blog using the delete() method from Mongoengine
        deleteHospital.delete()
        # send a message to the user that the blog was deleted.
        flash('The post was deleted.')
    else:
        # if the user is not the author tell them they were denied.
        flash("You can't delete a post you don't own.")
    # Retrieve all of the remaining blogs so that they can be listed.
    hospitals = Hospital.objects()  
    # Send the user to the list of remaining blogs.
    return render_template('hospitals.html',hospitals=hospitals)