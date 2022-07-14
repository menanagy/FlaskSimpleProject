from wtforms import Form,StringField,PasswordField,TextAreaField,validators

class RegisterForm (Form):
    name = StringField('Name', [validators.Length(min=4,max=20)])
    username = StringField('Username', [validators.Length(min=4,max=15)])
    email = StringField('Email', [validators.Length(min=6,max=50)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

# class Login (Form):
#         username = StringField('Username', [validators.Length(min=4,max=15)])
#         password = PasswordField('Password', [
#         validators.DataRequired(),
#     ])


class Add_Article_form (Form):
    title=StringField('Title', [validators.Length(min=5,max=25)])
    content=TextAreaField('Content', [validators.Length(min=30)])
