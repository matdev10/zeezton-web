from ..models import TarifaEnvio


def calcular_costo_envio(metodo_entrega, comuna):
    if metodo_entrega != "DOMICILIO":
        return 0

    if not comuna:
        return 0

    tarifa = TarifaEnvio.objects.filter(
        comuna__iexact=comuna.strip(),
        activo=True
    ).first()

    if tarifa:
        return tarifa.costo

    return 0