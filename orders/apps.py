from django.apps import AppConfig



class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self) -> None:
        import orders.signals
        from .utils import payment_done_singal, items_ordered_singal
        from .signals import send_order_confirmation_to_customer, send_order_confirmation_to_vendors
        
        payment_done_singal.connect(send_order_confirmation_to_customer, dispatch_uid='send_confirmation_to_customer')
        items_ordered_singal.connect(send_order_confirmation_to_vendors, dispatch_uid='send_confirmation_to_vendor')

        return super().ready()
