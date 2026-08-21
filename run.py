import os
from dotenv import load_dotenv
from qualidade_flask import create_app

# Carrega as variáveis de ambiente do arquivo .env (se existir)
# Permite configurar GROQ_API_KEY / GOOGLE_API_KEY / SECRET_KEY etc. sem depender do sistema.
load_dotenv()

app = create_app()

if __name__ == '__main__':
    # debug só é ligado explicitamente por variável de ambiente. Por padrão permanece desativado.
    debug_mode = os.environ.get('FLASK_DEBUG', '0').lower() in ('1', 'true', 'yes')
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
