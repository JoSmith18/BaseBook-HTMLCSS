from string import printable, ascii_letters, digits, punctuation
from data import create_user, username_is_taken, valid_user_pass, get_user_by_name, get_user, add_comment


class CreateAccountForm:
    valid_username_letters = ascii_letters + digits
    valid_password_letters = ascii_letters + digits + punctuation

    def __init__(self,
                 username='',
                 password='',
                 passwordRepeat='',
                 from_user=False):

        self.username = username
        self.password = password
        self.passwordRepeat = passwordRepeat
        self.from_user = from_user

    def is_valid(self):
        return (self.username_is_valid() and self.password_is_valid() and
                self.passwords_match())

    def username_is_valid(self):
        return not self.username_errors

    @property
    def username_errors(self):
        if not self.from_user:
            return []

        errors = []
        if not (2 <= len(self.username) <= 15):
            errors.append('usernames must be 2-15 characters long')
        if not all(c in self.valid_username_letters for c in self.username):
            errors.append('usernames must only be letters and digits')
        if username_is_taken(self.username):
            errors.append('username is taken')
        return errors

    def password_is_valid(self):
        return not self.password_errors

    @property
    def password_errors(self):
        if not self.from_user:
            return []
        errors = []
        if not (6 <= len(self.password) <= 18):
            errors.append('passwords must be 6-18 characters long')
        if not all(c in self.valid_password_letters for c in self.password):
            errors.append(
                'passwords must only be letters, digits, and punctuation')
        return errors

    def passwords_match(self):
        return self.password == self.passwordRepeat

    @property
    def passwordRepeat_errors(self):
        if not self.from_user:
            return []
        if self.password != self.passwordRepeat:
            return ['passwords must match']
        else:
            return []

    @classmethod
    def from_request(cls, request):
        return cls(
            request.form.get('username'),
            request.form.get('password'),
            request.form.get('passwordRepeat'),
            True, )

    def create_account(self):
        return create_user(self.username, self.password)

    @property
    def success_url(self):
        return '/wall'


class LoginForm:
    def __init__(self, username='', password='', from_user=False):
        self.username = username
        self.password = password
        self.from_user = from_user

    def is_valid(self):
        return not self.from_user or valid_user_pass(self.username,
                                                     self.password)

    @classmethod
    def from_request(cls, request):
        return LoginForm(
            request.form.get('username'), request.form.get('password'), True)

    @property
    def user_id(self):
        return get_user_by_name(self.username)['id']


class CommentForm:
    def __init__(self, wall_owner, author, message='', from_user=False):
        self.wall_owner = wall_owner
        self.author = author
        self.message = message
        self.from_user = from_user

    @classmethod
    def from_request(cls, request, wall_owner, author):
        return CommentForm(
            wall_owner,
            author,
            request.form.get('message', ''),
            True, )

    def is_valid(self):
        return True

    def post_comment(self):
        print(self.__dict__)
        add_comment(self.wall_owner, self.author, self.message)
