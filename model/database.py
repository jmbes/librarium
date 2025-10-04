import os
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Date, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship

# Importa a biblioteca para manipular o sistema operacional
import os


# Obtém a pasta raiz do projeto (sobe 1 nível a partir de models/)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Caminho absoluto para a pasta data
#DB_PATH = os.path.join(BASE_DIR, "data", "librarium.db")


# Configuração do banco SQLite usando caminho absoluto
database_path = os.environ.get("DATA_DIR", "data")
engine = create_engine(f"sqlite:///{database_path}/librarium.db")

# Interpreta as classes de objetos como tabelas de banco de dados.
tabela = declarative_base()

# ========= TABELA DE USUÁRIOS =========
class Usuario(tabela):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    nascimento = Column(Date, nullable=False)
    endereco = Column(Text, nullable=False)
    telefone = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(255), nullable=False)
    tipo_de_usuario = Column(String(20), nullable=False)  # "Bibliotecário" ou "Leitor"
    ativo = Column(Boolean, default=True)

    # Relacionamento: um usuário pode ter vários empréstimos
    emprestimos = relationship('Emprestimo', back_populates='usuario')

    def __repr__(self):
        return f'Usuario: {self.nome} - CPF: {self.cpf} - Perfil: {self.tipo_de_usuario}'


# ========= TABELA DE LIVROS =========
class Livro(tabela):
    __tablename__ = 'livro'

    id = Column(Integer, primary_key=True)
    isbn = Column(String(25), unique=True, nullable=False)
    titulo = Column(String(100), nullable=False)
    autor = Column(Text, nullable=False)
    editora = Column(String(100), nullable=False)
    edicao = Column(String(15), nullable=True)
    volume = Column(Integer, nullable=True)
    genero = Column(String(100), nullable=False)
    numero_de_paginas = Column(Integer, nullable=False)
    ano_publicacao = Column(Integer, nullable=False)
    exemplares = Column(Integer, nullable=False)
    ativo = Column(Boolean, default=True)

    # Relacionamento: um livro pode ter vários empréstimos
    emprestimos = relationship('Emprestimo', back_populates='livro')

    def __repr__(self):
        return f'Livro: {self.titulo} - Autor: {self.autor} - Ativo: {self.ativo}'


# ========= TABELA DE EMPRÉSTIMO DE LIVROS =========
class Emprestimo(tabela):
    __tablename__ = 'emprestimo'

    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    id_livro = Column(Integer, ForeignKey('livro.id'), nullable=False)
    data_emprestimo = Column(DateTime, nullable=False)
    data_devolucao_prevista = Column(DateTime, nullable=False)
    status = Column(String(25), nullable=False)
    ativo = Column(Boolean, default=True)

    # Relacionamentos bidirecionais
    usuario = relationship('Usuario', back_populates='emprestimos')
    livro = relationship('Livro', back_populates='emprestimos')

    def __repr__(self):
        return (f'Emprestimo: {self.id} - Usuario: {self.id_usuario} '
                f'- Livro: {self.id_livro} - Status: {self.status}')


