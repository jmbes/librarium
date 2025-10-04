# Importa os modulos do Flask.
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from sqlalchemy.orm import sessionmaker
from model.database import engine, Livro

# Cria uma instância do Blueprint.
blueprint = Blueprint("book_management", __name__)

# Cria uma sessão do back-end com o banco de dados.
Session = sessionmaker(bind=engine)

@blueprint.route("/books")
def list_book():
    connection = Session()
    livros = connection.query(Livro).all()  # traz todos os livros
    connection.close()
    return render_template("book-list.html", livros=livros)

# Rota para cadastrar o livro
@blueprint.route("/register-book", methods= ["GET", "POST"])
def register_book():

    # Verifica se o usuário está logado.
    if "user_id" not in session:

        # Retorna uma mensagem de erro.
        flash("Para acessar o software faça login...", "warning")

        # Redireciona o usuário para o INDEX
        return redirect(url_for("user_authentication.login"))
    
    else:

        # Verifica se existe uma requisição de processamento de dados
        if request.method == "POST":

            # Abre a conexão com o banco de dados
            connection = Session()

            # Recupera os dados enviados pelo formulário de HTML 
            isbn = request.form["isbn"]
            titulo = request.form["titulo"]
            autor = request.form["autor"]
            editora = request.form["editora"]
            edicao = request.form["edicao"]
            volume = request.form["volume"]
            genero = request.form["genero"]
            num_paginas = request.form["num_paginas"]
            ano_publicacao = request.form["ano_publicacao"]
            qtd_exemplares = request.form["qtd_exemplares"]
            
            # Verifica se o livro já existe no banco de dados.
            existe = connection.query(Livro).filter_by(isbn=isbn).first()

            if existe:
                # Envia uma mensagem de erro
                flash("ISBN já existe", "danger")

                # Fechar a conexão com o banco de dados
                connection.close()

                # Redireciona para o HTML de listagem de livros 
                return redirect(url_for("book_management.list_book"))
            
            else:

                # Cria um novo objeto.
                novo_livro = Livro (
                    isbn=isbn,
                    titulo=titulo,
                    autor=autor,
                    editora=editora,
                    edicao=edicao,
                    volume=int(volume),
                    genero=genero,
                    numero_de_paginas=int(num_paginas),
                    ano_publicacao=int(ano_publicacao),
                    exemplares=int(qtd_exemplares)
                )

                # Adiciona o objeto no banco de dados
                connection.add(novo_livro)

                # Confirma a transacao
                connection.commit()

                # Fecha a conexão com o banco de dados
                connection.close()

                # Envia umamensagem de sucesso
                flash("Livro cadastrado com sucesso!", "success")
                
                # Redireciona para o HTML de listagem de livros 
                return redirect(url_for("book_management.list_book"))
            
        else:

            # Renderiza o HTML de cadastro de livro
            return render_template("book-register.html")
        
# Rota para editar um livro
@blueprint.route("/edit-book/<int:id>", methods=["GET", "POST"])
def edit_book(id):
    connection = Session()
    livro = connection.query(Livro).get(id)
    if not livro:
        flash("Livro não encontrado", "danger")
        connection.close()
        return redirect(url_for("book_management.list_book"))

    if request.method == "POST":
        livro.titulo = request.form["titulo"]
        livro.autor = request.form["autor"]
        livro.editora = request.form["editora"]
        livro.edicao = request.form["edicao"]
        livro.volume = int(request.form["volume"])
        livro.genero = request.form["genero"]
        livro.numero_de_paginas = int(request.form["num_paginas"])
        livro.ano_publicacao = int(request.form["ano_publicacao"])
        livro.exemplares = int(request.form["qtd_exemplares"])

        connection.commit()
        connection.close()
        flash("Livro atualizado com sucesso!", "success")
        return redirect(url_for("book_management.list_book"))

    connection.close()
    return render_template("book-register.html", livro=livro)

# Rota para excluir um livro
@blueprint.route("/delete-book/<int:id>")
def delete_book(id):
    connection = Session()
    livro = connection.query(Livro).get(id)
    if livro:
        connection.delete(livro)
        connection.commit()
        flash("Livro excluído com sucesso!", "success")
    else:
        flash("Livro não encontrado", "danger")
    connection.close()
    return redirect(url_for("book_management.list_book"))

@blueprint.route("/manage-books")
def manage_books():
    if "user_id" not in session:
        flash("Para acessar o software faça login...", "warning")
        return redirect(url_for("user_authentication.login"))
    return render_template("book-menu.html")
