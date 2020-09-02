from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def notification_order_ready(orders_data, *args, **kwargs):
    theme = f'Заказ: №{orders_data.id} готов к выдаче'
    receiver = orders_data.client_email
    message = render_to_string('message/order_notification.html',
                               {
                                   'name': orders_data.client_name,
                                   'surname': orders_data.client_surname,
                                   'updated': orders_data.updated
                               })
    try:
        send_mail(subject=theme, recipient_list=[receiver], message=message, from_email=settings.DEFAULT_FROM_EMAIL,
                  html_message=message)
    except Exception as error:
        # Можно написать модель писем, и туда складывать ошибки
        print(f'{type(error).__name__} - {list(error.args)}')
        pass
