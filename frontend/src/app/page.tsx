import Link from "next/link";
import { AboutHomeSection } from "@/components/AboutHomeSection";
import { BlogPreviewSection } from "@/components/BlogPreviewSection";
import { CmsImage } from "@/components/CmsImage";
import { ContactForm } from "@/components/ContactForm";
import { FinalCtaSection } from "@/components/FinalCtaSection";
import { HomeShowcasesSection } from "@/components/HomeShowcasesSection";
import { ImpactStatsSection } from "@/components/ImpactStatsSection";
import { Reveal } from "@/components/Reveal";
import { StaffAugmentationSection } from "@/components/StaffAugmentationSection";
import { TestimonialsSection } from "@/components/TestimonialsSection";
import { WhyChooseSection } from "@/components/WhyChooseSection";
import { COMPANY, CONTACT_EMAIL, SERVICE_SLUG_ORDER } from "@/lib/constants";
import { fetchAbout, fetchBlogsList, fetchHomeBundle, fetchProjectsList } from "@/lib/cms";

export const revalidate = 60;

export default async function HomePage() {
  const [home, projects, blogPosts, aboutCms] = await Promise.all([
    fetchHomeBundle(),
    fetchProjectsList(),
    fetchBlogsList(),
    fetchAbout(),
  ]);
  const { services, testimonials, hero, stats, showcases } = home;
  const featured = projects.slice(0, 3);
  const envHero = process.env.NEXT_PUBLIC_HERO_BACKGROUND?.trim();
  const heroBackground =
    hero.background_image?.trim() || envHero || null;

  const order = new Map<string, number>(
    SERVICE_SLUG_ORDER.map((slug, i) => [slug, i])
  );
  const orderedServices = [...services].sort(
    (a, b) => (order.get(a.slug) ?? 99) - (order.get(b.slug) ?? 99)
  );

  const heroHeadline = hero.headline?.trim() || COMPANY;
  const heroEyebrow = hero.eyebrow?.trim();
  const heroSub = hero.subheadline?.trim();

  return (
    <>
      <section
        id="top"
        className="relative flex min-h-[90vh] items-center overflow-hidden bg-helix-bg"
      >
        <div className="absolute inset-0">
          {heroBackground ? (
            <CmsImage
              src={heroBackground}
              alt=""
              fill
              className="object-cover"
              sizes="100vw"
              priority
            />
          ) : (
            <div
              className="absolute inset-0 bg-gradient-to-br from-[#0A1128] via-[#0f1629] to-[#06080f]"
              aria-hidden
            />
          )}
          <div
            className="absolute inset-0 bg-gradient-to-b from-black/85 via-black/62 to-black/[0.92]"
            aria-hidden
          />
          <div
            className="absolute inset-0 bg-gradient-to-r from-black/55 via-black/20 to-transparent sm:from-black/50"
            aria-hidden
          />
          <div
            className="absolute inset-0 bg-[radial-gradient(ellipse_80%_55%_at_70%_18%,rgba(0,232,255,0.1),transparent),radial-gradient(ellipse_45%_38%_at_12%_78%,rgba(212,175,55,0.07),transparent)]"
            aria-hidden
          />
        </div>
        <div
          className="pointer-events-none absolute inset-0 bg-grid-fade-dark opacity-[0.2] dark:opacity-[0.25]"
          aria-hidden
        />
        <div className="relative z-10 mx-auto w-full max-w-6xl px-4 pb-20 pt-24 sm:px-6 sm:pb-28 sm:pt-28">
          <div className="max-w-4xl">
            {heroEyebrow ? (
              <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand drop-shadow-sm">
                {heroEyebrow}
              </p>
            ) : null}
            <h1 className="mt-5 max-w-4xl font-display text-4xl font-bold leading-[1.06] tracking-tight text-white drop-shadow-[0_2px_24px_rgba(0,0,0,0.45)] sm:mt-6 sm:text-5xl md:text-6xl lg:text-7xl">
              {heroHeadline}
            </h1>
            {heroSub ? (
              <p className="mt-6 max-w-xl text-lg font-bold leading-snug text-white sm:text-xl [text-shadow:0_1px_2px_rgba(0,0,0,0.95),0_2px_20px_rgba(0,0,0,0.75)]">
                {heroSub}
              </p>
            ) : null}
            <div className="mt-11 flex flex-wrap gap-4">
              {hero.cta_primary_label?.trim() ? (
                <Link
                  href={hero.cta_primary_link?.trim() || "/contact"}
                  className="inline-flex min-h-[3.25rem] items-center justify-center rounded-xl bg-white px-8 py-3.5 text-sm font-bold uppercase tracking-[0.12em] text-helix-heading shadow-[0_8px_32px_rgba(0,0,0,0.35)] transition hover:bg-slate-100 hover:shadow-[0_12px_40px_rgba(0,0,0,0.4)]"
                >
                  {hero.cta_primary_label.trim()}
                </Link>
              ) : null}
              {hero.cta_secondary_label?.trim() ? (
                <Link
                  href={hero.cta_secondary_link?.trim() || "/services"}
                  className="inline-flex min-h-[3.25rem] items-center justify-center rounded-xl border border-white/35 bg-black/25 px-8 py-3.5 text-base font-semibold text-white backdrop-blur-sm transition hover:border-white/50 hover:bg-black/35"
                >
                  {hero.cta_secondary_label.trim()}
                </Link>
              ) : null}
            </div>
          </div>
        </div>
      </section>

      <ImpactStatsSection stats={stats} />

      <HomeShowcasesSection showcases={showcases} />

      <section id="services" className="border-t border-slate-200 py-20 dark:border-helix-border sm:py-28">
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <Reveal>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand">
              Services
            </p>
            <h2 className="mt-4 font-display text-3xl font-bold text-helix-heading dark:text-white sm:text-5xl">
              Digital Weapons Built to Win
            </h2>
            <p className="mt-5 max-w-3xl text-lg leading-relaxed text-slate-600 dark:text-slate-400 sm:text-xl">
              Explore what we offer—content and imagery are managed in the CMS.
            </p>
          </Reveal>
          {orderedServices.length > 0 ? (
          <div className="mt-14 grid gap-5 md:grid-cols-2 lg:grid-cols-3">
            {orderedServices.map((s, i) => (
              <Reveal key={s.slug} delay={0.05 * i}>
                <Link
                  href={`/services/${s.slug}`}
                  className="group flex h-full flex-col overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:border-brand/35 hover:shadow-md dark:border-helix-border dark:bg-helix-bg dark:hover:border-brand/40 dark:hover:shadow-brand/10"
                >
                  <div className="relative aspect-[16/10] bg-slate-100 dark:bg-helix-elevated">
                    {s.cover_image ? (
                      <CmsImage
                        src={s.cover_image}
                        alt=""
                        fill
                        className="object-cover transition duration-500 group-hover:scale-[1.03]"
                        sizes="(max-width:768px) 100vw, 33vw"
                      />
                    ) : (
                      <div className="flex h-full items-center justify-center bg-gradient-to-br from-brand/20 via-slate-100 to-helix-gold/15 text-2xl font-bold text-brand dark:via-helix-elevated">
                        {s.title.slice(0, 1)}
                      </div>
                    )}
                  </div>
                  <div className="flex flex-1 flex-col p-6">
                    <span className="text-base font-semibold text-brand">{s.title}</span>
                    <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400">
                      {s.summary}
                    </p>
                    <span className="mt-4 text-sm font-semibold text-helix-heading opacity-0 transition group-hover:opacity-100 dark:text-white">
                      View service →
                    </span>
                  </div>
                </Link>
              </Reveal>
            ))}
          </div>
          ) : (
            <p className="mt-12 max-w-xl text-slate-600 dark:text-slate-400">
              No services published yet. Add them in Django admin (CMS).
            </p>
          )}
        </div>
      </section>

      <StaffAugmentationSection />

      {featured.length > 0 ? (
        <section
          id="portfolio"
          className="border-t border-slate-200 bg-slate-50 py-20 dark:border-helix-border dark:bg-helix-surface sm:py-28"
        >
          <div className="mx-auto max-w-6xl px-4 sm:px-6">
            <Reveal className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
              <div>
                <h2 className="font-display text-3xl font-bold text-helix-heading dark:text-white sm:text-5xl">
                  Proof. Not Promises.
                </h2>
                <p className="mt-3 max-w-2xl text-lg leading-relaxed text-slate-600 dark:text-slate-400 sm:text-xl">
                  Selected work from the CMS—add projects in admin to populate this section.
                </p>
              </div>
              <Link
                href="/portfolio"
                className="text-base font-semibold text-brand hover:text-brand-hover"
              >
                View full portfolio →
              </Link>
            </Reveal>
            <div className="mt-12 grid gap-6 md:grid-cols-3">
              {featured.map((p, i) => (
                <Reveal key={p.slug} delay={0.06 * i}>
                  <Link
                    href={`/portfolio/${p.slug}`}
                    className="group block overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:border-brand/40 dark:border-helix-border dark:bg-helix-bg dark:hover:border-brand/45"
                  >
                    <div className="relative aspect-[16/10] bg-slate-100 dark:bg-helix-elevated">
                      {p.cover_image ? (
                        <CmsImage
                          src={p.cover_image}
                          alt=""
                          fill
                          className="object-cover transition duration-500 group-hover:scale-[1.03]"
                          sizes="(max-width:768px) 100vw, 33vw"
                        />
                      ) : (
                        <div className="flex h-full items-center justify-center bg-gradient-to-br from-brand/20 via-slate-100 to-helix-gold/15 text-xs text-slate-500 dark:via-helix-elevated">
                          Cover image (admin)
                        </div>
                      )}
                    </div>
                    <div className="p-6">
                      <p className="text-sm font-semibold uppercase tracking-wider text-brand">
                        {p.category}
                      </p>
                      <h3 className="mt-2 font-display text-xl font-semibold text-helix-heading group-hover:text-brand dark:text-white dark:group-hover:text-brand">
                        {p.title}
                      </h3>
                      <p className="mt-3 line-clamp-2 text-base leading-relaxed text-slate-600 dark:text-slate-400">
                        {p.excerpt}
                      </p>
                    </div>
                  </Link>
                </Reveal>
              ))}
            </div>
          </div>
        </section>
      ) : null}

      <TestimonialsSection items={testimonials} />

      <WhyChooseSection />

      <BlogPreviewSection posts={blogPosts} />

      <AboutHomeSection intro={aboutCms.intro} />

      <FinalCtaSection />

      <section
        id="contact"
        className="border-t border-slate-200 bg-slate-50 py-16 dark:border-helix-border dark:bg-helix-surface sm:py-24"
      >
        <div className="mx-auto max-w-6xl px-4 sm:px-6">
          <Reveal>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand">
              Contact
            </p>
            <h2 className="mt-3 font-display text-3xl font-bold text-helix-heading dark:text-white sm:text-5xl">
              Let’s Make Your Competition Nervous
            </h2>
            <p className="mt-5 max-w-2xl text-lg leading-relaxed text-slate-600 dark:text-slate-400 sm:text-xl">
              Ready to explode your revenue, dominate search, launch a killer app, or
              instantly scale your team with elite talent? Our US-focused team is standing
              by. First strategy call is 100% free — no pitch, just a clear plan to get you
              results faster.
            </p>
            <a
              href="#contact-form"
              className="mt-8 inline-flex text-base font-semibold text-brand hover:text-brand-hover"
            >
              Start Dominating Today →
            </a>
            <p className="mt-6 max-w-2xl text-base leading-relaxed text-slate-600 dark:text-slate-400">
              Prefer async? Email us with your goals and timeline—we&apos;ll reply with next
              steps.
            </p>
          </Reveal>

          <div className="mt-12 grid gap-12 lg:grid-cols-2 lg:gap-16">
            <Reveal delay={0.06} className="space-y-8">
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-helix-border dark:bg-helix-elevated sm:p-8">
                <p className="text-sm font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  Email
                </p>
                <a
                  href={`mailto:${CONTACT_EMAIL}`}
                  className="mt-3 block break-all text-xl font-medium text-brand hover:text-brand-hover"
                >
                  {CONTACT_EMAIL}
                </a>
                <p className="mt-4 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
                  We typically respond within one business day for qualified inquiries. For
                  urgent staff-augmentation requests, mention your stack and start date in the
                  subject line so we can route you faster.
                </p>
              </div>
              <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-helix-border dark:bg-helix-elevated sm:p-8">
                <p className="text-sm font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                  What happens next
                </p>
                <ol className="mt-4 list-decimal space-y-3 pl-5 text-sm leading-relaxed text-slate-600 dark:text-slate-400">
                  <li>We acknowledge your message and ask any blocking questions.</li>
                  <li>You get a short call or Loom with a concrete plan—no generic deck.</li>
                  <li>We agree on scope, cadence, and success metrics before any heavy lift.</li>
                </ol>
              </div>
              <p className="text-base leading-relaxed text-slate-500 dark:text-slate-500">
                {COMPANY}
              </p>
            </Reveal>

            <Reveal delay={0.1}>
              <div
                id="contact-form"
                className="rounded-2xl border border-slate-200 bg-white p-6 shadow-md dark:border-helix-border dark:bg-helix-elevated sm:p-10"
              >
                <h3 className="font-display text-2xl font-semibold text-helix-heading dark:text-white sm:text-3xl">
                  Send a message
                </h3>
                <p className="mt-3 text-base leading-relaxed text-slate-600 dark:text-slate-400 sm:text-lg">
                  Tell us what you&apos;re building — we&apos;ll respond with next steps.
                </p>
                <div className="mt-8">
                  <ContactForm serviceOptions={orderedServices} />
                </div>
              </div>
            </Reveal>
          </div>
        </div>
      </section>
    </>
  );
}
