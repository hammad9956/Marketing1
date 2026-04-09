/** Fallback static copy when the content API is unavailable (hero, stats, showcases, about). */
import type {
  CmsAbout,
  CmsHero,
  CmsShowcase,
  CmsStat,
  CmsTestimonial,
} from "@/lib/cms";

export const STATIC_HERO: CmsHero = {
  eyebrow: "USA-market software & growth partner",
  headline: "Dominate Your Market. Explode Your Revenue.",
  subheadline:
    "Websites, SEO, apps, automation, and elite remote teams—built for US revenue growth, not vanity metrics. Senior-led delivery, transparent reporting, and shipping cycles you can plan around.",
  background_image: null,
  cta_primary_label: "Book a Strategy Session",
  cta_primary_link: "/contact",
  cta_secondary_label: "Explore services",
  cta_secondary_link: "/services",
};

export const STATIC_HOME_STATS: CmsStat[] = [
  {
    value: "150+",
    label: "Engagements across web, product, and automation",
  },
  {
    value: "98%",
    label: "Clients who renew or expand their engagement",
  },
  {
    value: "24h",
    label: "Target response for qualified inquiries",
  },
  {
    value: "US",
    label: "Timezone-friendly collaboration as standard",
  },
];

export const STATIC_SHOWCASES: CmsShowcase[] = [];

const _tid = (i: number) => 900_000 + i;

export const STATIC_TESTIMONIALS: CmsTestimonial[] = [
  {
    id: _tid(0),
    client_name: "Sarah M.",
    role_title: "Founder & CEO, B2B SaaS (United States)",
    quote:
      "They reframed our entire acquisition funnel—not just the website. Within one quarter we had clearer messaging, faster pages, and a lead flow we could finally measure.",
    stars: 5,
  },
  {
    id: _tid(1),
    client_name: "Michael C.",
    role_title: "VP Engineering, Fintech (New York)",
    quote:
      "We needed senior engineers who could own features without a six-month hiring cycle. Helix embedded quickly, shipped production code, and documented everything for our internal team.",
    stars: 5,
  },
  {
    id: _tid(2),
    client_name: "Jessica R.",
    role_title: "Director of Operations, E-commerce (California)",
    quote:
      "Automation was sold to us as a buzzword; they delivered real hours back to the team and fewer errors in fulfillment. Communication was crisp the whole way.",
    stars: 5,
  },
];

export const STATIC_ABOUT: CmsAbout = {
  hero_title: "We Don't Do Average. We Deliver Dominance.",
  hero_subtitle:
    "Helix Prime Solutions pairs sharp US-market strategy with disciplined engineering—so ambitious teams get speed, quality, and outcomes tied to pipeline and profit.",
  hero_background_image: null,
  intro:
    "We work with founders, growth leaders, and operators who are done with opaque agencies and shelf-ware deliverables. Every engagement is structured around clear goals, acceptance criteria, and metrics you already track.\n\nWhether you need a high-converting site, a product launch, SEO that compounds, or a senior pod embedded with your team, we align on the shortest path from today's constraints to tomorrow's revenue.",
  mission_title: "Our mission",
  mission_body:
    "Give every client a measurable digital advantage: faster launches, higher conversion, lower operational drag, and reporting you can trust. Enterprise-grade rigor with the urgency of a team that treats your runway as our own.",
  images: [],
};
