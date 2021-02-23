from flask import Flask, render_template,request,redirect,url_for, flash# For flask implementation
from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient
from models import Person
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

title = "SAMPLE REGISTERATION"
heading = "REGISTERATION FORM"

client = MongoClient("mongodb://127.0.0.1:27017") #host uri
db = client.mydatabase #Select the database
db_variable = db.register #Select the collection name

def redirect_url():
    return request.args.get('next') or \
        request.referrer or \
        url_for('index')

@app.route("/list")
def lists ():
    #Display the all Tasks
    todos_l = db_variable.find()
    a1="active"
    return render_template('index.html',a1=a1,db_variable=todos_l,t=title,h=heading)

@app.route("/")
@app.route("/status_uncompleted")
def tasks ():
    #Display the Uncompleted Tasks
    todos_l = db_variable.find({"done":"no"})
    a2="active"
    return render_template('index.html',a2=a2,db_variable=todos_l,t=title,h=heading)

@app.route("/completed")
def completed ():
    #Display the Completed Tasks
    todos_l = db_variable.find({"done":"yes"})
    a3="active"
    return render_template('index.html',a3=a3,db_variable=todos_l,t=title,h=heading)

@app.route("/done")
def done ():
    #Done-or-not Status ICON
    id=request.values.get("_id")
    task=db_variable.find({"_id":ObjectId(id)})
    if(task[0]["done"]=="yes"):
        db_variable.update({"_id":ObjectId(id)}, {"$set": {"done":"no"}})
    else:
        db_variable.update({"_id":ObjectId(id)}, {"$set": {"done":"yes"}})
    redir=redirect_url()    
    return redirect(redir)

@app.route("/action", methods=['POST'])
def action ():
    #Adding a Task
    name=request.values.get("name")
    email=request.values.get("email")
    password=request.values.get("password")
    mobile=request.values.get("mobile")
    address=request.values.get("address")
    db_variable.insert({ "name":name, "email":email, "password":password, "mobile":mobile,"address":address, "done":"no"})
    return redirect("/list")

@app.route("/remove")
def remove ():
    #Deleting a Task with various references
    key=request.values.get("_id")
    db_variable.remove({"_id":ObjectId(key)})
    return redirect("/")

@app.route("/update")
def update ():
    id=request.values.get("_id")
    task=db_variable.find({"_id":ObjectId(id)})
    return render_template('update.html',tasks=task,h=heading,t=title)

@app.route("/action3", methods=['POST'])
def action3 ():
    #Updating a Task with various references
    name=request.values.get("name")
    email=request.values.get("email")
    password=request.values.get("password")
    mobile=request.values.get("mobile")
    address=request.values.get("address")
    id=request.values.get("_id")
    db_variable.update({"_id":ObjectId(id)}, {'$set':{ "name":name, "email":email, "password":password, "mobile":mobile ,"address":address}})
    return redirect("/")

@app.route("/search", methods=['GET'])
def search():
    #Searching a Task with various references
    key=request.values.get("key")
    refer=request.values.get("refer")
    if(key=="_id"):
        todos_l = db_variable.find({refer:ObjectId(key)})
    else:
        todos_l = db_variable.find({refer:key})
    return render_template('searchlist.html',db_variable=todos_l,t=title,h=heading)
# To upload image on file
UPLOAD_FOLDER = '/home/apptrinity19/sample_project/media'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['SECRET_KEY']="wfdwyg"

@app.route('/upload')
def upload_file_h():
   return render_template('upload.html')


@app.route('/success')
def success_file():
   return render_template('success.html')
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        if f.filename == '':
            flash('No file selected for uploading')
            return redirect('/upload')
        if f:
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect('/success')

        
if __name__ == '__main__':
   app.run(debug = True)