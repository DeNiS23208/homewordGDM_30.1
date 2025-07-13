import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_product(name):
    """
    Создаёт продукт в Stripe
    """
    product = stripe.Product.create(name=name)
    return product


def create_stripe_price(product_id, amount):
    """
    Создаёт цену для продукта в Stripe
    """
    price = stripe.Price.create(
        product=product_id,
        unit_amount=amount * 100,  # Stripe принимает цену в копейках
        currency="rub",  # Валюта (можно поменять)
    )
    return price


def create_stripe_session(price_id):
    """
    Создаёт сессию оплаты и возвращает ссылку для оплаты
    """
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
    )
    return session
