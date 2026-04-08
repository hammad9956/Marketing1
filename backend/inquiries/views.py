import json
import logging
import threading
import urllib.error
import urllib.request

from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Inquiry

logger = logging.getLogger(__name__)

MAX_MESSAGE = 8000


def _resend_is_configured() -> bool:
    return bool(
        (getattr(settings, "RESEND_API_KEY", "") or "").strip()
        and (getattr(settings, "RESEND_FROM_EMAIL", "") or "").strip()
    )


def _send_resend_email(
    *,
    to_email: str,
    subject: str,
    text_body: str,
    reply_to: str | None = None,
) -> None:
    payload: dict[str, object] = {
        "from": settings.RESEND_FROM_EMAIL,
        "to": [to_email],
        "subject": subject,
        "text": text_body,
    }
    if reply_to:
        payload["reply_to"] = reply_to

    req = urllib.request.Request(
        "https://api.resend.com/emails",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            status = getattr(res, "status", 200)
            if int(status) >= 300:
                raise RuntimeError(f"Resend returned status {status}")
    except urllib.error.HTTPError as exc:
        body = ""
        try:
            body = exc.read().decode("utf-8", errors="ignore")[:500]
        except Exception:
            pass
        raise RuntimeError(f"Resend HTTP {exc.code}: {body}") from exc
    except Exception as exc:
        raise RuntimeError(f"Resend request failed: {exc}") from exc


def _send_confirmation_email(inquiry: Inquiry) -> None:
    """Best-effort confirmation email to the visitor."""
    try:
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
        if _resend_is_configured():
            _send_resend_email(
                to_email=inquiry.email,
                subject=confirm_subject,
                text_body=confirm_body,
            )
        else:
            send_mail(
                confirm_subject,
                confirm_body,
                settings.DEFAULT_FROM_EMAIL,
                [inquiry.email],
                fail_silently=False,
            )
    except Exception:
        logger.exception(
            "Confirmation email failed for inquiry id=%s", inquiry.id
        )


@require_http_methods(["GET", "HEAD"])
def health(request):
    """Lightweight probe for Railway / load balancers (no DB hit)."""
    if request.method == "HEAD":
        return HttpResponse()
    return JsonResponse({"ok": True})


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

    recipient = settings.CONTACT_RECIPIENT_EMAIL
    has_resend = _resend_is_configured()
    has_smtp = bool(settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD)
    if not recipient or (not has_resend and not has_smtp):
        logger.warning(
            "Email not configured. Set CONTACT_RECIPIENT_EMAIL plus either "
            "RESEND_API_KEY/RESEND_FROM_EMAIL or SMTP settings."
        )
        return JsonResponse(
            {
                "ok": False,
                "error": "Email is not configured on the server yet. Please contact support directly.",
            },
            status=503,
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
    try:
        # Send team email in-request for reliability.
        if has_resend:
            _send_resend_email(
                to_email=recipient,
                subject=subject,
                text_body=body,
                reply_to=inquiry.email,
            )
        else:
            internal = EmailMessage(
                subject=subject,
                body=body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient],
                reply_to=[inquiry.email],
            )
            internal.send(fail_silently=False)
    except Exception:
        logger.exception("Team inquiry email failed for inquiry id=%s", inquiry.id)
        return JsonResponse(
            {
                "ok": False,
                "error": "We could not send your message right now. Please try again shortly.",
            },
            status=502,
        )

    # Best-effort visitor confirmation in background so response stays fast.
    visitor_email = inquiry.email.strip().lower()
    team_inbox = recipient.strip().lower()
    if visitor_email != team_inbox:
        threading.Thread(
            target=_send_confirmation_email,
            args=(inquiry,),
            daemon=False,
        ).start()

    return JsonResponse({"ok": True, "id": inquiry.id})
