from app import db
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import backref

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    produto = db.relationship('Produto', backref="user", passive_deletes=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def is_anonymous(self):
        return True


    def __init__(self, nome, username, password, email):
        self.nome = nome
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return "User %r" % self.username

class Categoria(db.Model):
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))

    produto = db.relationship('Produto',  backref="categoriax", passive_deletes=True)

    def __init__(self, nome):
        self.nome = nome

    def __repr__(self):
        return"Categoria %r" % self.nome

class Custos(db.Model):
    __tablename__ = "custos"

    id = db.Column(db.Integer, primary_key=True)
    idProduto = db.Column(db.Integer, db.ForeignKey('produtos.id', ondelete='CASCADE'))
    nome = db.Column(db.String(50), unique=True)
    qtd = db.Column(db.Integer)
    valor = db.Column(db.Float)

    def __init__(self, idProduto ,nome, qtd, valor):
        self.idProduto = idProduto
        self.nome = nome
        self.qtd = qtd
        self.valor = valor

    def __repr__(self):
        return " Custos %r" % self.nome


class Produto(db.Model):

    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    idUsuario = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))
    nome = db.Column(db.String(100))
    categoria = db.Column(db.Integer, db.ForeignKey('categorias.id', ondelete='CASCADE'))
    rendimento = db.Column(db.Integer)
    margemLucro = db.Column(db.Integer)

    custos = db.relationship('Custos', backref="produtox", passive_deletes=True)

    def __init__(self, idUsuario, nome, categoria, rendimento, margemLucro):
        self.idUsuario = idUsuario
        self.nome = nome
        self.categoria = categoria
        self.rendimento = rendimento
        self.margemLucro = margemLucro


    def __repr__(self):
        return "Produto %r" % self.nome
