"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template, url_for, request, jsonify, redirect, flash, session, abort
from NoteTakingAppProject import app
from repository import Repository
from functools import wraps

repo = Repository()
try:
    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' in session:
                return f(*args, **kwargs)
            else:
                flash("A login is required to see the page!")
                return redirect(url_for('start', next=request.path))
        return decorated_function

    @app.route('/')
    @app.route('/login', methods=['GET','POST'])
    def log_in():
        if request.method == "GET":
            try:
                return render_template('log_in.html',title='Log In Page',error='')
            except Exception as e:
                print("In GET Section of login")
                print(e);                   
        elif request.method =='POST':
            try:
                if request.form['username'] != '' and request.form['password']!='': 
                    if(repo.check_password(request.form['username'],request.form['password']) == True):
                        session['UserName'] = request.form['username']
                        userName = request.form['username']
                        return render_template('index.html',title='Home Page')
                    else:
                        return render_template('log_in.html',title='Log In Page', error = "Please type in the right credentials or sign up")
                else:
                    print("There was no Username entered")
            except Exception as e:
                print("In POST Section of login")
                print(e)
                return render_template('log_in.html',title='Log In Page', error="Please type in the right credentials or sign up")

    @app.route('/sign_up', methods=['GET','POST'])
    def sign_up():
        if request.method == "GET":
            try:
                return render_template('sign_up.html',title='Sign Up', error = '')
            except Exception as e:
                print("In GET Section of sign_up")
                print(e);                   
        elif request.method =='POST':
            try:
                print(request.form['newusername'],request.form['newpassword'])
                if request.form['newusername'] != '' and request.form['newpassword']!='':
                    repo.add_new_user(request.form['newusername'],request.form['newpassword'])
                    session['UserName'] = request.form['newusername']
                    return render_template('index.html',title='Home Page',error ='') 
                else:
                    print("There was no Username entered")           
            except Exception as e:
                print("In POST Section of sign_up")
                print(e)
                return render_template('sign_up.html',title='Sign Up', error ="There was an error, try signing up with different credentials") 

    @login_required
    @app.route('/home', methods=['GET','POST'])
    def home():
        if 'logout' in request.form:
            session.pop('userName', None)
            return redirect(url_for('log_in'))
        return render_template('index.html',title='Home Page')

    @login_required
    @app.route('/math', methods=['GET','POST'])
    def math():
        userName = session['UserName']
        if request.method == "GET":
            try:
                topicNames = []
                notesNames = []    
                userID = repo.get_user_id(userName)
                topicNames = repo.get_topics("Math",userID)
                notesNames = repo.get_notes("Math", userID)               
                topicNames = [i[0] for i in topicNames]
                notesNames = [i[0] for i in notesNames]             
                return render_template('math.html',title='Math',topicNames = topicNames, notesNames = notesNames)
            except Exception as e1:
                print("problem in Math GET Method in views.py")
                print(e1)
            
        elif request.method =='POST':
            try:
                if request.form['Topic'] != '':
                    topicSubmit = request.form['Topic']
                    notesSubmit = request.form['Notes']
                    userID = repo.get_user_id(userName)                     
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Math",userID)
                    notesNames = repo.get_notes("Math", userID)
                    if request.form['Notes'] == 'delete this':
                        repo.delete_topic("Math", topicSubmit, userID)
                    elif repo.check_topics("Math", userID, topicSubmit):
                        repo.update_notes("Math",topicSubmit, notesSubmit, userID)
                    else:
                        repo.add_to_subject_table("Math",topicSubmit, notesSubmit, userID)                        
                    userID = repo.get_user_id(userName)    
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Math",userID)
                    notesNames = repo.get_notes("Math", userID)                                  
                    topicNames = [i[0] for i in topicNames]
                    notesNames = [i[0] for i in notesNames]
                    return render_template('math.html',title='Math',topicNames = topicNames, notesNames = notesNames)
                else:
                    print("There was no Topic entered")
            except Exception as e2:
                print("problem in Math POST Method in views.py")
                print(e1)
      
    @login_required      
    @app.route('/english', methods=['GET','POST'])
    def english():
        userName = session['UserName']
        if request.method == "GET":
            try:
                topicNames = []
                notesNames = []    
                userID = repo.get_user_id(userName)
                topicNames = repo.get_topics("English",userID)
                notesNames = repo.get_notes("English", userID)               
                topicNames = [i[0] for i in topicNames]
                notesNames = [i[0] for i in notesNames]           
                return render_template('english.html',title='English',topicNames = topicNames, notesNames = notesNames)
            except Exception as e2:
                print("problem in English GET Method in views.py")
                print(e2)
        elif request.method =='POST':
             try:
                print("In the Post of English")
                if request.form['Topic'] != '':
                    print("Topic is not empty")
                    topicSubmit = request.form['Topic']
                    notesSubmit = request.form['Notes']
                    userID = repo.get_user_id(userName)            
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("English",userID)
                    notesNames = repo.get_notes("English", userID)
                    if request.form['Notes'] == 'delete this':
                        repo.delete_topic("English", topicSubmit, userID)
                    elif repo.check_topics("English", userID, topicSubmit):
                        repo.update_notes("English",topicSubmit, notesSubmit, userID)
                    else:
                        repo.add_to_subject_table("English",topicSubmit, notesSubmit, userID)                        
                    userID = repo.get_user_id(userName)                     
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("English",userID)
                    notesNames = repo.get_notes("English", userID)                                 
                    topicNames = [i[0] for i in topicNames]
                    notesNames = [i[0] for i in notesNames]
                    return render_template('english.html',title='English',topicNames = topicNames, notesNames = notesNames)
                else:
                    print("There was no Topic entered")
             except Exception as e2:
                print("problem in English POST Method in views.py")
                print(e1)
    @login_required       
    @app.route('/science', methods=['GET','POST'])
    def science():
        userName = session['UserName']
        if request.method == "GET":
            try:
                print(userName)
                topicNames = []
                notesNames = []    
                userID = repo.get_user_id(userName)
                topicNames = repo.get_topics("Science",userID)
                notesNames = repo.get_notes("Science", userID)               
                topicNames = [i[0] for i in topicNames]
                notesNames = [i[0] for i in notesNames]             
                return render_template('science.html',title='Science',topicNames = topicNames, notesNames = notesNames)
            except Exception as e1:
                print("problem in Science GET Method in views.py")
                print(e1)           
        elif request.method =='POST':
            try:
                if request.form['Topic'] != '':
                    topicSubmit = request.form['Topic']
                    notesSubmit = request.form['Notes']
                    userID = repo.get_user_id(userName)                 
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Science",userID)
                    notesNames = repo.get_notes("Science", userID)
                    if request.form['Notes'] == 'delete this':
                        repo.delete_topic("Science", topicSubmit, userID)
                    elif repo.check_topics("Science", userID, topicSubmit):
                        repo.update_notes("Science",topicSubmit, notesSubmit, userID)
                    else:
                        repo.add_to_subject_table("Science",topicSubmit, notesSubmit, userID) 
                    userID = repo.get_user_id(userName)                     
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Science",userID)
                    notesNames = repo.get_notes("Science", userID)                               
                    topicNames = [i[0] for i in topicNames]
                    notesNames = [i[0] for i in notesNames]
                    return render_template('science.html',title='Science',topicNames = topicNames, notesNames = notesNames)
                else:
                    print("There was no Topic entered")
            except Exception as e2:
                print("problem in Science POST Method in views.py")
                print(e1)
    @login_required        
    @app.route('/economics', methods=['GET','POST'])
    def economics():
        userName = session['UserName']
        if request.method == "GET":
            try:
                topicNames = []
                notesNames = []    
                userID = repo.get_user_id(userName)
                topicNames = repo.get_topics("Economics",userID)
                notesNames = repo.get_notes("Economics", userID)               
                topicNames = [i[0] for i in topicNames]
                notesNames = [i[0] for i in notesNames]
                
                return render_template('economics.html',title='Economics',topicNames = topicNames, notesNames = notesNames)
            except Exception as e1:
                print("problem in Economics GET Method in views.py")
                print(e1)
            
        elif request.method =='POST':
            try:
                if request.form['Topic'] != '':
                    topicSubmit = request.form['Topic']
                    notesSubmit = request.form['Notes']
                    userID = repo.get_user_id(userName)                  
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Economics",userID)
                    notesNames = repo.get_notes("Economics", userID)
                    if request.form['Notes'] == 'delete this':
                        repo.delete_topic("Economics", topicSubmit, userID)
                    elif repo.check_topics("Economics", userID, topicSubmit):
                        repo.update_notes("Economics",topicSubmit, notesSubmit, userID)
                    else:
                        repo.add_to_subject_table("Economics",topicSubmit, notesSubmit, userID)   
                    userID = repo.get_user_id(userName)                     
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Economics",userID)
                    notesNames = repo.get_notes("Economics", userID)                                
                    topicNames = [i[0] for i in topicNames]
                    notesNames = [i[0] for i in notesNames]

                    return render_template('economics.html',title='Economics',topicNames = topicNames, notesNames = notesNames)
                else:
                    print("There was no Topic entered")
            except Exception as e2:
                print("problem in Economics POST Method in views.py")
                print(e1)
    @login_required        
    @app.route('/language', methods=['GET','POST'])
    def language():
        userName = session['UserName']
        if request.method == "GET":
             try:
                topicNames = []
                notesNames = []    
                userID = repo.get_user_id(userName)
                topicNames = repo.get_topics("Language",userID)
                notesNames = repo.get_notes("Language", userID)               
                topicNames = [i[0] for i in topicNames]
                notesNames = [i[0] for i in notesNames]            
                return render_template('language.html',title='Language',topicNames = topicNames, notesNames = notesNames)
             except Exception as e1:
                print("problem in Language GET Method in views.py")
                print(e1)
             
        elif request.method =='POST':
            try:
                if request.form['Topic'] != '':
                    topicSubmit = request.form['Topic']
                    notesSubmit = request.form['Notes']
                    userID = repo.get_user_id(userName)                
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Language",userID)
                    notesNames = repo.get_notes("Language", userID)
                    if request.form['Notes'] == 'delete this':
                        repo.delete_topic("Language", topicSubmit, userID)
                    elif repo.check_topics("Language", userID, topicSubmit):
                        repo.update_notes("Language",topicSubmit, notesSubmit, userID)
                    else:
                        repo.add_to_subject_table("Language",topicSubmit, notesSubmit, userID)   
                    userID = repo.get_user_id(userName)                 
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Language",userID)
                    notesNames = repo.get_notes("Language", userID)                           
                    topicNames = [i[0] for i in topicNames]
                    notesNames = [i[0] for i in notesNames]
                    return render_template('language.html',title='Language',topicNames = topicNames, notesNames = notesNames)
                else:
                    print("There was no Topic entered")
            except Exception as e2:
                print("problem in Language POST Method in views.py")
                print(e1)
    @login_required        
    @app.route('/computer', methods=['GET','POST'])
    def computer():
        userName = session['UserName']
        if request.method == "GET":
            try:
                topicNames = []
                notesNames = []    
                userID = repo.get_user_id(userName)
                topicNames = repo.get_topics("Computer",userID)
                notesNames = repo.get_notes("Computer", userID)               
                topicNames = [i[0] for i in topicNames]
                notesNames = [i[0] for i in notesNames]
                
                return render_template('computer.html',title='Computer',topicNames = topicNames, notesNames = notesNames)
            except Exception as e1:
                print("problem in Computer GET Method in views.py")
                print(e1)
                            
        elif request.method =='POST':
            try:
                if request.form['Topic'] != '':
                    topicSubmit = request.form['Topic']
                    notesSubmit = request.form['Notes']
                    userID = repo.get_user_id(userName)                   
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Computer",userID)
                    notesNames = repo.get_notes("Computer", userID)
                    if request.form['Notes'] == 'delete this':
                        repo.delete_topic("Computer", topicSubmit, userID)
                    elif repo.check_topics("Computer", userID, topicSubmit):
                        repo.update_notes("Computer",topicSubmit, notesSubmit, userID)
                    else:
                        repo.add_to_subject_table("Computer",topicSubmit, notesSubmit, userID)   
                    userID = repo.get_user_id(userName)                    
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Computer",userID)
                    notesNames = repo.get_notes("Computer", userID)
                                   
                    topicNames = [i[0] for i in topicNames]
                    notesNames = [i[0] for i in notesNames]

                    return render_template('computer.html',title='Computer',topicNames = topicNames, notesNames = notesNames)
                else:
                    print("There was no Topic entered")
            except Exception as e2:
                print("problem in Computer POST Method in views.py")
                print(e1)
    @login_required        
    @app.route('/art', methods=['GET','POST'])
    def art():
        userName = session['UserName']
        if request.method == "GET":
            try:
                topicNames = []
                notesNames = []    
                userID = repo.get_user_id(userName)
                topicNames = repo.get_topics("Art",userID)
                notesNames = repo.get_notes("Art", userID)               
                topicNames = [i[0] for i in topicNames]
                notesNames = [i[0] for i in notesNames]              
                return render_template('art.html',title='Art',topicNames = topicNames, notesNames = notesNames)
            except Exception as e1:
                print("problem in Art GET Method in views.py")
                print(e1)
        
            
        elif request.method =='POST':
            try:
                if request.form['Topic'] != '':
                    topicSubmit = request.form['Topic']
                    notesSubmit = request.form['Notes']
                    userID = repo.get_user_id(userName)  
                    
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Art",userID)
                    notesNames = repo.get_notes("Art", userID)
                    if request.form['Notes'] == 'delete this':
                        repo.delete_topic("Art", topicSubmit, userID)
                    elif repo.check_topics("Art", userID, topicSubmit):
                        repo.update_notes("Art",topicSubmit, notesSubmit, userID)
                    else:
                        repo.add_to_subject_table("Art",topicSubmit, notesSubmit, userID)  
                    userID = repo.get_user_id(userName)  
                    
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Art",userID)
                    notesNames = repo.get_notes("Art", userID)
                                   
                    topicNames = [i[0] for i in topicNames]
                    notesNames = [i[0] for i in notesNames]

                    return render_template('art.html',title='Art',topicNames = topicNames, notesNames = notesNames)
                else:
                    print("There was no Topic entered")
            except Exception as e2:
                print("problem in Art POST Method in views.py")
                print(e1)
    @login_required        
    @app.route('/philosophy', methods=['GET','POST'])
    def philosophy():
        userName = session['UserName']
        if request.method == "GET":
            try:
                topicNames = []
                notesNames = []    
                userID = repo.get_user_id(userName)
                topicNames = repo.get_topics("Philosophy",userID)
                notesNames = repo.get_notes("Philosophy", userID)               
                topicNames = [i[0] for i in topicNames]
                notesNames = [i[0] for i in notesNames]
                
                return render_template('philosophy.html',title='Philosophy',topicNames = topicNames, notesNames = notesNames)
            except Exception as e1:
                print("problem in Philosophy GET Method in views.py")
                print(e1)
        
            
        elif request.method =='POST':
            try:
                if request.form['Topic'] != '':
                    topicSubmit = request.form['Topic']
                    notesSubmit = request.form['Notes']
                    userID = repo.get_user_id(userName)  
                    
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Philosophy",userID)
                    notesNames = repo.get_notes("Philosophy", userID)
                    if request.form['Notes'] == 'delete this':
                        repo.delete_topic("Philosophy", topicSubmit, userID)
                    elif repo.check_topics("Philosophy", userID, topicSubmit):
                        repo.update_notes("Philosophy",topicSubmit, notesSubmit, userID)
                    else:
                        repo.add_to_subject_table("Philosophy",topicSubmit, notesSubmit, userID)  
                    userID = repo.get_user_id(userName)  
                    
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Philosophy",userID)
                    notesNames = repo.get_notes("Philosophy", userID)
                                   
                    topicNames = [i[0] for i in topicNames]
                    notesNames = [i[0] for i in notesNames]

                    return render_template('philosophy.html',title='Philosophy',topicNames = topicNames, notesNames = notesNames)
                else:
                    print("There was no Topic entered")
            except Exception as e2:
                print("problem in Philosophy POST Method in views.py")
                print(e1)
    @login_required        
    @app.route('/history', methods=['GET','POST'])
    def history():
        userName = session['UserName']
        if request.method == "GET":
            try:
                topicNames = []
                notesNames = []    
                userID = repo.get_user_id(userName)
                topicNames = repo.get_topics("History",userID)
                notesNames = repo.get_notes("History", userID)               
                topicNames = [i[0] for i in topicNames]
                notesNames = [i[0] for i in notesNames]
                
                return render_template('history.html',title='History',topicNames = topicNames, notesNames = notesNames)
            except Exception as e1:
                print("problem in History GET Method in views.py")
                print(e1)
        
            
        elif request.method =='POST':
            try:
                if request.form['Topic'] != '':
                    topicSubmit = request.form['Topic']
                    notesSubmit = request.form['Notes']
                    userID = repo.get_user_id(userName)  
                    
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("History",userID)
                    notesNames = repo.get_notes("History", userID)
                    if request.form['Notes'] == 'delete this':
                        repo.delete_topic("History", topicSubmit, userID)
                    elif repo.check_topics("History", userID, topicSubmit):
                        repo.update_notes("History",topicSubmit, notesSubmit, userID)
                    else:
                        repo.add_to_subject_table("History",topicSubmit, notesSubmit, userID)
                    userID = repo.get_user_id(userName)  
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("History",userID)
                    notesNames = repo.get_notes("History", userID)
                                   
                    topicNames = [i[0] for i in topicNames]
                    notesNames = [i[0] for i in notesNames]

                    return render_template('history.html',title='History',topicNames = topicNames, notesNames = notesNames)
                else:
                    print("There was no Topic entered")
            except Exception as e2:
                print("problem in History POST Method in views.py")
                print(e1)
    @login_required        
    @app.route('/other', methods=['GET','POST'])
    def other():
        userName = session['UserName']
        if request.method == "GET":
            try:
                topicNames = []
                notesNames = []    
                userID = repo.get_user_id(userName)
                topicNames = repo.get_topics("Other",userID)
                notesNames = repo.get_notes("Other", userID)               
                topicNames = [i[0] for i in topicNames]
                notesNames = [i[0] for i in notesNames]
                
                return render_template('other.html',title='Other',topicNames = topicNames, notesNames = notesNames)
            except Exception as e1:
                print("problem in Other GET Method in views.py")
                print(e1)
        
            
        elif request.method =='POST':
            try:
                if request.form['Topic'] != '':
                    topicSubmit = request.form['Topic']
                    notesSubmit = request.form['Notes']
                    userID = repo.get_user_id(userName)  
                  
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Other",userID)
                    notesNames = repo.get_notes("Other", userID)
                    if request.form['Notes'] == 'delete this':
                        repo.delete_topic("Other", topicSubmit, userID)
                    elif repo.check_topics("Other", userID, topicSubmit):
                        repo.update_notes("Other",topicSubmit, notesSubmit, userID)
                    else:
                        repo.add_to_subject_table("Other",topicSubmit, notesSubmit, userID) 
                    userID = repo.get_user_id(userName)  
                    
                    topicNames = []
                    notesNames = []
                    topicNames = repo.get_topics("Other",userID)
                    notesNames = repo.get_notes("Other", userID)
                                   
                    topicNames = [i[0] for i in topicNames]
                    notesNames = [i[0] for i in notesNames]

                    return render_template('other.html',title='Other',topicNames = topicNames, notesNames = notesNames)
                else:
                    print("There was no Topic entered")
            except Exception as e2:
                print("problem in Other POST Method in views.py")
                print(e1)
            
except Exception as e:
    print("problem in views.py")
    print(e)