from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, FloatField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    remember_me = BooleanField("remember_me")

class CreateUser(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])

class CreateProduct(FlaskForm):
    nome = StringField("nome", validators=[DataRequired()])
    categoria = StringField("categoria", validators=[DataRequired()])
    margemLucro = IntegerField("margemLucro", validators=[DataRequired()])
    rendimento = IntegerField("rendimento", validators=[DataRequired()])

class CreateCustos(FlaskForm):
    idProduto = IntegerField("idProduto", validators=[DataRequired()])
    nome = StringField("nome", validators=[DataRequired()])
    qtd = StringField("qnt", validators=[DataRequired()])
    valor = FloatField("valor", validators=[DataRequired()])
