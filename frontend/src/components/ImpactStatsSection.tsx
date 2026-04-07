"use client";

import type { CmsStat } from "@/lib/cms";
import { useInView } from "@/hooks/useInView";
import { usePrefersReducedMotion } from "@/hooks/usePrefersReducedMotion";
import { useEffect, useRef, useState } from "react";

function easeOutCubic(t: number) {
  return 1 - Math.pow(1 - t, 3);
}

function parseNumericValue(raw: string): {
  target: number;
  decimals: number;
  prefix: string;
  suffix: string;
} | null {
  const s = raw.trim();
  const match = s.match(/^([^0-9.-]*)(-?[\d.]+)([^0-9.]*)$/);
  if (!match) return null;
  const num = Number.parseFloat(match[2]);
  if (!Number.isFinite(num)) return null;
  const decimals = match[2].includes(".") ? match[2].split(".")[1]?.length ?? 0 : 0;
  return { target: num, decimals, prefix: match[1], suffix: match[3] };
}

function useCountUp(
  target: number,
  durationMs: number,
  active: boolean,
  startDelayMs: number,
  reduceMotion: boolean,
  decimals: number
) {
  const [value, setValue] = useState(0);
  const rafRef = useRef(0);

  useEffect(() => {
    if (!active) {
      setValue(0);
      return;
    }
    if (reduceMotion) {
      setValue(target);
      return;
    }

    let delayTimer: ReturnType<typeof setTimeout>;

    const run = () => {
      const start = performance.now();
      const tick = (now: number) => {
        const elapsed = now - start;
        const t = Math.min(elapsed / durationMs, 1);
        const eased = easeOutCubic(t);
        const raw = eased * target;
        const rounded =
          decimals > 0
            ? Math.round(raw * Math.pow(10, decimals)) / Math.pow(10, decimals)
            : Math.round(raw);
        setValue(rounded);
        if (t < 1) {
          rafRef.current = requestAnimationFrame(tick);
        }
      };
      rafRef.current = requestAnimationFrame(tick);
    };

    delayTimer = setTimeout(run, startDelayMs);
    return () => {
      clearTimeout(delayTimer);
      cancelAnimationFrame(rafRef.current);
    };
  }, [active, target, durationMs, startDelayMs, reduceMotion, decimals]);

  return value;
}

const statCardClass =
  "relative overflow-hidden rounded-2xl border border-white/10 bg-[#0b122e] p-6 shadow-lg shadow-black/30";

function TextStatBlock({ stat }: { stat: CmsStat }) {
  return (
    <div className={statCardClass}>
      <p className="font-display text-3xl font-bold tabular-nums tracking-tight text-brand sm:text-4xl">
        {stat.value}
      </p>
      <p className="mt-3 text-base leading-snug text-slate-300">
        {stat.label}
      </p>
    </div>
  );
}

function NumericStatBlock({
  stat,
  parsed,
  active,
  index,
  reduceMotion,
}: {
  stat: CmsStat;
  parsed: NonNullable<ReturnType<typeof parseNumericValue>>;
  active: boolean;
  index: number;
  reduceMotion: boolean;
}) {
  const n = useCountUp(
    parsed.target,
    2200,
    active,
    index * 140,
    reduceMotion,
    parsed.decimals
  );
  const display =
    parsed.decimals > 0 ? n.toFixed(parsed.decimals) : String(Math.round(n));

  return (
    <div className={statCardClass}>
      <div className="absolute right-5 top-5 flex gap-1" aria-hidden>
        {[0, 1, 2].map((dot) => (
          <span key={dot} className="h-1.5 w-1.5 rounded-full bg-brand" />
        ))}
      </div>
      <p className="tabular-nums">
        <span className="font-display text-3xl font-bold tabular-nums tracking-tight text-brand sm:text-4xl">
          {parsed.prefix}
          {display}
          {parsed.suffix === "x" ? "X" : parsed.suffix}
        </span>
      </p>
      <p className="mt-3 text-base leading-snug text-slate-300">
        {stat.label}
      </p>
    </div>
  );
}

function StatBlock(props: {
  stat: CmsStat;
  active: boolean;
  index: number;
  reduceMotion: boolean;
}) {
  const parsed = parseNumericValue(props.stat.value);
  if (!parsed) {
    return <TextStatBlock stat={props.stat} />;
  }
  return <NumericStatBlock {...props} parsed={parsed} />;
}

type Props = {
  stats: CmsStat[];
};

export function ImpactStatsSection({ stats }: Props) {
  const sectionRef = useRef<HTMLElement>(null);
  const inView = useInView(sectionRef, {
    once: true,
    amount: 0.12,
    rootMargin: "0px 0px 20% 0px",
  });
  const reduceMotion = usePrefersReducedMotion();

  if (!stats.length) return null;

  return (
    <section
      ref={sectionRef}
      id="impact"
      className="border-y border-slate-200 bg-gradient-to-b from-slate-100 via-white to-slate-100 py-16 dark:border-white/10 dark:from-[#070b14] dark:via-[#0A1128] dark:to-[#070b14] sm:py-24"
    >
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="grid gap-12 lg:grid-cols-12 lg:items-start">
          <div className="lg:col-span-5">
            <div>
              <span className="inline-flex items-center gap-2 rounded-full border border-slate-200 bg-white px-4 py-2 text-sm font-semibold uppercase tracking-wider text-brand shadow-sm dark:border-white/15 dark:bg-white/5 dark:shadow-none">
                Our impact
              </span>
              <h2 className="mt-6 font-display text-3xl font-bold leading-tight tracking-tight text-helix-heading dark:text-white sm:text-4xl lg:text-[2.65rem] lg:leading-[1.12]">
                Numbers That Actually Matter
              </h2>
              <p className="mt-6 text-lg leading-relaxed text-slate-600 dark:text-slate-400">
                These figures are whatever you save under CMS → Home — Impact stats in Django Admin.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:col-span-7">
            {stats.map((s, i) => (
              <StatBlock
                key={`${s.label}-${i}`}
                stat={s}
                active={inView}
                index={i}
                reduceMotion={reduceMotion}
              />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
