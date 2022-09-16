import os.path

import werkzeug.datastructures
from flask import Blueprint
from flask_restful import Resource, marshal_with, fields, reqparse, inputs, marshal

from apps.user.model import User, Friend
from exts import api, db
from settings import Config

user_bp = Blueprint('user', __name__, url_prefix='/api')


class IsDelete(fields.Raw):
	def format(self, value):
		# print('-------------->', value)
		return '删除' if value else '未删除'


user_fields = {
	'id': fields.Integer,
	'username': fields.String,
	'uri': fields.Url('single_user', absolute=True),
}


user_fields_1 = {
	'id': fields.Integer,
	'username': fields.String,
	'password': fields.String,
	'isDelete': fields.Boolean(attribute='isdelete'),
	'isDelete1': IsDelete(attribute='isdelete'),
	'udatetime': fields.DateTime
}

# 参数解析
parser = reqparse.RequestParser()   # 解析对象
parser.add_argument('username', type=str, required=True, help='必须输入用户名')
parser.add_argument('password', type=str, required=True, help='必须输入密码')
parser.add_argument('phone', type=inputs.regex(r'^1[356789]\d{9}$'), location=['form'], help='手机号码格式错误')
parser.add_argument('icon', type=werkzeug.datastructures.FileStorage, location=['files', ])


# 定义类视图 (所有用户的操作)
class UserResource(Resource):
	# get请求的处理
	@marshal_with(user_fields_1)
	def get(self):
		users = User.query.all()
		# userList = []
		# for user in userList:
		# 	userList.append(user.__dict__)
		return users

	@marshal_with(user_fields)
	def post(self):
		args = parser.parse_args()
		username = args.get('username')
		password = args.get('password')
		phone = args.get('phone')
		icon = args.get('icon')
		# 创建user对象
		user = User()
		user.username = username
		user.password = password
		if icon:
			upload_path = os.path.join(Config.UPLOAD_ICON_DIR, icon.filename)
			icon.save(upload_path)
			# 保存路径
			user.icon = os.path.join('upload/icon', icon.filename)
		if phone:
			user.phone = phone
		db.session.add(user)
		db.session.commit()

		return user

	def put(self):
		pass

	def delete(self):
		pass


# 针对某一个用户的操作
class UserSimpleResource(Resource):
	@marshal_with(user_fields)   # 通过marshal_with()对返回的用户对象进行序列化转换
	def get(self, id):
		user = User.query.get(id)
		return user

	def put(self, id):
		pass


user_friend_fields = {
	'username': fields.String,
	'nums': fields.Integer,
	'friends': fields.List(fields.Nested(user_fields))

}


class UserFriendResource(Resource):
	@marshal_with(user_friend_fields)
	def get(self, id):
		friends = Friend.query.filter(Friend.uid == id).all()
		user = User.query.get(id)

		friend_list = []
		for friend in friends:
			u = User.query.get(friend.fid)
			friend_list.append(u)

		data = {
			'username': user.username,
			'nums': len(friends),
			'friends': friend_list   # 一个个user
		}
		return data


api.add_resource(UserResource, '/user', endpoint='all_user')
api.add_resource(UserSimpleResource, '/user/<int:id>', endpoint='single_user')
api.add_resource(UserFriendResource, '/friend/<int:id>', endpoint='user_friend')
