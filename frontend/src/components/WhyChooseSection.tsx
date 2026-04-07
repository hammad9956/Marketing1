import { Reveal } from "@/components/Reveal";

const ITEMS = [
  {
    title: "Revenue-First Obsession",
    body: "Every decision is tied to your bottom line: more qualified leads, higher conversion, and profitable growth—not vanity metrics. We align roadmaps, creative, and engineering to the numbers you actually report to the board. When trade-offs appear, we default to what moves revenue and margin.",
  },
  {
    title: "US Strategy + Global Firepower",
    body: "We speak fluent US buyer psychology, compliance sensitivity, and brand tone—then execute with senior teams tuned for speed and craft. You get premium outcomes without the overhead of a coast-to-coast agency roster. Same timezone cadences when you need them; async depth when you don’t.",
  },
  {
    title: "End-to-End Domination",
    body: "One accountable partner for web, SEO, product, automation, integrations, and staff augmentation—no more fragmented vendors pointing fingers. Shared context across channels means faster launches, fewer handoffs, and a single thread from strategy through shipping.",
  },
  {
    title: "Radical Transparency",
    body: "Dashboards, weekly checkpoints, and clear scope so you always know what shipped, what’s next, and why. No black boxes: you see progress, risks, and options in plain language. You stay in control while we carry the execution load.",
  },
  {
    title: "Proven Long-Term Wins",
    body: "Teams stay because we compound value quarter over quarter—documentation, playbooks, and systems that outlive any single campaign. High retention reflects partnerships built on outcomes and trust, not one-off project invoices.",
  },
] as const;

/** lg+ bento: tall flagship left (2×2), four tiles in the right 2×2. */
const BENTO_SPANS = [
  "lg:col-span-2 lg:row-span-2 lg:col-start-1 lg:row-start-1",
  "lg:col-start-3 lg:row-start-1",
  "lg:col-start-4 lg:row-start-1",
  "lg:col-start-3 lg:row-start-2",
  "lg:col-start-4 lg:row-start-2",
] as const;

const CARD_THEMES = [
  {
    bar: "border-l-violet-500",
    surface:
      "from-violet-50/95 via-white to-indigo-50/85 dark:from-violet-950/55 dark:via-slate-900/85 dark:to-indigo-950/45",
    num: "text-violet-500 dark:text-violet-300",
    glow: "from-violet-400 to-indigo-500",
  },
  {
    bar: "border-l-emerald-500",
    surface:
      "from-emerald-50/95 via-white to-teal-50/80 dark:from-emerald-950/45 dark:via-slate-900/85 dark:to-teal-950/38",
    num: "text-emerald-600 dark:text-emerald-400",
    glow: "from-emerald-400 to-teal-400",
  },
  {
    bar: "border-l-amber-500",
    surface:
      "from-amber-50/95 via-white to-orange-50/78 dark:from-amber-950/42 dark:via-slate-900/85 dark:to-orange-950/35",
    num: "text-amber-600 dark:text-amber-400",
    glow: "from-amber-400 to-orange-400",
  },
  {
    bar: "border-l-rose-500",
    surface:
      "from-rose-50/95 via-white to-fuchsia-50/78 dark:from-rose-950/45 dark:via-slate-900/85 dark:to-fuchsia-950/38",
    num: "text-rose-500 dark:text-rose-300",
    glow: "from-rose-400 to-fuchsia-400",
  },
  {
    bar: "border-l-cyan-500",
    surface:
      "from-cyan-50/95 via-white to-sky-50/80 dark:from-cyan-950/40 dark:via-slate-900/85 dark:to-sky-950/40",
    num: "text-cyan-600 dark:text-cyan-300",
    glow: "from-cyan-400 to-sky-500",
  },
] as const;

export function WhyChooseSection() {
  return (
    <section
      id="why-us"
      className="relative overflow-hidden border-t border-slate-200/90 py-20 dark:border-helix-border sm:py-28"
    >
      <div
        className="pointer-events-none absolute inset-0 bg-[linear-gradient(160deg,#f0f4fb_0%,#e8edf6_35%,#f5f2ef_100%)] dark:bg-[linear-gradient(160deg,#070b14_0%,#0c1524_45%,#0a111c_100%)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 bg-[radial-gradient(ellipse_80%_55%_at_15%_20%,rgba(99,102,241,0.14),transparent),radial-gradient(ellipse_70%_50%_at_90%_85%,rgba(6,182,212,0.12),transparent)] dark:bg-[radial-gradient(ellipse_75%_50%_at_20%_15%,rgba(99,102,241,0.12),transparent),radial-gradient(ellipse_65%_45%_at_85%_80%,rgba(34,211,238,0.1),transparent)]"
        aria-hidden
      />
      <div
        className="pointer-events-none absolute inset-0 opacity-[0.28] dark:opacity-[0.15] [background-image:radial-gradient(circle_at_center,rgba(15,23,42,0.06)_1px,transparent_1px)] [background-size:1.35rem_1.35rem] dark:[background-image:radial-gradient(circle_at_center,rgba(255,255,255,0.04)_1px,transparent_1px)]"
        aria-hidden
      />

      <div className="relative mx-auto max-w-6xl px-4 sm:px-6">
        <div className="lg:grid lg:grid-cols-12 lg:items-start lg:gap-10">
          <Reveal className="mx-auto max-w-3xl text-center lg:col-span-4 lg:mx-0 lg:max-w-none lg:pt-1 lg:text-left">
            <p className="text-sm font-semibold uppercase tracking-[0.22em] text-helix-goldMuted">
              Why Helix Prime
            </p>
            <h2 className="mt-4 font-display text-3xl font-bold leading-tight text-helix-heading dark:text-white sm:text-4xl md:text-5xl">
              Why Top US Companies Choose Helix Prime
            </h2>
            <p className="mt-5 text-base leading-relaxed text-slate-600 dark:text-slate-400 sm:text-lg">
              Five reasons revenue leaders replace scattered vendors with one partner built for the US
              market—strategy, delivery, and transparency in one lane.
            </p>
          </Reveal>

          <ul className="mt-12 grid grid-cols-1 gap-4 sm:gap-4 md:grid-cols-2 lg:col-span-8 lg:mt-0 lg:grid-cols-4 lg:grid-rows-2 lg:gap-4">
          {ITEMS.map((item, i) => {
            const theme = CARD_THEMES[i]!;
            const featured = i === 0;
            return (
              <Reveal key={item.title} delay={0.04 * i}>
                <li
                  className={`group relative flex h-full flex-col overflow-hidden rounded-2xl border border-slate-200/90 bg-gradient-to-br shadow-md shadow-slate-900/[0.05] ring-1 ring-white/55 transition duration-300 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-slate-900/10 dark:border-white/10 dark:shadow-black/35 dark:ring-white/[0.04] dark:hover:border-white/12 ${theme.bar} border-l-[5px] ${theme.surface} ${featured ? "md:col-span-2" : ""} ${i === ITEMS.length - 1 ? "md:col-span-2" : ""} ${BENTO_SPANS[i]!} ${featured ? "p-6 sm:p-8" : "p-5 sm:p-6"}`}
                >
                  <div
                    className={`pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full bg-gradient-to-br opacity-20 blur-2xl transition duration-500 group-hover:opacity-35 ${theme.glow}`}
                    aria-hidden
                  />
                  {featured ? (
                    <div className="relative flex flex-col gap-3">
                      <span
                        className={`inline-flex w-fit rounded-lg border border-white/80 bg-white/70 px-2.5 py-1 font-mono text-xs font-bold tabular-nums shadow-sm dark:border-white/10 dark:bg-black/25 ${theme.num}`}
                      >
                        {String(i + 1).padStart(2, "0")}
                      </span>
                      <h3 className="font-display text-xl font-bold leading-snug tracking-tight text-helix-deepNavy dark:text-white sm:text-2xl md:text-[1.65rem]">
                        {item.title}
                      </h3>
                      <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300 sm:text-base">
                        {item.body}
                      </p>
                    </div>
                  ) : (
                    <div className="relative flex h-full flex-col gap-2.5">
                      <span
                        className={`inline-flex w-fit rounded-lg border border-white/80 bg-white/65 px-2 py-0.5 font-mono text-[11px] font-bold tabular-nums shadow-sm dark:border-white/10 dark:bg-black/25 ${theme.num}`}
                      >
                        {String(i + 1).padStart(2, "0")}
                      </span>
                      <h3 className="font-display text-base font-bold leading-snug text-helix-deepNavy dark:text-white sm:text-lg">
                        {item.title}
                      </h3>
                      <p className="text-sm leading-relaxed text-slate-700 dark:text-slate-300">
                        {item.body}
                      </p>
                    </div>
                  )}
                </li>
              </Reveal>
            );
          })}
          </ul>
        </div>
      </div>
    </section>
  );
}
