from flask import render_template, flash, redirect, url_for, jsonify, request, session
from app import app, db, lm, base
from app.models.forms import LoginForm, CreateUser, CreateCustos, CreateProduct
from app.models.tables import User, Categoria, Produto, Custos
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func



@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/createProduct", methods=['GET'])
def createProduto():
    return render_template('createProduct.html', formu=CreateProduct())

@app.route('/home')
def home():
    if session['usuario'] == 'sim':
        return render_template('home.html')
    else:
        return render_template('index.html')


@app.route('/teste', methods=["GET"])
def teste():
    listacategoria = Categoria.query.order_by(Categoria.id).all()
    categorias = []
    for i in listacategoria:
        categorias.append(i.nome)
    catego = jsonify({'categorias' : categorias})
    return catego

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            session['usuario'] = 'sim'
            session['usuario_id'] = user.id
            return redirect(url_for("home"))
            flash("Usuário logado")

        else:
            return redirect(url_for("index"))
    else:
        session['usuario'] = 'nao'
        session['usuario_id'] = ''
        flash("Login Inválido")

    return render_template('login.html',
                            form=form)


@app.route("/logout")
def logout():
    session['usuario'] = 'nao'
    session['usuario_id'] = ''
    logout_user()
    return redirect(url_for("index"))

@app.route("/createCustos", methods=["GET"])
def lerCusto():
    lista = Produto.query.filter_by(idUsuario = session['usuario_id']).all()
    use = None
    for i in lista:
        use = i.id
    print("MAX ID"+str(use))
    produto = Produto.query.filter_by(id = use).first()
    selecao = Custos.query.filter_by(idProduto = use).all()
    resultado = 0;
    for i in selecao:
        resultado = resultado + (i.valor*i.qtd)

        return render_template("createCustos.html", form=CreateCustos(), selecao=selecao, resultado=resultado)
    return render_template("createCustos.html", form=CreateCustos(), selecao=selecao, resultado=resultado)


@app.route("/createCustos", methods=["POST"])
def createCusto():
    lista = Produto.query.filter_by(idUsuario = session['usuario_id']).all()
    use = None
    for i in lista:
        use = i.id
    formu = CreateCustos()
    nome = request.json['nome']
    qtd  = request.json['qtd']
    valor = request.json['valor']
    if nome and qtd and valor:
        print('SAIDA DE DADOS'+nome+qtd+valor)
        custos = Custos(use, nome, qtd, valor)
        try:
            db.session.add(custos)
            db.session.commit()
        except Exception as e:
            raise e




@app.route("/createProduct", methods=["POST"])
def createProduct():
    formu = CreateProduct()
    nome = request.json['nome']
    categoria = request.json['categoria']
    categorias = Categoria.query.filter_by(nome = categoria).first()
    rendimento = request.json['rendimento']
    margemLucro = request.json['margemLucro']
    print ('O USUARIO É: '+str(session['usuario_id']))
    if nome and categorias.id and rendimento and margemLucro:
        produto = Produto(session['usuario_id'], nome, categorias.id, rendimento, margemLucro)
        db.session.add(produto)
        db.session.commit()





@app.route("/registerUser", methods=["GET", "POST"])
def registerUser():
    form = CreateUser()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.email.data).first()
        nome = form.nome.data
        username = form.username.data
        password = form.password.data
        email = form.email.data
        if nome and username and password and email:
            usuario = User(nome, username, password, email)
            db.session.add(usuario)
            db.session.commit()
            session['usuario'] = 'sim'
            return redirect(url_for("home"))

    return render_template('registerUser.html',
                        form=form);

@app.route("/resultado", methods=['GET'])
def resultado():
    lista = Produto.query.filter_by(idUsuario = session['usuario_id']).all()
    use = None
    for i in lista:
        use = i.id
    selecao = Custos.query.filter_by(idProduto = use).all()
    produto = Produto.query.filter_by(id = use).first()
    resultado = 0
    for i in selecao:
        resultado = resultado + (i.valor*i.qtd)
    valorFinal = (resultado+(resultado*(produto.margemLucro/100)))/produto.rendimento
    return render_template('resultado.html', produto=produto, selecao=selecao, resultado=resultado, valorFinal=round(valorFinal,2))

@app.route('/meusProdutos', methods=["GET"])
def meusProdutos():
    session['usuario_id']
    selecao = Produto.query.filter_by(idUsuario = session['usuario_id']).all()
    return render_template('meusProdutos.html', selecao=selecao);

@app.route('/rotas', methods=["GET"])
def rotas():
    id = request.args['id']
    produto = Produto.query.filter_by(id = id).first()
    if produto.idUsuario == session['usuario_id']:
        selecao = Custos.query.filter_by(idProduto = id).all()
        resultado = 0
        for i in selecao:
            resultado = resultado + (i.valor*i.qtd)
        valorFinal = (resultado+(resultado*(produto.margemLucro/100)))/produto.rendimento
        return render_template('resultado.html', produto=produto, selecao=selecao, resultado=resultado, valorFinal=round(valorFinal,2))

@app.route('/deletarProduto')
def deletarProduto():
    id = request.args['id']
    produto = Produto.query.filter_by(id=id).first()
    try:
        db.session.delete(produto)
        db.session.commit()
        return render_template('home.html');
    except Exception as e:
        raise
