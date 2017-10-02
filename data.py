import pendulum

data = {
    'users': {
        1: {
            'username':
            'natec425',
            'password':
            'fakepass',
            'id':
            1,
            'wall': [{
                'author_id': 2,
                'author': 'mmclark',
                'timestamp': pendulum.now(),
                'message': 'Hey There'
            }]
        },
        2: {
            'username': 'mmclark',
            'password': 'badpass',
            'id': 2,
            'wall': []
        }
    }
}
next_ids = {'user': 3}
usernames = {'natec425': 1, 'mmclark': 2}


def create_user(username, password):
    id = next_ids['user']
    next_ids['user'] += 1
    data['users'][id] = {
        'username': username,
        'password': password,
        'id': id,
        'posts': []
    }
    usernames[username] = id
    return data['users'][id]


def username_is_taken(username):
    return username in usernames


def get_user(id):
    return data['users'].get(id)


def valid_user_pass(username, password):
    id = usernames.get(username)
    if id is None:
        return False

    return data['users'][id]['password'] == password


def get_user_by_name(username):
    id = usernames.get(username)
    if id is None:
        return None

    return data['users'][id]


def add_comment(wall_owner, author, message):
    wall_owner['wall'].insert(0, {
        'author_id': author['id'],
        'author': author['username'],
        'message': message,
        'timestamp': pendulum.now()
    })


def all_users():
    return data['users'].values()
