







# migrate = Migrate(app, db)

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(400), unique=True, nullable=False)
#     slug = db.Column(db.String(100), unique=True, nullable=False)
#     content = db.Column(db.Text, nullable=False)
#     created_at = db.Column(db.DateTime, nullable=True)
#     image = db.Column(db.String(30), nullable=True) 
    
#     def as_dict(self):
#         return {
#             'id': self.id,
#             'title': self.title,
#             'slug': self.slug,
#             'content': self.content,
#             'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
#         }



# class Contact(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(200), unique=True)
#     Phone_num = db.Column(db.String(20))
#     msg = db.Column(db.Text)



# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), unique=True, nullable=False)
#     password = db.Column(db.String(100), nullable=False)


