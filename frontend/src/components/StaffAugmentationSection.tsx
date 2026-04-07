import { Reveal } from "@/components/Reveal";

const BENEFIT_CARDS = [
  {
    title: "Slash Costs by 60%",
    body: "Blend senior output with rates that respect your runway. We help you redirect budget from idle overhead into shipping—without sacrificing quality or accountability.",
  },
  {
    title: "Scale Instantly",
    body: "Add vetted engineers, designers, or specialists in days—not quarters. Surge for launches, then right-size once the spike cools.",
  },
  {
    title: "Unfair Talent Advantage",
    body: "US-market polish with execution discipline: crisp communication, ownership, and delivery habits shaped for demanding stakeholders and fast feedback loops.",
  },
  {
    title: "Speed That Crushes Competitors",
    body: "Parallel workstreams and fewer hiring bottlenecks mean your roadmap moves while others are still scheduling screens and negotiating offers.",
  },
  {
    title: "Total Control",
    body: "You set priorities and own the product; our people embed like senior ICs on your tools, ceremonies, and reporting—no black-box handoffs.",
  },
] as const;

/** Bento placement on lg+ (3×3 grid). Mobile/tablet: single column stack. */
const BENTO_SPANS = [
  "lg:col-span-2 lg:row-span-2 lg:row-start-1 lg:col-start-1",
  "lg:col-start-3 lg:row-start-1",
  "lg:col-start-3 lg:row-start-2",
  "lg:col-start-1 lg:row-start-3",
  "lg:col-span-2 lg:col-start-2 lg:row-start-3",
] as const;

/** Per-card tint + left accent (light / dark). */
const CARD_THEMES = [
  {
    bar: "border-l-indigo-500",
    surface:
      "from-indigo-50/95 via-white to-violet-50/80 dark:from-indigo-950/50 dark:via-slate-900/80 dark:to-violet-950/40",
    num: "text-indigo-400 dark:text-indigo-300",
  },
  {
    bar: "border-l-emerald-500",
    surface:
      "from-emerald-50/95 via-white to-teal-50/75 dark:from-emerald-950/45 dark:via-slate-900/80 dark:to-teal-950/35",
    num: "text-emerald-500 dark:text-emerald-400",
  },
  {
    bar: "border-l-amber-500",
    surface:
      "from-amber-50/95 via-white to-orange-50/75 dark:from-amber-950/40 dark:via-slate-900/80 dark:to-orange-950/35",
    num: "text-amber-600 dark:text-amber-400",
  },
  {
    bar: "border-l-rose-500",
    surface:
      "from-rose-50/95 via-white to-fuchsia-50/75 dark:from-rose-950/45 dark:via-slate-900/80 dark:to-fuchsia-950/35",
    num: "text-rose-500 dark:text-rose-300",
  },
  {
    bar: "border-l-sky-500",
    surface:
      "from-sky-50/95 via-white to-blue-50/75 dark:from-sky-950/45 dark:via-slate-900/80 dark:to-blue-950/35",
    num: "text-sky-500 dark:text-sky-300",
  },
] as const;

const CARD_GLOW = [
  "from-indigo-400 to-violet-400",
  "from-emerald-400 to-teal-400",
  "from-amber-400 to-orange-400",
  "from-rose-400 to-fuchsia-400",
  "from-sky-400 to-blue-500",
] as const;

export function StaffAugmentationSection() {
  return (
    <section
      id="staff-augmentation"
      className="relative overflow-hidden border-t border-slate-200/90 py-20 dark:border-helix-border sm:py-28"
    >
      {/* Warm shell + corner glow (different from prior slate/indigo wash) */}
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(165deg,#faf8f5_0%,#f0f4f8_45%,#e8f5f0_100%)] dark:bg-[linear-gradient(165deg,#070b14_0%,#0a1420_50%,#071018_100%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_90%_60%_at_100%_0%,rgba(251,191,36,0.12),transparent),radial-gradient(ellipse_70%_50%_at_0%_100%,rgba(56,189,248,0.14),transparent)] dark:bg-[radial-gradient(ellipse_80%_55%_at_95%_5%,rgba(251,191,36,0.08),transparent),radial-gradient(ellipse_65%_50%_at_5%_95%,rgba(34,211,238,0.1),transparent)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.35] dark:opacity-[0.2] [background-image:linear-gradient(rgba(15,23,42,0.04)_1px,transparent_1px),linear-gradient(90deg,rgba(15,23,42,0.04)_1px,transparent_1px)] [background-size:2.25rem_2.25rem] dark:[background-image:linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)]"
        aria-hidden
      />

      <div className="relative mx-auto max-w-6xl px-4 sm:px-6">
        <Reveal>
          <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand drop-shadow-sm">
            Staff augmentation
          </p>
          <h2 className="mt-4 max-w-4xl font-display text-3xl font-bold leading-tight text-helix-deepNavy dark:text-white sm:text-4xl md:text-5xl">
            Staff Augmentation: Elite Talent. Zero Drama. Instant Scale.
          </h2>
          <p className="mt-6 max-w-3xl text-lg leading-relaxed text-slate-700 dark:text-slate-400 sm:text-xl">
            Tired of slow hiring, sky-high salaries, and underperforming teams? Staff
            augmentation from Helix Prime gives you immediate access to battle-tested
            US-market-ready developers, designers, and digital experts who plug into your
            team and deliver from day one.
          </p>
          <p className="mt-4 max-w-3xl text-lg font-semibold leading-relaxed text-slate-800 dark:text-slate-200">
            No long onboarding. No bloated overhead. Just pure firepower.
          </p>
        </Reveal>

        <Reveal delay={0.06} className="mt-14">
          <div className="lg:grid lg:grid-cols-12 lg:gap-10 lg:items-start">
            <div className="lg:col-span-4 lg:pt-2">
              <p className="text-center text-xs font-semibold uppercase tracking-[0.22em] text-helix-goldMuted sm:text-left sm:text-sm">
                Why companies choose us for staff augmentation
              </p>
              <p className="mx-auto mt-4 max-w-sm text-center text-sm leading-relaxed text-slate-600 dark:text-slate-500 sm:mx-0 sm:text-left">
                Five concrete outcomes we hear from teams that augment with Helix Prime—laid
                out as a quick-scan bento.
              </p>
            </div>

            <ul className="mt-10 grid grid-cols-1 gap-4 sm:gap-5 md:grid-cols-2 lg:col-span-8 lg:mt-0 lg:grid-cols-3 lg:grid-rows-3 lg:gap-4">
              {BENEFIT_CARDS.map((card, i) => {
                const theme = CARD_THEMES[i]!;
                const featured = i === 0;
                return (
                  <li
                    key={card.title}
                    className={`group relative overflow-hidden rounded-2xl border border-slate-200/90 bg-gradient-to-br shadow-lg shadow-slate-900/[0.06] ring-1 ring-white/60 transition duration-300 hover:-translate-y-0.5 hover:shadow-xl hover:shadow-slate-900/10 dark:border-white/10 dark:shadow-black/40 dark:ring-white/[0.04] dark:hover:border-white/15 ${theme.bar} border-l-[5px] ${theme.surface} ${featured ? "md:col-span-2" : ""} ${BENTO_SPANS[i]!} ${featured ? "min-h-[5.5rem] p-6 sm:p-7 lg:min-h-0 lg:p-8" : "min-h-[4.5rem] p-5 sm:p-6"}`}
                  >
                    <div
                      className={`pointer-events-none absolute -right-6 -top-6 h-24 w-24 rounded-full bg-gradient-to-br opacity-25 blur-2xl transition duration-500 group-hover:opacity-40 ${CARD_GLOW[i]!}`}
                      aria-hidden
                    />
                    {featured ? (
                      <div className="relative flex h-full flex-col justify-start gap-3">
                        <span
                          className={`font-mono text-sm font-semibold tabular-nums ${theme.num}`}
                        >
                          {String(i + 1).padStart(2, "0")}
                        </span>
                        <p className="font-display text-xl font-bold leading-snug tracking-tight text-helix-deepNavy dark:text-white sm:text-2xl">
                          {card.title}
                        </p>
                        <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-400 sm:text-base">
                          {card.body}
                        </p>
                      </div>
                    ) : (
                      <div className="relative flex items-start gap-3">
                        <span
                          className={`mt-0.5 shrink-0 font-mono text-xs font-bold tabular-nums ${theme.num}`}
                        >
                          {String(i + 1).padStart(2, "0")}
                        </span>
                        <div className="min-w-0 flex-1 space-y-2">
                          <p className="text-base font-bold leading-snug text-helix-deepNavy dark:text-white sm:text-lg">
                            {card.title}
                          </p>
                          <p className="text-sm leading-relaxed text-slate-600 dark:text-slate-400">
                            {card.body}
                          </p>
                        </div>
                      </div>
                    )}
                  </li>
                );
              })}
            </ul>
          </div>

          <p className="mx-auto mt-12 max-w-2xl text-center text-base font-medium leading-relaxed text-slate-700 dark:text-slate-400 sm:mx-0 sm:max-w-3xl sm:text-left">
            Perfect for startups racing to launch and established businesses scaling without
            breaking the bank.
          </p>
        </Reveal>
      </div>
    </section>
  );
}
