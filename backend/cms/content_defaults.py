"""
Canonical Helix Prime marketing copy.

- Django API views merge these values when a queryset is empty or when optional text
  fields are blank, so a fresh PostgreSQL database still serves the same public content.
- `seed_cms` imports from here so seeded rows match API defaults (single source of truth).
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def coalesce_str(value: str | None, default: str) -> str:
    s = (value or "").strip()
    return s if s else default


def bullet_list_from_text(bullets: str) -> list[str]:
    return [b.strip() for b in (bullets or "").splitlines() if b.strip()]


def detail_paragraphs_from_text(detail: str) -> list[str]:
    raw = (detail or "").strip()
    if not raw:
        return []
    parts = [p.strip() for p in raw.replace("\r\n", "\n").split("\n\n")]
    return [p for p in parts if p]


# ---------------------------------------------------------------------------
# Home — Hero (matches JSON shape except background_image resolved per-request)
# ---------------------------------------------------------------------------

HERO_SEED: dict[str, str] = {
    "eyebrow": "USA-market software & growth partner",
    "headline": "Dominate Your Market. Explode Your Revenue.",
    "subheadline": (
        "Websites, SEO, apps, automation, and elite remote teams-built for US revenue "
        "growth, not vanity metrics. Senior-led delivery, transparent reporting, and "
        "shipping cycles you can plan around."
    ),
    "cta_primary_label": "Book a Strategy Session",
    "cta_primary_link": "/contact",
    "cta_secondary_label": "Explore services",
    "cta_secondary_link": "/services",
}


def hero_merged(hero, media_url_fn) -> dict[str, Any]:
    """Merge DB hero with defaults; blank DB fields fall back to canonical copy."""
    h = HERO_SEED
    if not hero:
        return {
            **h,
            "background_image": None,
        }
    bg = media_url_fn(hero.background_image)
    return {
        "eyebrow": coalesce_str(hero.eyebrow, h["eyebrow"]),
        "headline": coalesce_str(hero.headline, h["headline"]),
        "subheadline": coalesce_str(hero.subheadline, h["subheadline"]),
        "background_image": bg,
        "cta_primary_label": coalesce_str(hero.cta_primary_label, h["cta_primary_label"]),
        "cta_primary_link": coalesce_str(hero.cta_primary_link, h["cta_primary_link"]),
        "cta_secondary_label": coalesce_str(
            hero.cta_secondary_label, h["cta_secondary_label"]
        ),
        "cta_secondary_link": coalesce_str(
            hero.cta_secondary_link, h["cta_secondary_link"]
        ),
    }


# ---------------------------------------------------------------------------
# About page
# ---------------------------------------------------------------------------

ABOUT_SEED: dict[str, str] = {
    "hero_title": "We Don't Do Average. We Deliver Dominance.",
    "hero_subtitle": (
        "Helix Prime Solutions pairs sharp US-market strategy with disciplined "
        "engineering-so ambitious teams get speed, quality, and outcomes tied to pipeline "
        "and profit."
    ),
    "intro": (
        "We work with founders, growth leaders, and operators who are done with opaque "
        "agencies and shelf-ware deliverables. Every engagement is structured around "
        "clear goals, acceptance criteria, and metrics you already track.\n\n"
        "Whether you need a high-converting site, a product launch, SEO that compounds, "
        "or a senior pod embedded with your team, we align on the shortest path from "
        "today's constraints to tomorrow's revenue."
    ),
    "mission_title": "Our mission",
    "mission_body": (
        "Give every client a measurable digital advantage: faster launches, higher "
        "conversion, lower operational drag, and reporting you can trust. Enterprise-grade "
        "rigor with the urgency of a team that treats your runway as our own."
    ),
}


def about_merged(about, media_url_fn) -> dict[str, Any]:
    if not about:
        return {
            **ABOUT_SEED,
            "hero_background_image": None,
            "images": [],
        }
    a = ABOUT_SEED
    return {
        "hero_title": coalesce_str(about.hero_title, a["hero_title"]),
        "hero_subtitle": coalesce_str(about.hero_subtitle, a["hero_subtitle"]),
        "hero_background_image": media_url_fn(about.hero_background_image),
        "intro": coalesce_str(about.intro, a["intro"]),
        "mission_title": coalesce_str(about.mission_title, a["mission_title"]),
        "mission_body": coalesce_str(about.mission_body, a["mission_body"]),
        "images": [
            {
                "image": media_url_fn(img.image),
                "caption": img.caption or "",
            }
            for img in about.images.all()
        ],
    }


# ---------------------------------------------------------------------------
# Home — stats / pillars / showcases / testimonials
# ---------------------------------------------------------------------------

STAT_SEEDS: list[dict[str, Any]] = [
    {
        "value": "150+",
        "label": "Engagements across web, product, and automation",
        "order": 0,
    },
    {
        "value": "98%",
        "label": "Clients who renew or expand their engagement",
        "order": 1,
    },
    {
        "value": "24h",
        "label": "Target response for qualified inquiries",
        "order": 2,
    },
    {
        "value": "US",
        "label": "Timezone-friendly collaboration as standard",
        "order": 3,
    },
]

PILLAR_SEEDS: list[dict[str, Any]] = [
    {
        "title": "Revenue-first delivery",
        "body": (
            "Scope, milestones, and reporting map to leads, revenue, and efficiency-not "
            "just tickets closed. You always know what shipped and why it mattered."
        ),
        "order": 0,
    },
    {
        "title": "US-market clarity",
        "body": (
            "We speak plain English, respect US business hours, and design for buyers, "
            "compliance, and operations the way US teams actually run."
        ),
        "order": 1,
    },
    {
        "title": "End-to-end capability",
        "body": (
            "One partner for web, apps, SEO, automation, and staff augmentation-so you "
            "stop coordinating five vendors and start compounding results."
        ),
        "order": 2,
    },
]

SHOWCASE_SEEDS: list[dict[str, Any]] = []

TESTIMONIAL_SEEDS: list[dict[str, Any]] = [
    {
        "client_name": "Sarah M.",
        "role_title": "Founder & CEO, B2B SaaS (United States)",
        "quote": (
            "They reframed our entire acquisition funnel-not just the website. Within "
            "one quarter we had clearer messaging, faster pages, and a lead flow we "
            "could finally measure."
        ),
        "stars": 5,
        "is_published": True,
        "order": 0,
    },
    {
        "client_name": "Michael C.",
        "role_title": "VP Engineering, Fintech (New York)",
        "quote": (
            "We needed senior engineers who could own features without a six-month "
            "hiring cycle. Helix embedded quickly, shipped production code, and "
            "documented everything for our internal team."
        ),
        "stars": 5,
        "is_published": True,
        "order": 1,
    },
    {
        "client_name": "Jessica R.",
        "role_title": "Director of Operations, E-commerce (California)",
        "quote": (
            "Automation was sold to us as a buzzword; they delivered real hours back to "
            "the team and fewer errors in fulfillment. Communication was crisp the "
            "whole way."
        ),
        "stars": 5,
        "is_published": True,
        "order": 2,
    },
]

# Stable synthetic IDs for default testimonials (no DB row); avoids clashes with low PKs.
_TESTIMONIAL_ID_BASE = 900_000


def testimonials_default_json() -> list[dict[str, Any]]:
    return [
        {
            "id": _TESTIMONIAL_ID_BASE + i,
            "client_name": t["client_name"],
            "role_title": t["role_title"],
            "quote": t["quote"],
            "stars": min(5, max(1, int(t["stars"]))),
        }
        for i, t in enumerate(TESTIMONIAL_SEEDS)
    ]


def stats_json_from_db_or_default(rows) -> list[dict[str, str]]:
    if rows:
        return [{"value": s.value, "label": s.label} for s in rows]
    return [{"value": x["value"], "label": x["label"]} for x in STAT_SEEDS]


def pillars_json_from_db_or_default(rows) -> list[dict[str, str]]:
    if rows:
        return [{"title": p.title, "body": p.body} for p in rows]
    return [{"title": x["title"], "body": x["body"]} for x in PILLAR_SEEDS]


def showcases_json_from_db_or_default(rows, media_url_fn) -> list[dict[str, Any]]:
    if rows:
        return [
            {
                "title": s.title,
                "body": s.body,
                "image": media_url_fn(s.image),
                "image_alt": (s.image_alt or s.title).strip() or s.title,
                "image_on_right": s.image_on_right,
            }
            for s in rows
        ]
    return [
        {
            "title": x["title"],
            "body": x["body"],
            "image": None,
            "image_alt": x["title"],
            "image_on_right": x["image_on_right"],
        }
        for x in SHOWCASE_SEEDS
    ]


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------

SERVICE_SEEDS: list[dict[str, Any]] = [
    {
        "title": "Website development",
        "slug": "web",
        "summary": (
            "High-performance websites engineered for conversion, Core Web Vitals, and "
            "a CMS your team can run without filing a ticket for every edit."
        ),
        "detail": (
            "We design and build modern frontends on stacks that scale-typically Next.js "
            "or equivalent-with structured content, analytics hooks, and patterns your "
            "team can extend.\n\n"
            "Every build includes performance budgets, accessibility checks, and SEO "
            "fundamentals baked in from day one-not bolted on after launch."
        ),
        "bullets": (
            "Next.js and modern front-end stacks\n"
            "Performance, CWV, and technical SEO\n"
            "CMS-ready architecture and handoff documentation"
        ),
        "order": 0,
    },
    {
        "title": "SEO (Search Engine Optimization)",
        "slug": "seo",
        "summary": (
            "Technical SEO, content structure, and measurement so organic traffic turns "
            "into qualified pipeline-not vanity rankings."
        ),
        "detail": (
            "We start with audits, crawl hygiene, and indexation reality checks-then align "
            "content and internal linking with how your buyers actually search.\n\n"
            "Reporting ties to conversions and assisted revenue where possible, not only "
            "traffic graphs."
        ),
        "bullets": (
            "Site audits and prioritized fixes\n"
            "Schema, metadata, and content clusters\n"
            "Analytics and attribution you can trust"
        ),
        "order": 1,
    },
    {
        "title": "App development",
        "slug": "app",
        "summary": (
            "Mobile and web applications built for reliability, security, and iteration-"
            "from first release through ongoing product work."
        ),
        "detail": (
            "We scope MVPs that still convert, define API contracts early, and ship with "
            "logging and error tracking so issues surface before customers do.\n\n"
            "Engagements can include staff augmentation, dedicated squads, or full build-"
            "own-operate depending on your stage."
        ),
        "bullets": (
            "Mobile-first UX and secure APIs\n"
            "CI/CD and release discipline\n"
            "Analytics and product instrumentation"
        ),
        "order": 2,
    },
    {
        "title": "Social media management",
        "slug": "social",
        "summary": (
            "Editorial systems and creative direction that support authority and "
            "distribution-without chasing trends that do not move revenue."
        ),
        "detail": (
            "We align channels to your GTM motion: thought leadership, demand gen, or "
            "community-whichever actually fits your ICP.\n\n"
            "Creative, copy, and reporting roll up to the same KPIs your leadership cares "
            "about."
        ),
        "bullets": (
            "Editorial calendars and brand voice\n"
            "Creative direction and asset production\n"
            "Reporting tied to business outcomes"
        ),
        "order": 3,
    },
    {
        "title": "Automation solutions",
        "slug": "automation",
        "summary": (
            "Workflow automation and integrations that remove manual work, reduce errors, "
            "and connect CRM, support, and operations honestly."
        ),
        "detail": (
            "We map processes with stakeholders, implement idempotent integrations, and add "
            "monitoring so failures are visible before they hit customers.\n\n"
            "Tooling ranges from no-code bridges to custom services when off-the-shelf "
            "breaks down."
        ),
        "bullets": (
            "Process mapping and prioritization\n"
            "Zapier, native APIs, and custom connectors\n"
            "Monitoring, alerts, and runbooks"
        ),
        "order": 4,
    },
    {
        "title": "Staff augmentation",
        "slug": "staff",
        "summary": (
            "Senior developers and specialists who plug into your team with clear "
            "ownership, overlap with your time zone, and documentation that survives "
            "after they roll off."
        ),
        "detail": (
            "We match skills to your stack and stage, set expectations on availability and "
            "communication, and run short trial milestones before long commitments.\n\n"
            "Ideal when hiring is too slow but delivery cannot wait."
        ),
        "bullets": (
            "Vetted senior engineers and leads\n"
            "Overlap with US business hours\n"
            "Knowledge transfer as part of the engagement"
        ),
        "order": 5,
    },
]


def service_dict_from_seed(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": row["title"],
        "slug": row["slug"],
        "summary": row["summary"],
        "bullets": bullet_list_from_text(row["bullets"]),
        "icon_image": None,
        "cover_image": None,
    }


def service_detail_dict_from_seed(row: dict[str, Any]) -> dict[str, Any]:
    d = service_dict_from_seed(row)
    return {
        **d,
        "hero_image": None,
        "body_paragraphs": detail_paragraphs_from_text(row["detail"]),
    }


def default_service_by_slug(slug: str) -> dict[str, Any] | None:
    for row in SERVICE_SEEDS:
        if row["slug"] == slug:
            return row
    return None


# ---------------------------------------------------------------------------
# Blog
# ---------------------------------------------------------------------------

BLOG_POST_SEEDS: list[dict[str, Any]] = [
    {
        "title": "Choosing a revenue-first digital partner (what US teams should ask)",
        "slug": "revenue-first-digital-partner",
        "description": (
            "The questions that separate vendors who ship tickets from partners who "
            "ship outcomes-aligned to pipeline, speed, and accountability."
        ),
        "bullets": (
            "How scope maps to measurable KPIs\n"
            "What 'done' means for your buyers, not only your backlog\n"
            "How reporting connects to CRM and revenue"
        ),
        "body": (
            "Most RFPs optimize for hourly rate or technology buzzwords. Stronger "
            "engagements start with how a partner ties milestones to acquisition, "
            "conversion, retention, or cost-to-serve.\n\n"
            "Ask for examples of instrumentation, release cadence, and how they "
            "handle production incidents. Ask who owns communication and how often "
            "executives see progress without a status theater meeting."
        ),
        "is_published": True,
        "order": 0,
    },
    {
        "title": "Technical SEO and conversion: why they fail when treated separately",
        "slug": "seo-and-conversion-together",
        "description": (
            "Search traffic without a fast, trustworthy page experience leaks "
            "revenue. Here is how we align technical SEO with CRO fundamentals."
        ),
        "bullets": (
            "Core Web Vitals and trust signals\n"
            "Landing page clarity for commercial intent\n"
            "Measurement that attributes to leads, not only sessions"
        ),
        "body": (
            "Ranking without speed and clarity still loses to competitors who load "
            "faster and answer the buyer's question in the first screen.\n\n"
            "We combine crawl fixes, structured data, and template-level UX so organic "
            "visitors hit pages built to convert-not generic blog shells."
        ),
        "is_published": True,
        "order": 1,
    },
]


def blog_card_from_seed(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "title": row["title"],
        "slug": row["slug"],
        "description": row["description"],
        "bullets": bullet_list_from_text(row["bullets"]),
        "cover_image": None,
    }


def blog_detail_from_seed(row: dict[str, Any]) -> dict[str, Any]:
    card = blog_card_from_seed(row)
    return {
        **card,
        "body_paragraphs": detail_paragraphs_from_text(row["body"]),
        "published_at": None,
    }


def default_blog_by_slug(slug: str) -> dict[str, Any] | None:
    for row in BLOG_POST_SEEDS:
        if row["slug"] == slug:
            return row
    return None


def filter_blog_seeds_by_query(q: str) -> list[dict[str, Any]]:
    if not q:
        return list(BLOG_POST_SEEDS)
    q_lower = q.lower()
    return [r for r in BLOG_POST_SEEDS if q_lower in r["title"].lower()]


# ---------------------------------------------------------------------------
# Social links (footer)
# ---------------------------------------------------------------------------

SOCIAL_DEFAULT_API: list[dict[str, str]] = [
    {
        "id": "linkedin",
        "label": "LinkedIn",
        "href": "https://www.linkedin.com/company/helix-prime-solutions",
    },
    {"id": "x", "label": "X (Twitter)", "href": "https://x.com/helixprimesolutions"},
    {
        "id": "facebook",
        "label": "Facebook",
        "href": "https://www.facebook.com/helixprimesolutions",
    },
    {"id": "github", "label": "GitHub", "href": "https://github.com/helix-prime-solutions"},
    {
        "id": "instagram",
        "label": "Instagram",
        "href": "https://www.instagram.com/helixprimesolutions",
    },
    {"id": "whatsapp", "label": "WhatsApp", "href": "https://wa.me/15551234567"},
]

# (platform value, url, label, order) — matches `SocialLink` fields for seeding.
SOCIAL_SEEDS_ORM: list[tuple[str, str, str, int]] = [
    ("linkedin", "https://www.linkedin.com/company/helix-prime-solutions", "", 0),
    ("x", "https://x.com/helixprimesolutions", "", 1),
    ("facebook", "https://www.facebook.com/helixprimesolutions", "", 2),
    ("github", "https://github.com/helix-prime-solutions", "", 3),
    ("instagram", "https://www.instagram.com/helixprimesolutions", "", 4),
    ("whatsapp", "https://wa.me/15551234567", "WhatsApp", 5),
]
