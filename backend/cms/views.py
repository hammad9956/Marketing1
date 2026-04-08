from urllib.parse import urlparse

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from . import content_defaults as cd
from .models import (
    AboutSettings,
    BlogPost,
    HeroSettings,
    HomePillar,
    HomeShowcase,
    HomeStat,
    HomeTestimonial,
    Project,
    Service,
    SocialLink,
)


def _rewrite_media_absolute_url(url: str) -> str:
    """
    When the API is called from SSR using an internal hostname, build_absolute_uri() can
    produce http://*.railway.internal/... or http://127.0.0.1:8000/... — browsers cannot
    load those. Rewrite /media/... to DJANGO_PUBLIC_BASE_URL when set.
    """
    base = (getattr(settings, "DJANGO_PUBLIC_BASE_URL", "") or "").strip().rstrip("/")
    if not base or not url:
        return url
    if url.startswith(base):
        return url
    # Cloudinary and other CDNs are already public; do not rewrite.
    if "res.cloudinary.com" in url:
        return url
    try:
        p = urlparse(url)
        if "/media/" not in (p.path or ""):
            return url
    except Exception:
        return url
    bad = (
        "railway.internal",
        "127.0.0.1",
        "localhost",
    )
    if not any(b in url for b in bad):
        return url
    try:
        p = urlparse(url)
        suffix = p.path or ""
        if p.query:
            suffix = f"{suffix}?{p.query}"
        return f"{base}{suffix}"
    except Exception:
        return url


def _media_url(request, filefield):
    if not filefield or not getattr(filefield, "name", None):
        return None
    path = filefield.url
    if path.startswith(("http://", "https://")):
        return _rewrite_media_absolute_url(path)
    # MEDIA_URL may be "media/..." without a leading slash; joining with DJANGO_PUBLIC_BASE_URL
    # must not produce "https://hostmedia/..." (missing slash before /media/).
    if not path.startswith("/"):
        path = "/" + path.lstrip("/")
    base = getattr(settings, "DJANGO_PUBLIC_BASE_URL", "") or ""
    if base:
        return f"{base.rstrip('/')}{path}"
    return _rewrite_media_absolute_url(request.build_absolute_uri(path))


def _service_dict(request, s: Service):
    return {
        "title": s.title,
        "slug": s.slug,
        "summary": s.summary,
        "bullets": s.bullet_list(),
        "icon_image": _media_url(request, s.icon_image),
        "cover_image": _media_url(request, s.cover_image),
    }


def _project_list_dict(request, p: Project):
    return {
        "title": p.title,
        "slug": p.slug,
        "category": p.category,
        "excerpt": p.excerpt,
        "cover_image": _media_url(request, p.cover_image),
    }


@require_GET
def home_payload(request):
    hero_out = cd.hero_merged(HeroSettings.objects.first(), lambda f: _media_url(request, f))
    pillars = cd.pillars_json_from_db_or_default(list(HomePillar.objects.all()))
    showcases = cd.showcases_json_from_db_or_default(
        list(HomeShowcase.objects.all()),
        lambda f: _media_url(request, f),
    )
    stats = cd.stats_json_from_db_or_default(list(HomeStat.objects.all()))
    services = [_service_dict(request, s) for s in Service.objects.all()]

    t_qs = HomeTestimonial.objects.filter(is_published=True)
    if t_qs.exists():
        testimonials = [
            {
                "id": t.id,
                "client_name": t.client_name,
                "role_title": t.role_title,
                "quote": t.quote,
                "stars": min(5, max(1, t.stars)),
            }
            for t in t_qs
        ]
    else:
        testimonials = cd.testimonials_default_json()

    return JsonResponse(
        {
            "hero": hero_out,
            "pillars": pillars,
            "showcases": showcases,
            "stats": stats,
            "services": services,
            "testimonials": testimonials,
        }
    )


@require_GET
def services_list(request):
    data = [_service_dict(request, s) for s in Service.objects.all()]
    return JsonResponse({"services": data})


@require_GET
def service_detail(request, slug: str):
    try:
        s = Service.objects.get(slug=slug)
    except Service.DoesNotExist:
        return JsonResponse({"detail": "Not found."}, status=404)
    return JsonResponse(
        {
            "title": s.title,
            "slug": s.slug,
            "summary": s.summary,
            "bullets": s.bullet_list(),
            "icon_image": _media_url(request, s.icon_image),
            "cover_image": _media_url(request, s.cover_image),
            "hero_image": _media_url(request, s.hero_image),
            "body_paragraphs": s.detail_paragraphs(),
        }
    )


@require_GET
def service_slugs(request):
    slugs = list(Service.objects.values_list("slug", flat=True))
    return JsonResponse({"slugs": slugs})


@require_GET
def projects_list(request):
    qs = Project.objects.filter(is_published=True)
    data = [_project_list_dict(request, p) for p in qs]
    return JsonResponse({"projects": data})


@require_GET
def project_detail(request, slug: str):
    p = get_object_or_404(Project, slug=slug, is_published=True)
    gallery = [
        {
            "image": _media_url(request, g.image),
            "caption": g.caption,
        }
        for g in p.gallery_images.all()
    ]
    return JsonResponse(
        {
            "title": p.title,
            "slug": p.slug,
            "category": p.category,
            "excerpt": p.excerpt,
            "body_paragraphs": p.body_paragraphs(),
            "cover_image": _media_url(request, p.cover_image),
            "hero_image": _media_url(request, p.hero_image),
            "gallery": gallery,
        }
    )


@require_GET
def about_payload(request):
    a = AboutSettings.objects.first()
    return JsonResponse(
        {
            "about": cd.about_merged(
                a, lambda f: _media_url(request, f)
            )
        }
    )


@require_GET
def project_slugs(request):
    slugs = list(
        Project.objects.filter(is_published=True).values_list("slug", flat=True)
    )
    return JsonResponse({"slugs": slugs})


def _blog_card_dict(request, b: BlogPost):
    return {
        "title": b.title,
        "slug": b.slug,
        "description": b.description,
        "bullets": b.bullet_list(),
        "cover_image": _media_url(request, b.cover_image),
    }


@require_GET
def blogs_list(request):
    q = (request.GET.get("q") or "").strip()
    qs = BlogPost.objects.filter(is_published=True)
    if q:
        qs = qs.filter(title__icontains=q)
    qs = qs.order_by("order", "-published_at", "-id")
    data = [_blog_card_dict(request, b) for b in qs]
    return JsonResponse({"posts": data})


@require_GET
def blog_detail(request, slug: str):
    try:
        b = BlogPost.objects.get(slug=slug, is_published=True)
    except BlogPost.DoesNotExist:
        return JsonResponse({"detail": "Not found."}, status=404)
    out = _blog_card_dict(request, b)
    out["body_paragraphs"] = b.body_paragraphs()
    out["published_at"] = b.published_at.isoformat() if b.published_at else None
    return JsonResponse(out)


@require_GET
def blog_slugs(request):
    slugs = list(
        BlogPost.objects.filter(is_published=True).values_list("slug", flat=True)
    )
    return JsonResponse({"slugs": slugs})


@require_GET
def social_links(request):
    items = [
        {
            "id": s.platform,
            "label": (s.label or "").strip() or s.get_platform_display(),
            "href": s.url,
        }
        for s in SocialLink.objects.filter(is_active=True)
    ]
    if not items:
        items = list(cd.SOCIAL_DEFAULT_API)
    return JsonResponse({"social": items})
