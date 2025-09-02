import stripe

from config.settings import PUBLIC_API_KEY_STRIPE

stripe.api_key = PUBLIC_API_KEY_STRIPE

def create_stripe_price_amount(name_product: str, amount: int) -> dict:
    return stripe.Price.create(
        currency="usd",
        unit_amount= amount * 100,
        product_data={"name": name_product}
    )

def create_stripe_session(price: dict) -> tuple:
    session =  stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment"
    )
    return session.get("id"), session.get("url")