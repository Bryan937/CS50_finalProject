# LGA_WebApp

Video Demo: https://youtu.be/p-_xZnylFDU

Description:

LGA Network is a web-based application, using mainly python(flask), html and css. My website is a place where people can create and have access to worksheets created by other users from Grade 1 to 12 on a variety of subjects like Math, History, Biology and many more. The website can be used anonymously, meaning that one doesn't need to create an account to surf through the website. Any user can lookup any worksheets he/she desires and can use the menu or even use the worksheet filter to find the precise worksheets the user is looking for.

I designed my web application mainly with Flask because since I had just learned how to use it, I felt like I would be comfortable using it. Furthermore, I needed templates so Flask was perfect. To start I used sqlite3 as my database and I used Sqlalchemy as my sql server for my queries. I used Sqlalchemy because it is a server that works well with flask and it has a lot of features that ended up being useful for my project. One of flask features that was useful for this for my project is the Flask_login import that allow me to register and login user with no problems. Flask login also handle input error(eg invalid email or email and password not matching) Of course the password are hashed using bcrypt (I'm not storing them directly). After that some sql queries did the job of adding the registered user in the database. To send the data I used the POST method and to display the data I used the GET method as taught by CS50. To sign up, a person needs to provide an username, an email, a grade(1 to 12), a password and a confirmation. If their is an error the page will tell the user exactly what the problem is, so that the registration can be successful. Once registered, the person just needs to login and the process is completed. Of course, if the user email and password don't match, an error message will be shown to the user. Once a user has successfully logged in, he can now enjoy the website to its fullest. The authentication process is made with the Flask_login import. Important detail: Username and emails are unique so 2 users cannot have the same username and one user cannot have two username connected to the same email. All of the error handling in the Login and Register form is handle by Flask_Login and some if statements in Python.

Before talking about what a logged in user can do, let's talk about what an anonymous user (non-registered user) has access to. As an anonymous user

You can click on 'Worksheets' to see all the worksheets created by other users
You can click on 'Subject' or 'Grade' to see worksheets of a specific subject or grade
You can use the worksheet filter on the left of the page(that filter doesn't appear on all pages) to look for worksheets with a specific combination of a subject and a grade
You can click on a user name to see their profile and all the worksheets they created
As a registered user (You can do all the things an anonymous user can do and even more like):

You can click on 'New Worksheet' to create a new worksheet (You must fill all the fields in the worksheet creation form)
You can click on 'profile' to look at your profile that contains some of your info
You can click on 'My Worksheets' to see all the worksheets you created
You can click on 'Update Profile', to update either your username, email, grade or profile picture
You can click on a worksheet name to see the whole worksheet (Question and answer)
If you click on a worksheet you created you can click on update(to modify it) or delete(to delete it)
As a registered when you click on the logo your are brung to your feed which shows worksheets recommendations based on your grade
You can click 'Logout' to disconnect and turn to an anonymous user
Once in the website there are many routes that lead to different actions. I used the @app.route decorator to manage those routes. Some routes have the @login_required decorator, which means that a user must be logged to have access to this url path. The display of the different worksheets shown were the work of sql queries that acted according to the route which follows the users clicks or inputs. I used python classes and FlaskForms to do all the forms in my project (Login, sign up, creation of worksheet, update profile, etc..) so it was quite easy to manage them. I also added some bootstraps alerts when particular events happened (Successful sign up, successful profile update, etc..). I also used bootstrap and some sqlalchemy tools for the pagination of my pages.

Of course, I used css for all the style. Some it was from bootstrap, some of it was snippets from other people(I gave them credit in my code) and some (rather most of it) was my own.

I organised my files as packages to organise my project better so that it would be easier for me or someone else to look at my project source code. That means that I had a file just for my routes, a file just for my forms, a file just for my app configuration, etc. I was importing my own files in other files to make the whole thing work.

Overall my goal for this project was to create something useful that didn't necessarily require a login and that allowed the contribution of everyone regardless of age, location or any other constraint. I plan on working on it during my free time to improve it little by little. This whole semester was a challenge but I'm glad, I accepted that challenge.

This was LGA Networks! This was CSX50!!!
