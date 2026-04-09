"""
HTML + plain-text bodies for contact inquiry emails.

All user-supplied strings are escaped for HTML. Plain-text parts mirror structure
for clients that do not render HTML.
"""

from __future__ import annotations

import html
from django.conf import settings

from .models import Inquiry

COMPANY = "Helix Prime Solutions"

# Email-safe colors (avoid relying on external CSS).
_BG_PAGE = "#f1f5f9"
_BG_CARD = "#ffffff"
_BG_HEADER = "#0a1128"
_ACCENT = "#06b6d4"
_TEXT = "#0f172a"
_TEXT_MUTED = "#64748b"
_BORDER = "#e2e8f0"


def _site_url() -> str:
    return str(getattr(settings, "PUBLIC_SITE_URL", "") or "").strip().rstrip("/") or (
        "https://helixprimesolutions.com"
    )


def _e(s: str) -> str:
    return html.escape((s or "").strip(), quote=True)


def _first_name(full_name: str) -> str:
    parts = (full_name or "").strip().split()
    return parts[0] if parts else "there"


def _nl2br(text: str) -> str:
    t = _e(text).replace("\r\n", "\n").replace("\r", "\n")
    return t.replace("\n", "<br>\n")


def _shell(title: str, inner: str) -> str:
    url = _site_url()
    return f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:{_BG_PAGE};">
<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:{_BG_PAGE};">
<tr><td align="center" style="padding:28px 14px;">
<table role="presentation" width="600" cellspacing="0" cellpadding="0" style="max-width:600px;width:100%;background:{_BG_CARD};border-radius:12px;overflow:hidden;border:1px solid {_BORDER};">
<tr><td style="background:{_BG_HEADER};padding:22px 26px;border-bottom:3px solid {_ACCENT};">
<div style="font-family:Georgia,'Times New Roman',serif;font-size:20px;font-weight:700;color:#ffffff;letter-spacing:0.04em;">HELIX PRIME</div>
<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:12px;color:#94a3b8;margin-top:4px;text-transform:uppercase;letter-spacing:0.12em;">Solutions</div>
</td></tr>
<tr><td style="padding:28px 26px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;color:{_TEXT};font-size:15px;line-height:1.55;">
<h1 style="margin:0 0 16px;font-size:20px;font-weight:700;color:{_TEXT};">{title}</h1>
{inner}
</td></tr>
<tr><td style="padding:0 26px 24px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:12px;color:{_TEXT_MUTED};line-height:1.5;border-top:1px solid {_BORDER};">
<p style="margin:16px 0 0;">© {COMPANY}<br>
<a href="{_e(url)}" style="color:{_ACCENT};text-decoration:none;">{_e(url.removeprefix("https://").removeprefix("http://"))}</a></p>
</td></tr>
</table>
</td></tr>
</table>
</body>
</html>"""


def _detail_row(label: str, value: str, *, is_email: bool = False) -> str:
    display = value.strip() if value.strip() else "—"
    if is_email and display != "—":
        cell = f'<a href="mailto:{_e(display)}" style="color:{_ACCENT};text-decoration:none;">{_e(display)}</a>'
    else:
        cell = _e(display)
    return f"""<table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border-bottom:1px solid {_BORDER};">
<tr>
<td style="padding:12px 0;width:38%;vertical-align:top;font-size:13px;color:{_TEXT_MUTED};">{_e(label)}</td>
<td style="padding:12px 0;vertical-align:top;font-size:14px;color:{_TEXT};font-weight:500;">{cell}</td>
</tr>
</table>"""


def build_team_notification(inquiry: Inquiry) -> tuple[str, str]:
    """Return (plain_text, html) for the internal team notification."""
    msg_plain = inquiry.message.strip()
    text = (
        f"New inquiry via {COMPANY} website\n"
        f"{'=' * 48}\n\n"
        f"Name:  {inquiry.name}\n"
        f"Email: {inquiry.email}\n"
        f"Company: {inquiry.company or '—'}\n"
        f"Phone: {inquiry.phone or '—'}\n"
        f"Service interest: {inquiry.service or '—'}\n\n"
        f"What they wrote (message field):\n"
        f"{'-' * 40}\n"
        f"{msg_plain}\n"
        f"{'-' * 40}\n\n"
        f"Reply directly to this email to respond — Reply-To is set to the visitor.\n"
    )
    inner = (
        "<p style=\"margin:0 0 8px;color:#64748b;font-size:14px;\">"
        "Someone submitted the contact form. Reply to this email to reach them "
        "(Reply-To is set to their address).</p>"
        + _detail_row("Name", inquiry.name)
        + _detail_row("Email", inquiry.email, is_email=True)
        + _detail_row("Company", inquiry.company)
        + _detail_row("Phone", inquiry.phone)
        + _detail_row("Service interest", inquiry.service)
        + "<p style=\"margin:20px 0 8px;font-size:13px;font-weight:600;color:#0f172a;text-transform:uppercase;letter-spacing:0.06em;\">Their message</p>"
        + f"<div style=\"margin:0;padding:16px 18px;background:#f8fafc;border-left:4px solid {_ACCENT};border-radius:0 8px 8px 0;font-size:15px;line-height:1.55;color:{_TEXT};\">{_nl2br(inquiry.message)}</div>"
    )
    html_body = _shell("New website inquiry", inner)
    return text, html_body


def build_visitor_confirmation(inquiry: Inquiry) -> tuple[str, str]:
    """Return (plain_text, html) for the auto-reply to the submitter."""
    first = _first_name(inquiry.name)
    msg_plain = inquiry.message.strip()
    text = (
        f"Hi {first},\n\n"
        f"Thank you for contacting {COMPANY}. We received your inquiry and will "
        f"get back to you as soon as we can.\n\n"
        f"Copy of your submission (exactly as entered):\n"
        f"{'-' * 40}\n"
        f"Name:  {inquiry.name}\n"
        f"Email: {inquiry.email}\n"
        f"Company: {inquiry.company or '—'}\n"
        f"Phone: {inquiry.phone or '—'}\n"
        f"Service interest: {inquiry.service or '—'}\n\n"
        f"Project details / message:\n"
        f"{msg_plain}\n"
        f"{'-' * 40}\n\n"
        f"If you need to add or correct anything, reply to this email.\n\n"
        f"Best regards,\n{COMPANY}\n"
        f"{_site_url()}\n"
    )
    inner = (
        f"<p style=\"margin:0 0 16px;\">Hi <strong>{_e(first)}</strong>,</p>"
        f"<p style=\"margin:0 0 16px;\">Thank you for reaching out to <strong>{_e(COMPANY)}</strong>. "
        "We have received your inquiry and will respond as soon as we can.</p>"
        "<p style=\"margin:0 0 12px;color:#64748b;font-size:14px;\">"
        "<strong>Your submission</strong> — here is everything you entered on the form, for your records.</p>"
        + _detail_row("Name", inquiry.name)
        + _detail_row("Email", inquiry.email, is_email=True)
        + _detail_row("Company", inquiry.company)
        + _detail_row("Phone", inquiry.phone)
        + _detail_row("Service interest", inquiry.service)
        + "<p style=\"margin:20px 0 8px;font-size:13px;font-weight:600;color:#0f172a;text-transform:uppercase;letter-spacing:0.06em;\">Project details</p>"
        f"<div style=\"margin:0;padding:16px 18px;background:#f8fafc;border-left:4px solid {_ACCENT};border-radius:0 8px 8px 0;font-size:15px;line-height:1.55;color:{_TEXT};\">{_nl2br(inquiry.message)}</div>"
        "<p style=\"margin:20px 0 0;\">If you would like to add anything, you can reply to this email.</p>"
        f"<p style=\"margin:20px 0 0;\">Best regards,<br><strong>{_e(COMPANY)}</strong></p>"
    )
    html_body = _shell("We received your message", inner)
    return text, html_body
