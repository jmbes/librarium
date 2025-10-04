# Importa o módulo do back-end que configura a aplicação da web.
from controller import create_application

# Cria uma instância da aplicação da web.
web_application = create_application()

# Verifica se está executnado o arquivo de gatilho 

if __name__ == "__main__":

    # Inicia o servidor local da aplicacao da web em modo de depuração.
    web_application.run(debug=True)
    