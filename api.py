# from flask import Flask,Blueprint, jsonify, redirect, session, render_template,request, flash
# from app import api, Post,Contact, User, db
# from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_restful import Resource



# class ShowAllData(Resource):
#     def get(self):
#         data = Post.query.all()
#         return jsonify(data)


# class ShowSpecificData(Resource):
#     def get(self, pk):
#         data = Post.query.filter_by(id = pk).first()
#         if data:
#             data_dict = {
#                 'id': data.id,
#                 'book_name': data.book_name,
#                 'author_name': data.author_name
#             }
#             return jsonify(data_dict)
#         return jsonify({"Message": "Data not found!"})


# class AddNewData(Resource):
#     def post(self):
#         new_data = Post(
#             id= request.json['id'],
#             book_name= request.json['book_name'],
#             author_name= request.json['author_name']
#         )
#         db.session.add(new_data)
#         db.session.commit()
#         return jsonify({"Message": "Add new data successfully!"})


# class UpdateData(Resource):
#     def put(self, pk):
#         data = Post.query.filter_by(id=pk).first()
#         if data:
#             user = request.get_json()
#             data.id = user['id'],
#             data.book_name = user['book_name'],
#             data.author_name = user['author_name']
#             db.session.commit()
#             return jsonify({"Message": "Your data update successfully"})
#         return jsonify({"Message": "Data not found!"})


# class DeleteData(Resource):
#     def delete(self, pk):
#         data = Post.query.filter_by(id=pk).first()
#         if data:
#             db.session.delete(data)
#             db.session.commit()
#             return jsonify({"Message": "Delete Successfully"})
#         return jsonify({"Message": "Data not found!"})





# api.add_resource(ShowAllData, '/alldata')
# api.add_resource(ShowSpecificData, '/specificdata/<int:pk>')
# api.add_resource(AddNewData, '/addnewdata')
# api.add_resource(UpdateData, '/updatedata/<int:pk>')
# api.add_resource(DeleteData, '/deletedata/<int:pk>')


