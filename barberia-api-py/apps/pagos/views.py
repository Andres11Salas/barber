import mercadopago
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.citas.models import Cita
from .models import Pago


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crear_preferencia_pago(request):
    cita_id = request.data.get('citaId')
    monto = request.data.get('monto')
    descripcion = request.data.get('descripcion', 'Corte de Cabello / Servicio de Barbería')

    if not cita_id or not monto:
        return Response(
            {'error': 'citaId y monto son requeridos'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        cita = Cita.objects.get(id=cita_id)
    except Cita.DoesNotExist:
        return Response(
            {'error': 'La cita no existe'},
            status=status.HTTP_404_NOT_FOUND
        )

    nuevo_pago = Pago.objects.create(cita=cita, monto=monto)

    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)

    preference_data = {
        'items': [
            {
                'id': str(nuevo_pago.id),
                'title': descripcion,
                'quantity': 1,
                'unit_price': float(monto),
            }
        ],
        'back_urls': {
            'success': f'{settings.FRONTEND_URL}/pagos/exito',
            'failure': f'{settings.FRONTEND_URL}/pagos/falla',
            'pending': f'{settings.FRONTEND_URL}/pagos/pendiente',
        },
        'auto_return': 'approved',
        'notification_url': f'{settings.BACKEND_URL}/api/pagos/webhook',
        'external_reference': str(nuevo_pago.id),
    }

    result = sdk.preference().create(preference_data)

    if result['status'] == 201:
        preference = result['response']
        nuevo_pago.preference_id = preference['id']
        nuevo_pago.save()
        return Response({'url_pago': preference['init_point'], 'preference_id': preference['id']})
    else:
        nuevo_pago.estado = 'RECHAZADO'
        nuevo_pago.save()
        return Response(
            {'error': 'Error al crear la preferencia de pago'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def recibir_webhook(request):
    payment_id = request.query_params.get('id') or request.query_params.get('data.id')
    topic = request.query_params.get('topic') or request.query_params.get('type')

    if topic == 'payment' and payment_id:
        sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
        payment_info = sdk.payment().get(payment_id)

        if payment_info['status'] == 200:
            payment_data = payment_info['response']
            external_ref = payment_data.get('external_reference')
            status_pago = payment_data.get('status')

            if external_ref:
                try:
                    pago = Pago.objects.get(id=external_ref)
                    if status_pago == 'approved':
                        pago.estado = 'APROBADO'
                    elif status_pago == 'rejected':
                        pago.estado = 'RECHAZADO'
                    elif status_pago == 'refunded':
                        pago.estado = 'REEMBOLSADO'
                    elif status_pago == 'cancelled':
                        pago.estado = 'RECHAZADO'
                    pago.mercadopago_id = payment_id
                    pago.metodo_pago = payment_data.get('payment_method_id')
                    pago.save()
                except Pago.DoesNotExist:
                    pass

    return Response({'status': 'OK'}, status=status.HTTP_200_OK)