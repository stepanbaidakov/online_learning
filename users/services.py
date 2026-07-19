import os

from django.urls import reverse_lazy

from rest_framework.response import Response
from stripe import StripeClient

from materials.models import Course

from .models import Payment


def create_checkout_session(request, *args, **kwargs):
    course = Course.objects.get(pk=kwargs.get("pk"))
    api_key = os.getenv("API_KEY")
    client = StripeClient(api_key)

    product = client.v1.products.create({"name": course.title})
    price = client.v1.prices.create({"product": product.id, "unit_amount": int(course.price * 100), "currency": "usd"})

    session = client.v1.checkout.sessions.create(
        {
            "success_url": f"http://localhost:8000/courses/{course.id}/",
            "line_items": [{"price": price.id, "quantity": 1}],
            "mode": "payment",
        }
    )

    Payment.objects.create(
        user=request.user,
        course=course,
        amount=session.amount_total,
        status="unpaid",
        stripe_session_id=session.id,
    )

    payment_status = reverse_lazy("users:payment-status", kwargs={"session_id": session.id})
    return Response({"checkout_url": session.url, "payment_status_url": payment_status})
