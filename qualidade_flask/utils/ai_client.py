"""
Cliente de IA centralizado com suporte a múltiplos provedores (Groq + Google AI Studio).

Estratégia de fallback:
1. Tenta Groq (mais rápido) - model "llama-3.3-70b-versatile"
2. Se falhar ou não tiver chave, tenta Google AI Studio (Gemini) - model "gemini-2.0-flash"
3. Se ambos falharem, retorna None (o chamador decide o fallback)

Formato de chamada padronizado (OpenAI-compatível):
    client.chat.completions.create(messages=..., model=..., temperature=..., max_tokens=...)
    resposta.choices[0].message.content
"""

import os
import json
import logging

# Garante que as variáveis de ambiente do arquivo .env sejam carregadas
# mesmo quando o módulo é importado por processos que não passam por run.py
# (ex: gunicorn, uwsgi, testes, etc.)
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

logger = logging.getLogger(__name__)

# ------------------------------------------------------------
# CONFIGURAÇÃO DOS PROVEDORES
# ------------------------------------------------------------
PROVIDER_GROQ = {
    "nome": "groq",
    "chave_env": "GROQ_API_KEY",
    "modelo_padrao": "llama-3.3-70b-versatile",
    "modelo_fallback": "llama-3.1-8b-instant",
    "import_path": "groq",
    "classe": "Groq",
    "base_url": None,  # usa o padrão da lib
}

PROVIDER_GOOGLE = {
    "nome": "google",
    "chave_env": "GOOGLE_API_KEY",
    "modelo_padrao": "gemini-2.5-flash",
    "modelo_fallback": "gemini-2.0-flash",
    "import_path": "openai",
    "classe": "OpenAI",
    "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
}

# Modelos por prioridade (para rotar se um falhar)
MODELOS_PRIORIDADE = [
    # Groq
    PROVIDER_GROQ["modelo_padrao"],
    PROVIDER_GROQ["modelo_fallback"],
    # Google
    PROVIDER_GOOGLE["modelo_padrao"],
    PROVIDER_GOOGLE["modelo_fallback"],
]


def _importar_cliente(provider):
    """Importa dinamicamente a classe do cliente (Groq ou OpenAI)."""
    try:
        modulo = __import__(provider["import_path"])
        classe = getattr(modulo, provider["classe"], None)
        if not classe:
            logger.error(f"Classe {provider['classe']} não encontrada em {provider['import_path']}")
            return None
        return classe
    except ImportError as e:
        logger.error(f"Erro ao importar {provider['import_path']}: {e}")
        return None


def _criar_cliente(provider):
    """Cria uma instância do cliente para o provider especificado."""
    chave = os.environ.get(provider["chave_env"])
    if not chave:
        logger.info(f"Chave {provider['chave_env']} não configurada. Provider {provider['nome']} desabilitado.")
        return None

    classe = _importar_cliente(provider)
    if not classe:
        return None

    try:
        if provider["base_url"]:
            return classe(api_key=chave, base_url=provider["base_url"])
        return classe(api_key=chave)
    except Exception as e:
        logger.error(f"Erro ao criar cliente {provider['nome']}: {e}")
        return None


def get_cliente_groq():
    """Retorna o cliente Groq ou None se não configurado."""
    return _criar_cliente(PROVIDER_GROQ)


def get_cliente_google():
    """Retorna o cliente Google (via OpenAI-compatível) ou None se não configurado."""
    return _criar_cliente(PROVIDER_GOOGLE)


def get_cliente_disponivel():
    """Retorna o primeiro cliente disponível (Groq primeiro)."""
    for provider in [PROVIDER_GROQ, PROVIDER_GOOGLE]:
        cliente = _criar_cliente(provider)
        if cliente:
            return cliente, provider
    return None, None


def get_modelo_para_provider(provider, usar_fallback=False):
    """Retorna o modelo a usar para o provider."""
    if usar_fallback:
        return provider["modelo_fallback"]
    return provider["modelo_padrao"]


def gerar_analise(messages, model=None, temperature=0.3, max_tokens=2000):
    """
    Função genérica que gera uma análise usando o primeiro provedor disponível.
    Tenta Groq primeiro, depois Google.

    Parâmetros:
        messages: lista de mensagens no formato OpenAI [{'role': 'system'|'user', 'content': ...}]
        model: modelo específico (opcional). Se None, usa o padrão do provider atual.
        temperature: criatividade (0-1)
        max_tokens: limite de tokens de resposta

    Retorno:
        (texto, provider_usado) ou (None, None) se ambos falharem.
    """
    # 1. Tenta Groq
    cliente_groq = get_cliente_groq()
    if cliente_groq:
        try:
            resposta = cliente_groq.chat.completions.create(
                messages=messages,
                model=model or PROVIDER_GROQ["modelo_padrao"],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            texto = resposta.choices[0].message.content
            if texto:
                return texto, "groq"
        except Exception as e:
            logger.warning(f"Groq falhou (principal): {e}")
            # Tenta modelo fallback da Groq
            try:
                resposta = cliente_groq.chat.completions.create(
                    messages=messages,
                    model=PROVIDER_GROQ["modelo_fallback"],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                texto = resposta.choices[0].message.content
                if texto:
                    return texto, "groq"
            except Exception as e2:
                logger.warning(f"Groq falhou (fallback): {e2}")

    # 2. Tenta Google
    cliente_google = get_cliente_google()
    if cliente_google:
        try:
            resposta = cliente_google.chat.completions.create(
                messages=messages,
                model=model or PROVIDER_GOOGLE["modelo_padrao"],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            texto = resposta.choices[0].message.content
            if texto:
                return texto, "google"
        except Exception as e:
            logger.warning(f"Google falhou (principal): {e}")
            try:
                resposta = cliente_google.chat.completions.create(
                    messages=messages,
                    model=PROVIDER_GOOGLE["modelo_fallback"],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                texto = resposta.choices[0].message.content
                if texto:
                    return texto, "google"
            except Exception as e2:
                logger.warning(f"Google falhou (fallback): {e2}")

    return None, None


def gerar_analise_json(messages, model=None, temperature=0.4, max_tokens=2000):
    """
    Versão que tenta forçar resposta JSON (para sugestões de ferramentas).
    Retorna o dict JSON parseado, ou None se falhar.
    """
    cliente_groq = get_cliente_groq()
    if cliente_groq:
        try:
            resposta = cliente_groq.chat.completions.create(
                messages=messages,
                model=model or PROVIDER_GROQ["modelo_padrao"],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            texto = resposta.choices[0].message.content
            return json.loads(texto), "groq"
        except Exception as e:
            logger.warning(f"Groq JSON falhou: {e}")

    cliente_google = get_cliente_google()
    if cliente_google:
        try:
            resposta = cliente_google.chat.completions.create(
                messages=messages,
                model=model or PROVIDER_GOOGLE["modelo_padrao"],
                temperature=temperature,
                max_tokens=max_tokens,
                response_format={"type": "json_object"},
            )
            texto = resposta.choices[0].message.content
            return json.loads(texto), "google"
        except Exception as e:
            logger.warning(f"Google JSON falhou: {e}")

    return None, None
