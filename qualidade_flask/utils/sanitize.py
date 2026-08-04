"""
Sanitização de HTML para proteger contra XSS (Cross-Site Scripting).

Usado principalmente no conteúdo gerado por IA (analise_ia, conclusao_geral)
que é renderizado com o filtro | safe nos relatórios.
"""
import bleach

# Tags permitidas - suficiente para os relatórios HTML gerados pela IA
ALLOWED_TAGS = [
    'p', 'br', 'strong', 'b', 'em', 'i', 'u', 'ul', 'ol', 'li',
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'div', 'span', 'table', 'thead', 'tbody', 'tr', 'th', 'td',
    'a', 'blockquote', 'code', 'pre', 'hr', 'small', 'sub', 'sup',
    'img', 'figure', 'figcaption'
]

ALLOWED_ATTRS = {
    'a': ['href', 'title', 'target', 'rel'],
    'img': ['src', 'alt', 'title', 'width', 'height', 'style'],
    'div': ['class', 'style'],
    'span': ['class', 'style'],
    'p': ['class', 'style'],
    'table': ['class', 'border', 'style'],
    'td': ['class', 'style', 'colspan', 'rowspan'],
    'th': ['class', 'style', 'colspan', 'rowspan'],
    'h1': ['class'], 'h2': ['class'], 'h3': ['class'], 'h4': ['class'],
    'ul': ['class'], 'ol': ['class'], 'li': ['class'],
    'code': ['class'], 'pre': ['class'],
}


def sanitizar_html(texto):
    """
    Remove scripts, event handlers (onclick etc.), javascript: e outras
    construções perigosas do HTML. O protocolo 'data' é permitido para
    imagens base64 (gráficos dos relatórios).
    """
    if not texto:
        return texto
    return bleach.clean(
        texto,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRS,
        protocols=['http', 'https', 'mailto', 'data'],
        strip=True
    )

