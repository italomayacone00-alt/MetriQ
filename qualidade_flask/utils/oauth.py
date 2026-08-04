"""
Configuração do OAuth para login com Google.

Para usar:
1. Crie um projeto no Google Cloud Console (https://console.cloud.google.com)
2. Ative a API "Google+ API" ou "Google Identity Services"
3. Crie credenciais OAuth 2.0 (Web application)
4. Adicione URI de redirecionamento: https://seudominio.com/login/google/callback
   (Em desenvolvimento: http://localhost:5000/login/google/callback)
5. Copie o Client ID e Client Secret para variáveis de ambiente:
   GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET
"""

from authlib.integrations.flask_client import OAuth

oauth = OAuth()

google = None


def configurar_oauth(app):
    """Configura o OAuth com Google (se as credenciais estiverem disponíveis)."""
    oauth.init_app(app)

    global google
    client_id = app.config.get('GOOGLE_CLIENT_ID')
    client_secret = app.config.get('GOOGLE_CLIENT_SECRET')

    if client_id and client_secret:
        google = oauth.register(
            name='google',
            client_id=client_id,
            client_secret=client_secret,
            server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
            client_kwargs={
                'scope': 'openid email profile',
                'prompt': 'select_account'
            }
        )
        return True
    else:
        return False
