import unicodedata


def quitar_tildes(texto):
    if not texto:
        return ""

    return "".join(
        c for c in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(c)
    )