redirect_home = '<script>window.setTimeout(function(){window.location.href = "/";}, 3000);</script>'
redirect_login = '<script>window.setTimeout(function(){window.location.href = "login";}, 3000);</script>'
# login
class LoginSuccess(Exception):
    def __init__(self):
        self.category = 'success'
        self.message = 'Login successfully! You will be redirected to home page in 3 seconds later.' + redirect_home
    def __str__(self):
        return self.category + '+' + self.message
class UsernameNotExists(Exception):
    def __init__(self):
        self.category = 'error'
        self.message = 'No this user...<br>You can <a href="/register">register</a> it or check your username and login again.'
    def __str__(self):
        return self.category + '+' + self.message
class WrongPassword(Exception):
    def __init__(self):
        self.category = 'error'
        self.message = 'Authenticate failed...'
    def __str__(self):
        return self.category + '+' + self.message
class HaveLogined(Exception):
    def __init__(self):
        self.category = 'warning'
        self.message = 'You have logined as <a href="/user/%s">%s</a>.'
    def __str__(self):
        return self.category + '+' + self.message

# register
class RegisterSuccess(Exception):
    def __init__(self):
        self.category = 'success'
        self.message = 'Register successfully! You have to receive an email to verify your registeration.'
    def __str__(self):
        return self.category + '+' + self.message
class InvaildUsername(Exception):
    def __init__(self):
        self.category = 'error'
        self.message = 'There can only be letters and numbers in your username.'
    def __str__(self):
        return self.category + '+' + self.message
class UsernameOrEmailExists(Exception):
    def __init__(self):
        self.category = 'error'
        self.message = 'Sorry, but the username or email address has been registered...'
    def __str__(self):
        return self.category + '+' + self.message
class EmailNotCorrect(Exception):
    def __init__(self):
        self.category = 'error'
        self.message = 'Sorry, your email address is incorrect. Please check it out.'
    def __str__(self):
        return self.category + '+' + self.message
class recaptchaVerifyError(Exception):
    def __init__(self):
        self.category = 'error'
        self.message = 'You have to verify that you are not a robot!'
    def __str__(self):
        return self.category + '+' + self.message

# set password
class SetPasswordSuccess(Exception):
    def __init__(self):
        self.category = 'success'
        self.message = 'Successfully set your password!'
    def __str__(self):
        return self.category + '+' + self.message
class PasswordsNotMatch(Exception):
    def __init__(self):
        self.category = 'error'
        self.message = 'Passwords doesn\'t match...'
    def __str__(self):
        return self.category + '+' + self.message
