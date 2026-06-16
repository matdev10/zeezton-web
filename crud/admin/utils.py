# =========================
# UTILIDADES
# =========================

def dinero(valor):
    try:
        return f"${valor:,.0f}".replace(",", ".")
    except Exception:
        return "$0"

