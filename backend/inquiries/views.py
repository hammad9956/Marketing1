import json
import logging

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Inquiry

logger = logging.getLogger(__name__)

MAX_MESSAGE = 8000


@csrf_exempt
@require_http_methods(["POST", "OPTIONS"])
def contact_submit(request):
    if request.method == "OPTIONS":
        return JsonResponse({})

    try:
        data = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid JSON."}, status=400)

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    company = (data.get("company") or "").strip()[:200]
    phone = (data.get("phone") or "").strip()[:50]
    service = (data.get("service") or "").strip()[:120]
    message = (data.get("message") or "").strip()

    if not name or not email or not message:
        return JsonResponse(
            {"ok": False, "error": "Name, email, and message are required."},
            status=400,
        )

    if len(message) > MAX_MESSAGE:
        return JsonResponse(
            {"ok": False, "error": f"Message must be under {MAX_MESSAGE} characters."},
            status=400,
        )

    inquiry = Inquiry.objects.create(
        name=name[:200],
        email=email[:254],
        company=company,
        phone=phone,
        service=service,
        message=message,
    )

    subject = f"[Helix Prime] Inquiry from {name}"
    body = (
        f"Name: {inquiry.name}\n"
        f"Email: {inquiry.email}\n"
        f"Company: {inquiry.company or '—'}\n"
        f"Phone: {inquiry.phone or '—'}\n"
        f"Service interest: {inquiry.service or '—'}\n\n"
        f"Message:\n{inquiry.message}\n"
    )
    recipient = settings.CONTACT_RECIPIENT_EMAIL
    visitor_email = inquiry.email.strip().lower()
    team_inbox = recipient.strip().lower()

    if settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD:
        try:
            # Team notification — Reply-To so you can hit “Reply” and reach the visitor.
            internal = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient],
                reply_to=[inquiry.email],
            )
            internal.send(fail_silently=False)

            # Confirmation to the person who submitted (skip if same inbox as team to avoid duplicate).
            if visitor_email != team_inbox:
                confirm_subject = "We received your message — Helix Prime Solutions"
                confirm_body = (
                    f"Hi {inquiry.name},\n\n"
                    "Thank you for contacting Helix Prime Solutions. "
                    "We have received your inquiry and will get back to you shortly.\n\n"
                    "A copy of your message is below for your records.\n\n"
                    "—\n"
                    f"{inquiry.message}\n"
                    "—\n\n"
                    "Best regards,\n"
                    "Helix Prime Solutions\n"
                )
                try:
                    send_mail(
                        confirm_subject,
                        confirm_body,
                        settings.DEFAULT_FROM_EMAIL,
                        [inquiry.email],
                        fail_silently=False,
                    )
                except Exception:
                    logger.exception(
                        "Confirmation email to %s failed (inquiry saved; team email was sent)",
                        inquiry.email,
                    )
        except Exception as exc:
            logger.exception("Failed to send inquiry email")
            err_payload = {
                "ok": False,
                "error": "We could not send your message. Please try again or email us directly.",
            }
            # Helps debug Gmail app password, TLS/SSL, and .env loading (only when DEBUG).
            if settings.DEBUG:
                err_payload["smtp_error"] = str(exc)[:800]
            return JsonResponse(err_payload, status=500)
    else:
        logger.warning(
            "EMAIL_HOST_USER/PASSWORD not set — inquiry saved but no email sent."
        )

    return JsonResponse({"ok": True, "id": inquiry.id})
