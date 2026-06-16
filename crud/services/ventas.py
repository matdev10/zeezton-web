from django.db import transaction

from ..models import (
    Producto,
    Cliente,
    Venta,
    DetalleVenta,
)



def crear_venta_pos(data):
    tipo_documento = data.get("tipo_documento")
    detalles = data.get("detalles", [])
    cliente_data = data.get("cliente", {})

    numero_documento = cliente_data.get("numero_documento")
    nombre_completo = cliente_data.get("nombre_completo")

    if not tipo_documento:
        raise ValueError("Falta tipo_documento")

    tipo_documento = tipo_documento.upper()

    if tipo_documento not in ["BOLETA", "FACTURA"]:
        raise ValueError("Tipo de documento inválido")

    if not detalles:
        raise ValueError("La venta no tiene productos")

    if not numero_documento:
        raise ValueError("Falta numero_documento del cliente")

    if not nombre_completo:
        raise ValueError("Falta nombre_completo del cliente")

    partes_nombre = nombre_completo.strip().split(" ", 1)
    nombre = partes_nombre[0]
    apellido = partes_nombre[1] if len(partes_nombre) > 1 else ""

    with transaction.atomic():

        cliente, creado = Cliente.objects.get_or_create(
            numero_documento=numero_documento,
            defaults={
                "nombre": nombre,
                "apellido": apellido,
            }
        )

        venta = Venta.objects.create(
            cliente=cliente,
            tipo_documento=tipo_documento
        )

        for item in detalles:
            producto_id = item.get("producto_id")
            cantidad = int(item.get("cantidad", 0))

            if not producto_id or cantidad <= 0:
                raise ValueError("Detalle inválido")

            producto = Producto.objects.select_for_update().get(
                id=producto_id
            )

            if producto.stock < cantidad:
                raise ValueError(
                    f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}"
                )

            DetalleVenta.objects.create(
                venta=venta,
                producto=producto,
                cantidad=cantidad,
                precio_unitario=producto.precio
            )

            producto.stock -= cantidad
            producto.save(update_fields=["stock"])

        venta.recalcular_total()

    return venta