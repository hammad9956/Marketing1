"""
Populate SQLite with professional Helix Prime Solutions CMS content.

- Default: only fills empty tables (safe for new installs).
- --reset-professional --yes: removes CMS marketing rows (hero, about, home blocks,
  services, blog posts, social links) and recreates professional defaults.
  Does NOT delete Projects or Inquiries.
"""

from django.core.management.base import BaseCommand

from cms.models import (
    AboutSettings,
    BlogPost,
    HeroSettings,
    HomePillar,
    HomeShowcase,
    HomeStat,
    HomeTestimonial,
    Service,
    SocialLink,
)


def _create_professional_content() -> list[str]:
    """Insert full professional dataset. Caller must ensure tables are empty or reset."""
    notes: list[str] = []

    HeroSettings.objects.create(
        eyebrow="USA-market software & growth partner",
        headline="Dominate Your Market. Explode Your Revenue.",
        subheadline=(
            "Websites, SEO, apps, automation, and elite remote teams-built for US revenue "
            "growth, not vanity metrics. Senior-led delivery, transparent reporting, and "
            "shipping cycles you can plan around."
        ),
        cta_primary_label="Book a Strategy Session",
        cta_primary_link="/contact",
        cta_secondary_label="Explore services",
        cta_secondary_link="/services",
    )
    notes.append("Home - Hero")

    AboutSettings.objects.create(
        hero_title="We Don't Do Average. We Deliver Dominance.",
        hero_subtitle=(
            "Helix Prime Solutions pairs sharp US-market strategy with disciplined "
            "engineering-so ambitious teams get speed, quality, and outcomes tied to pipeline "
            "and profit."
        ),
        intro=(
            "We work with founders, growth leaders, and operators who are done with opaque "
            "agencies and shelf-ware deliverables. Every engagement is structured around "
            "clear goals, acceptance criteria, and metrics you already track.\n\n"
            "Whether you need a high-converting site, a product launch, SEO that compounds, "
            "or a senior pod embedded with your team, we align on the shortest path from "
            "today's constraints to tomorrow's revenue."
        ),
        mission_title="Our mission",
        mission_body=(
            "Give every client a measurable digital advantage: faster launches, higher "
            "conversion, lower operational drag, and reporting you can trust. Enterprise-grade "
            "rigor with the urgency of a team that treats your runway as our own."
        ),
    )
    notes.append("About page")

    HomeStat.objects.bulk_create(
        [
            HomeStat(
                value="150+",
                label="Engagements across web, product, and automation",
                order=0,
            ),
            HomeStat(
                value="98%",
                label="Clients who renew or expand their engagement",
                order=1,
            ),
            HomeStat(
                value="24h",
                label="Target response for qualified inquiries",
                order=2,
            ),
            HomeStat(
                value="US",
                label="Timezone-friendly collaboration as standard",
                order=3,
            ),
        ]
    )
    notes.append("Home - Stats")

    HomePillar.objects.bulk_create(
        [
            HomePillar(
                title="Revenue-first delivery",
                body=(
                    "Scope, milestones, and reporting map to leads, revenue, and efficiency-not "
                    "just tickets closed. You always know what shipped and why it mattered."
                ),
                order=0,
            ),
            HomePillar(
                title="US-market clarity",
                body=(
                    "We speak plain English, respect US business hours, and design for buyers, "
                    "compliance, and operations the way US teams actually run."
                ),
                order=1,
            ),
            HomePillar(
                title="End-to-end capability",
                body=(
                    "One partner for web, apps, SEO, automation, and staff augmentation-so you "
                    "stop coordinating five vendors and start compounding results."
                ),
                order=2,
            ),
        ]
    )
    notes.append("Home - Pillar cards")

    HomeShowcase.objects.bulk_create(
        [
            HomeShowcase(
                title="Strategy and engineering, one accountable team",
                body=(
                    "Discovery is not a workshop deck-it is a prioritized roadmap with trade-offs, "
                    "timeline, and success metrics. Engineering follows the same thread: clean "
                    "architecture, performance budgets, and instrumentation so marketing and "
                    "product can iterate with confidence.\n\n"
                    "Upload a supporting image in Admin for this block when ready."
                ),
                order=0,
                image_on_right=False,
            ),
            HomeShowcase(
                title="Operate with the discipline your P&L deserves",
                body=(
                    "We treat accessibility, security basics, and observability as part of "
                    "launch-not post-launch debt. That means fewer surprises in production, "
                    "cleaner handoffs to your internal team, and partners who can defend the "
                    "work in front of stakeholders.\n\n"
                    'Toggle \"image on right\" or add imagery from Admin to match your brand.'
                ),
                order=1,
                image_on_right=True,
            ),
        ]
    )
    notes.append("Home - Showcase blocks")

    HomeTestimonial.objects.bulk_create(
        [
            HomeTestimonial(
                client_name="Sarah M.",
                role_title="Founder & CEO, B2B SaaS (United States)",
                quote=(
                    "They reframed our entire acquisition funnel-not just the website. Within "
                    "one quarter we had clearer messaging, faster pages, and a lead flow we "
                    "could finally measure."
                ),
                stars=5,
                is_published=True,
                order=0,
            ),
            HomeTestimonial(
                client_name="Michael C.",
                role_title="VP Engineering, Fintech (New York)",
                quote=(
                    "We needed senior engineers who could own features without a six-month "
                    "hiring cycle. Helix embedded quickly, shipped production code, and "
                    "documented everything for our internal team."
                ),
                stars=5,
                is_published=True,
                order=1,
            ),
            HomeTestimonial(
                client_name="Jessica R.",
                role_title="Director of Operations, E-commerce (California)",
                quote=(
                    "Automation was sold to us as a buzzword; they delivered real hours back to "
                    "the team and fewer errors in fulfillment. Communication was crisp the "
                    "whole way."
                ),
                stars=5,
                is_published=True,
                order=2,
            ),
        ]
    )
    notes.append("Home - Testimonials")

    services_data = [
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
    for s in services_data:
        Service.objects.create(**s)
    notes.append("Services")

    BlogPost.objects.bulk_create(
        [
            BlogPost(
                title="Choosing a revenue-first digital partner (what US teams should ask)",
                slug="revenue-first-digital-partner",
                description=(
                    "The questions that separate vendors who ship tickets from partners who "
                    "ship outcomes-aligned to pipeline, speed, and accountability."
                ),
                bullets=(
                    "How scope maps to measurable KPIs\n"
                    "What 'done' means for your buyers, not only your backlog\n"
                    "How reporting connects to CRM and revenue"
                ),
                body=(
                    "Most RFPs optimize for hourly rate or technology buzzwords. Stronger "
                    "engagements start with how a partner ties milestones to acquisition, "
                    "conversion, retention, or cost-to-serve.\n\n"
                    "Ask for examples of instrumentation, release cadence, and how they "
                    "handle production incidents. Ask who owns communication and how often "
                    "executives see progress without a status theater meeting.\n\n"
                    "Replace this article with your own thought leadership anytime in Admin."
                ),
                is_published=True,
                order=0,
            ),
            BlogPost(
                title="Technical SEO and conversion: why they fail when treated separately",
                slug="seo-and-conversion-together",
                description=(
                    "Search traffic without a fast, trustworthy page experience leaks "
                    "revenue. Here is how we align technical SEO with CRO fundamentals."
                ),
                bullets=(
                    "Core Web Vitals and trust signals\n"
                    "Landing page clarity for commercial intent\n"
                    "Measurement that attributes to leads, not only sessions"
                ),
                body=(
                    "Ranking without speed and clarity still loses to competitors who load "
                    "faster and answer the buyer's question in the first screen.\n\n"
                    "We combine crawl fixes, structured data, and template-level UX so organic "
                    "visitors hit pages built to convert-not generic blog shells.\n\n"
                    "Edit or extend this post from Django Admin when you are ready."
                ),
                is_published=True,
                order=1,
            ),
        ]
    )
    notes.append("Blog posts")

    SocialLink.objects.bulk_create(
        [
            SocialLink(
                platform=SocialLink.Platform.LINKEDIN,
                url="https://www.linkedin.com/company/helix-prime-solutions",
                order=0,
            ),
            SocialLink(
                platform=SocialLink.Platform.X,
                url="https://x.com/helixprimesolutions",
                order=1,
            ),
            SocialLink(
                platform=SocialLink.Platform.FACEBOOK,
                url="https://www.facebook.com/helixprimesolutions",
                order=2,
            ),
            SocialLink(
                platform=SocialLink.Platform.GITHUB,
                url="https://github.com/helix-prime-solutions",
                order=3,
            ),
            SocialLink(
                platform=SocialLink.Platform.INSTAGRAM,
                url="https://www.instagram.com/helixprimesolutions",
                order=4,
            ),
            SocialLink(
                platform=SocialLink.Platform.WHATSAPP,
                url="https://wa.me/15551234567",
                label="WhatsApp",
                order=5,
            ),
        ]
    )
    notes.append("Social links")

    return notes


class Command(BaseCommand):
    help = (
        "Seed CMS with professional Helix Prime content. "
        "Use --reset-professional --yes to replace existing marketing data (keeps Projects)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-professional",
            action="store_true",
            help="Delete CMS marketing rows and recreate professional defaults.",
        )
        parser.add_argument(
            "--yes",
            action="store_true",
            help="Required with --reset-professional (confirmation).",
        )

    def handle(self, *args, **options):
        reset = options["reset_professional"]
        confirmed = options["yes"]

        if reset and not confirmed:
            self.stderr.write(
                self.style.ERROR(
                    "Refusing to reset without --yes. "
                    "Run: python manage.py seed_cms --reset-professional --yes"
                )
            )
            return

        if reset:
            self.stdout.write(
                self.style.WARNING(
                    "Removing CMS marketing content (Hero, About, home blocks, services, "
                    "blogs, social). Projects and Inquiries are NOT deleted."
                )
            )
            SocialLink.objects.all().delete()
            BlogPost.objects.all().delete()
            Service.objects.all().delete()
            HomeTestimonial.objects.all().delete()
            HomeShowcase.objects.all().delete()
            HomePillar.objects.all().delete()
            HomeStat.objects.all().delete()
            HeroSettings.objects.all().delete()
            AboutSettings.objects.all().delete()

            notes = _create_professional_content()
            self.stdout.write(
                self.style.SUCCESS(
                    "Replaced with professional content: " + ", ".join(notes) + "."
                )
            )
            self.stdout.write(
                "Open http://127.0.0.1:8000/admin/ (CMS section) to review and upload images."
            )
            return

        notes: list[str] = []

        if not HeroSettings.objects.exists():
            HeroSettings.objects.create(
                eyebrow="USA-market software & growth partner",
                headline="Dominate Your Market. Explode Your Revenue.",
                subheadline=(
                    "Websites, SEO, apps, automation, and elite remote teams-built for US revenue "
                    "growth, not vanity metrics. Senior-led delivery, transparent reporting, and "
                    "shipping cycles you can plan around."
                ),
                cta_primary_label="Book a Strategy Session",
                cta_primary_link="/contact",
                cta_secondary_label="Explore services",
                cta_secondary_link="/services",
            )
            notes.append("Home - Hero")

        if not AboutSettings.objects.exists():
            AboutSettings.objects.create(
                hero_title="We Don't Do Average. We Deliver Dominance.",
                hero_subtitle=(
                    "Helix Prime Solutions pairs sharp US-market strategy with disciplined "
                    "engineering-so ambitious teams get speed, quality, and outcomes tied to "
                    "pipeline and profit."
                ),
                intro=(
                    "We work with founders, growth leaders, and operators who are done with "
                    "opaque agencies and shelf-ware deliverables. Every engagement is structured "
                    "around clear goals, acceptance criteria, and metrics you already track.\n\n"
                    "Whether you need a high-converting site, a product launch, SEO that "
                    "compounds, or a senior pod embedded with your team, we align on the shortest "
                    "path from today's constraints to tomorrow's revenue."
                ),
                mission_title="Our mission",
                mission_body=(
                    "Give every client a measurable digital advantage: faster launches, higher "
                    "conversion, lower operational drag, and reporting you can trust. "
                    "Enterprise-grade rigor with the urgency of a team that treats your runway "
                    "as our own."
                ),
            )
            notes.append("About page")

        if not HomeStat.objects.exists():
            HomeStat.objects.bulk_create(
                [
                    HomeStat(
                        value="150+",
                        label="Engagements across web, product, and automation",
                        order=0,
                    ),
                    HomeStat(
                        value="98%",
                        label="Clients who renew or expand their engagement",
                        order=1,
                    ),
                    HomeStat(
                        value="24h",
                        label="Target response for qualified inquiries",
                        order=2,
                    ),
                    HomeStat(
                        value="US",
                        label="Timezone-friendly collaboration as standard",
                        order=3,
                    ),
                ]
            )
            notes.append("Home - Stats")

        if not HomePillar.objects.exists():
            HomePillar.objects.bulk_create(
                [
                    HomePillar(
                        title="Revenue-first delivery",
                        body=(
                            "Scope, milestones, and reporting map to leads, revenue, and "
                            "efficiency-not just tickets closed. You always know what shipped "
                            "and why it mattered."
                        ),
                        order=0,
                    ),
                    HomePillar(
                        title="US-market clarity",
                        body=(
                            "We speak plain English, respect US business hours, and design for "
                            "buyers, compliance, and operations the way US teams actually run."
                        ),
                        order=1,
                    ),
                    HomePillar(
                        title="End-to-end capability",
                        body=(
                            "One partner for web, apps, SEO, automation, and staff augmentation-"
                            "so you stop coordinating five vendors and start compounding results."
                        ),
                        order=2,
                    ),
                ]
            )
            notes.append("Home - Pillar cards")

        if not HomeShowcase.objects.exists():
            HomeShowcase.objects.bulk_create(
                [
                    HomeShowcase(
                        title="Strategy and engineering, one accountable team",
                        body=(
                            "Discovery is not a workshop deck-it is a prioritized roadmap with "
                            "trade-offs, timeline, and success metrics. Engineering follows the "
                            "same thread: clean architecture, performance budgets, and "
                            "instrumentation so marketing and product can iterate with "
                            "confidence.\n\n"
                            "Upload a supporting image in Admin for this block when ready."
                        ),
                        order=0,
                        image_on_right=False,
                    ),
                    HomeShowcase(
                        title="Operate with the discipline your P&L deserves",
                        body=(
                            "We treat accessibility, security basics, and observability as part "
                            "of launch-not post-launch debt. That means fewer surprises in "
                            "production, cleaner handoffs to your internal team, and partners who "
                            "can defend the work in front of stakeholders.\n\n"
                            "Toggle image position or add imagery from Admin to match your brand."
                        ),
                        order=1,
                        image_on_right=True,
                    ),
                ]
            )
            notes.append("Home - Showcase blocks")

        if not HomeTestimonial.objects.exists():
            HomeTestimonial.objects.bulk_create(
                [
                    HomeTestimonial(
                        client_name="Sarah M.",
                        role_title="Founder & CEO, B2B SaaS (United States)",
                        quote=(
                            "They reframed our entire acquisition funnel-not just the website. "
                            "Within one quarter we had clearer messaging, faster pages, and a "
                            "lead flow we could finally measure."
                        ),
                        stars=5,
                        is_published=True,
                        order=0,
                    ),
                    HomeTestimonial(
                        client_name="Michael C.",
                        role_title="VP Engineering, Fintech (New York)",
                        quote=(
                            "We needed senior engineers who could own features without a six-"
                            "month hiring cycle. Helix embedded quickly, shipped production code, "
                            "and documented everything for our internal team."
                        ),
                        stars=5,
                        is_published=True,
                        order=1,
                    ),
                    HomeTestimonial(
                        client_name="Jessica R.",
                        role_title="Director of Operations, E-commerce (California)",
                        quote=(
                            "Automation was sold to us as a buzzword; they delivered real hours "
                            "back to the team and fewer errors in fulfillment. Communication was "
                            "crisp the whole way."
                        ),
                        stars=5,
                        is_published=True,
                        order=2,
                    ),
                ]
            )
            notes.append("Home - Testimonials")

        if not Service.objects.exists():
            for s in [
                {
                    "title": "Website development",
                    "slug": "web",
                    "summary": (
                        "High-performance websites engineered for conversion, Core Web Vitals, "
                        "and a CMS your team can run without filing a ticket for every edit."
                    ),
                    "detail": (
                        "We design and build modern frontends on stacks that scale-typically "
                        "Next.js or equivalent-with structured content, analytics hooks, and "
                        "patterns your team can extend.\n\n"
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
                        "Technical SEO, content structure, and measurement so organic traffic "
                        "turns into qualified pipeline-not vanity rankings."
                    ),
                    "detail": (
                        "We start with audits, crawl hygiene, and indexation reality checks-then "
                        "align content and internal linking with how your buyers actually "
                        "search.\n\n"
                        "Reporting ties to conversions and assisted revenue where possible, not "
                        "only traffic graphs."
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
                        "Mobile and web applications built for reliability, security, and "
                        "iteration-from first release through ongoing product work."
                    ),
                    "detail": (
                        "We scope MVPs that still convert, define API contracts early, and ship "
                        "with logging and error tracking so issues surface before customers "
                        "do.\n\n"
                        "Engagements can include staff augmentation, dedicated squads, or full "
                        "build-own-operate depending on your stage."
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
                        "We align channels to your GTM motion: thought leadership, demand gen, "
                        "or community-whichever actually fits your ICP.\n\n"
                        "Creative, copy, and reporting roll up to the same KPIs your leadership "
                        "cares about."
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
                        "Workflow automation and integrations that remove manual work, reduce "
                        "errors, and connect CRM, support, and operations honestly."
                    ),
                    "detail": (
                        "We map processes with stakeholders, implement idempotent integrations, "
                        "and add monitoring so failures are visible before they hit "
                        "customers.\n\n"
                        "Tooling ranges from no-code bridges to custom services when "
                        "off-the-shelf breaks down."
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
                        "We match skills to your stack and stage, set expectations on "
                        "availability and communication, and run short trial milestones before "
                        "long commitments.\n\n"
                        "Ideal when hiring is too slow but delivery cannot wait."
                    ),
                    "bullets": (
                        "Vetted senior engineers and leads\n"
                        "Overlap with US business hours\n"
                        "Knowledge transfer as part of the engagement"
                    ),
                    "order": 5,
                },
            ]:
                Service.objects.create(**s)
            notes.append("Services")

        if not BlogPost.objects.exists():
            BlogPost.objects.bulk_create(
                [
                    BlogPost(
                        title="Choosing a revenue-first digital partner (what US teams should ask)",
                        slug="revenue-first-digital-partner",
                        description=(
                            "The questions that separate vendors who ship tickets from partners "
                            "who ship outcomes-aligned to pipeline, speed, and accountability."
                        ),
                        bullets=(
                            "How scope maps to measurable KPIs\n"
                            "What 'done' means for your buyers, not only your backlog\n"
                            "How reporting connects to CRM and revenue"
                        ),
                        body=(
                            "Most RFPs optimize for hourly rate or technology buzzwords. Stronger "
                            "engagements start with how a partner ties milestones to acquisition, "
                            "conversion, retention, or cost-to-serve.\n\n"
                            "Ask for examples of instrumentation, release cadence, and how they "
                            "handle production incidents. Ask who owns communication and how "
                            "often executives see progress without a status theater meeting.\n\n"
                            "Replace this article with your own thought leadership anytime in Admin."
                        ),
                        is_published=True,
                        order=0,
                    ),
                    BlogPost(
                        title="Technical SEO and conversion: why they fail when treated separately",
                        slug="seo-and-conversion-together",
                        description=(
                            "Search traffic without a fast, trustworthy page experience leaks "
                            "revenue. Here is how we align technical SEO with CRO fundamentals."
                        ),
                        bullets=(
                            "Core Web Vitals and trust signals\n"
                            "Landing page clarity for commercial intent\n"
                            "Measurement that attributes to leads, not only sessions"
                        ),
                        body=(
                            "Ranking without speed and clarity still loses to competitors who "
                            "load faster and answer the buyer's question in the first screen.\n\n"
                            "We combine crawl fixes, structured data, and template-level UX so "
                            "organic visitors hit pages built to convert-not generic blog "
                            "shells.\n\n"
                            "Edit or extend this post from Django Admin when you are ready."
                        ),
                        is_published=True,
                        order=1,
                    ),
                ]
            )
            notes.append("Blog posts")

        if not SocialLink.objects.exists():
            SocialLink.objects.bulk_create(
                [
                    SocialLink(
                        platform=SocialLink.Platform.LINKEDIN,
                        url="https://www.linkedin.com/company/helix-prime-solutions",
                        order=0,
                    ),
                    SocialLink(
                        platform=SocialLink.Platform.X,
                        url="https://x.com/helixprimesolutions",
                        order=1,
                    ),
                    SocialLink(
                        platform=SocialLink.Platform.FACEBOOK,
                        url="https://www.facebook.com/helixprimesolutions",
                        order=2,
                    ),
                    SocialLink(
                        platform=SocialLink.Platform.GITHUB,
                        url="https://github.com/helix-prime-solutions",
                        order=3,
                    ),
                    SocialLink(
                        platform=SocialLink.Platform.INSTAGRAM,
                        url="https://www.instagram.com/helixprimesolutions",
                        order=4,
                    ),
                    SocialLink(
                        platform=SocialLink.Platform.WHATSAPP,
                        url="https://wa.me/15551234567",
                        label="WhatsApp",
                        order=5,
                    ),
                ]
            )
            notes.append("Social links")

        if notes:
            self.stdout.write(
                self.style.SUCCESS("Created: " + ", ".join(notes) + ".")
            )
            self.stdout.write(
                "Open http://127.0.0.1:8000/admin/ (CMS section). "
                "To replace ALL marketing copy with this professional set, run:\n"
                "  python manage.py seed_cms --reset-professional --yes"
            )
        else:
            self.stdout.write(
                self.style.WARNING(
                    "Nothing to seed - CMS already has data. "
                    "Use --reset-professional --yes to replace marketing content, "
                    "or edit rows in admin."
                )
            )
