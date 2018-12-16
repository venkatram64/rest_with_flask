from src.user import User

users = [
    User(1, 'venkatram', 'venkat')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}

# users=[
#     {
#         'id':1,
#         'username':'bob',
#         'password':'bob'
#     }
# ]
#
# username_mapping = {
#     'bob':{
#         'id':1,
#         'username': 'bob',
#         'password': 'bob'
#     }
# }
#
# userid_mapping = {1: {
#     'id':1,
#     'username': 'bob',
#     'password': 'bob'
#     }
# }

def authenticate(username, password):

    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

