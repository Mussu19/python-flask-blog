from flask import Flask,Blueprint, jsonify, redirect, session, render_template,request, flash,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
import os
import math
import json






with open('config.json', "r") as c:
    params = json.load(c)["param"]

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = 'hrfdaevbdfbibhjgnbmk'




app.config['UPLOAD_FOLDER'] = params['upload_file']
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.secret_key = 'super-secret-key'

ADMIN_EMAIL = "admin@gmail.com"
ADMIN_PASSWORD = "admin"


# app.config['BASIC_AUTH_USERNAME'] = 'Admin'
# app.config['BASIC_AUTH_PASSWORD'] = 'admin'
# basic_auth = BasicAuth(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123#@localhost:5432/flask_practice1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)




migrate = Migrate(app, db)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    image = db.Column(db.String(30), nullable=True) 
    
    def as_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def __repr__(self):
        return f"Post('{self.title}')"



class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(200), unique=True)
    Phone_num = db.Column(db.String(20))
    msg = db.Column(db.Text)



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)






@app.route('/')
def index():
    posts = Post.query.filter_by().all()
    last = math.ceil(len(posts)/int(params['no_of_posts']))
    
    page = request.args.get('page')
    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    posts = posts[(page-1)*int(params['no_of_posts']): (page-1)*int(params['no_of_posts'])+ int(params['no_of_posts'])]
    
    if (page==1):
        prev = "#"
        next = "/?page=" + str(page + 1)
    elif (page==last):
        prev = "/?page=" + str(page - 1)
        next = "#"
    else:
        prev = "/?page=" + str(page - 1)
        next = "/?page=" + str(page + 1)
    return render_template("index.html", params = params, posts= posts, prevs = prev, nexts = next)



@app.route("/about")
def about():
    return render_template("about.html", params = params)



# @app.route('/register', methods=['POST'])
# def register():
#         data = request.get_json()
#         username = data['username']
#         password = data['password']
        
#         user = User.query.filter_by(username= username).first()
        
#         if user and User.password:
#             return {"Message": "username already taken"}, 400
        
#         new_user = User(username=username, password= password)
#         db.session.add(new_user)
#         db.session.commit()
#         return {"Message": "user created successfully"}, 200



@app.route('/login', methods=['GET','POST'])
def login():
    if (request.method == "POST"):
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username= username).first()

        if user and user.password == password:
            post = Post.query.all()
            return render_template('dashboard.html',posts = post ,  params = params)

            
    return render_template('login.html', params = params)





@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return {"Message": current_user_id }, 200



@app.route('/logout')
def logout():
    session.pop('username', None)  # Clear the username from the session
    return redirect('/login')




@app.route("/edit/<int:id>", methods = ['GET', 'POST'])
def edit(id):
    if ('email' in session and session['email'] == ADMIN_EMAIL):
        if (request.method == 'POST'):
            id = request.form.get('id')
            title = request.form.get('title')
            slug = request.form.get('slug')
            content = request.form.get('content')
            image = request.form.get('image')
            
            created_at = request.form.get('created_at')
            
            if id == 0:
                post = Post(id = id, title = title, slug = slug, content= content, image = image, created_at = created_at)
                db.session.add(post)
                db.session.commit()
            else:
                post = Post.query.filter_by(id = id).first()
                post.id = id
                post.title = title
                post.slug = slug
                post.content = content
                post.image = image
                post.created_at = created_at
                db.session.commit()
                return redirect('/edit/'+ id)
    post = Post.query.filter_by(id= id).first()
    return render_template('edit.html', params = params, posts= post)




@app.route("/delete/<int:id>", methods = ['POST'])
def delete(id):
    if (request.method == 'POST'):
        post = Post.query.get_or_404(id)
        db.session.delete(post)
        db.session.commit()
        return redirect('/login')



@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file1' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file1']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            upload_folder = app.config['UPLOAD_FOLDER']
            file.save(os.path.join(upload_folder, filename))
            return "Upload Successfully"
    return render_template('dashboard,html', params= params)



@app.route("/contact", methods = ['GET','POST'])
def contact():
    if (request.method== 'POST'):
        name = request.form.get('name')
        email = request.form.get('email')
        Phone_num = request.form.get('Phone_num')
        msg = request.form.get('msg')
        
        
        new_user = Contact(name = name, email = email, Phone_num=Phone_num, msg= msg)
        db.session.add(new_user)
        db.session.commit()
    return render_template("contact.html", params = params)



@app.route("/post/<string:post_slug>", methods =['GET'])
def post_route(post_slug):
    post = Post.query.filter_by(slug = post_slug).first()
    return render_template("post.html", params= params, posts = post)



    


# @blog_blueprint.route("/login", methods = ['GET', 'POST'])
# # @basic_auth.required
# def login():
    
#     if ('email' in session and session['email'] == ADMIN_EMAIL):
#         post = Post.query.all()
#         return render_template('dashboard.html', params = params, posts = post)
    
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
#             # If the credentials are correct, redirect to admin dashboard
#             session['email'] = email
#             post = Post.query.all()
#             return render_template('dashboard.html', params = params, post = post)
#         else:
#             # If the credentials are incorrect, show an error message
#             error = 'Invalid credentials. Please try again.'
#             return render_template('login.html', error=error, params = params)
#     return render_template('login.html', params = params)



class ShowAllData(Resource):
    def get(self):
        data = Post.query.all()
        return jsonify([post.as_dict() for post in data])


class ShowSpecificData(Resource):
    def get(self, pk):
        data = Post.query.filter_by(id = pk).first()
        if data:
            data_dict = {
                'id': data.id,
                'title': data.title,
                'slug': data.slug,
                'content': data.content,
                'created_at': data.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'image': data.image
            }
            return jsonify(data_dict)
        return jsonify({"Message": "Data not found!"})


class AddNewData(Resource):
    def post(self):
        new_data = Post(
            id= request.json['id'],
            title= request.json['title'],
            slug= request.json['slug'],
            content= request.json['content'],
            created_at= request.json['created_at'],
            image= request.json['image'],
            
        )
        db.session.add(new_data)
        db.session.commit()
        return jsonify({"Message": "Add new data successfully!"})


class UpdateData(Resource):
    def put(self, pk):
        data = Post.query.filter_by(id=pk).first()
        if data:
            user = request.get_json()
            data.id = user['id'],
            data.title = user['title'],
            data.slug = user['slug'],
            data.content = user['content'],
            data.created_at = user['created_at'],
            data.image = user['image'],
            db.session.commit()
            return jsonify({"Message": "Your data update successfully"})
        return jsonify({"Message": "Data not found!"})


class DeleteData(Resource):
    def delete(self, pk):
        data = Post.query.filter_by(id=pk).first()
        if data:
            db.session.delete(data)
            db.session.commit()
            return jsonify({"Message": "Delete Successfully"})
        return jsonify({"Message": "Data not found!"})





api.add_resource(ShowAllData, '/alldata')
api.add_resource(ShowSpecificData, '/specificdata/<int:pk>')
api.add_resource(AddNewData, '/addnewdata')
api.add_resource(UpdateData, '/updatedata/<int:pk>')
api.add_resource(DeleteData, '/deletedata/<int:pk>')





if __name__ == '__main__':
    app.run(debug=True, port=5010)









