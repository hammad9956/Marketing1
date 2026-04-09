"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { ThemeToggle } from "@/components/ThemeToggle";
import { COMPANY } from "@/lib/constants";
import {
  navFallbackProjects,
  navFallbackServices,
  type NavShellProject,
  type NavShellService,
} from "@/lib/navFallbacks";
function apiBase(): string {
  return (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000").replace(
    /\/$/,
    ""
  );
}

const NAV_FETCH_MS = 4000;

async function fetchNavJson(url: string): Promise<unknown | null> {
  const ctrl = new AbortController();
  const t = window.setTimeout(() => ctrl.abort(), NAV_FETCH_MS);
  try {
    const r = await fetch(url, { signal: ctrl.signal });
    return r.ok ? await r.json() : null;
  } catch {
    return null;
  } finally {
    window.clearTimeout(t);
  }
}

export function Navbar() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [services, setServices] = useState<NavShellService[]>([]);
  const [projects, setProjects] = useState<NavShellProject[]>([]);
  const [mobileSvc, setMobileSvc] = useState(false);
  const [mobilePf, setMobilePf] = useState(false);

  const loadNavData = useCallback(() => {
    const base = apiBase();
    Promise.all([
      fetchNavJson(`${base}/api/cms/services/`),
      fetchNavJson(`${base}/api/cms/projects/`),
    ])
      .then(([svcRaw, pfRaw]) => {
        const svc = svcRaw as { services?: NavShellService[] } | null;
        const pf = pfRaw as { projects?: NavShellProject[] } | null;
        if (svc?.services?.length) {
          setServices(svc.services as NavShellService[]);
        } else {
          setServices(navFallbackServices());
        }
        if (pf?.projects?.length) {
          setProjects(pf.projects as NavShellProject[]);
        } else {
          setProjects(navFallbackProjects());
        }
      })
      .catch(() => {
        setServices(navFallbackServices());
        setProjects(navFallbackProjects());
      });
  }, []);

  useEffect(() => {
    loadNavData();
  }, [loadNavData]);

  const navBtn = (href: string, label: string) => {
    const active = pathname === href;
    return (
      <Link
        href={href}
        prefetch={false}
        className={`rounded-lg px-3 py-2 text-sm font-medium transition ${
          active
            ? "bg-brand/10 text-brand dark:bg-white/10 dark:text-white"
            : "text-slate-600 hover:bg-slate-100 hover:text-helix-heading dark:text-slate-400 dark:hover:bg-white/5 dark:hover:text-white"
        }`}
      >
        {label}
      </Link>
    );
  };

  return (
    <header className="fixed inset-x-0 top-0 z-50 border-b border-slate-200/90 bg-white/90 backdrop-blur-md dark:border-helix-border dark:bg-helix-bg/90">
      <div className="mx-auto flex h-16 max-w-screen-2xl items-center justify-between gap-2 px-4 sm:px-6">
        <Link href="/" prefetch={false} className="group relative z-10 flex min-w-0 items-center gap-2">
          {/* Portrait logo (687×1024): tall slot + object-contain — wide bars crop this asset badly */}
          <span className="relative h-12 w-[calc(3rem*687/1024)] shrink-0 overflow-hidden rounded-lg bg-helix-bg shadow-lg shadow-brand/20 ring-1 ring-white/10 transition group-hover:shadow-brand/35 sm:h-[3.75rem] sm:w-[calc(3.75rem*687/1024)]">
            <Image
              src="/logo.png"
              alt="Helix Prime Solutions"
              fill
              className="object-contain object-center p-0.5"
              sizes="40px"
              priority
            />
          </span>
          <span className="truncate font-display text-lg font-semibold tracking-tight text-helix-heading dark:text-white">
            {COMPANY.replace(" Solutions", "")}
            <span className="text-slate-500 dark:text-slate-500"> Solutions</span>
          </span>
        </Link>

        <nav className="relative z-10 hidden items-center gap-0.5 md:flex">
          {navBtn("/", "Home")}
          {navBtn("/about", "About")}
          <Link
            href="/blogs"
            prefetch={false}
            className={`rounded-lg px-3 py-2 text-sm font-medium transition ${
              pathname.startsWith("/blogs")
                ? "bg-brand/10 text-brand dark:bg-white/10 dark:text-white"
                : "text-slate-600 hover:bg-slate-100 hover:text-helix-heading dark:text-slate-400 dark:hover:bg-white/5 dark:hover:text-white"
            }`}
          >
            Blog
          </Link>

          <div className="group relative">
            <div
              className={`flex items-center rounded-lg px-2 ${
                pathname.startsWith("/services")
                  ? "bg-brand/10 text-brand dark:bg-white/10 dark:text-white"
                  : ""
              }`}
            >
              <Link
                href="/services"
                prefetch={false}
                className="px-2 py-2 text-sm font-medium text-slate-700 hover:text-helix-heading dark:text-slate-300 dark:hover:text-white"
              >
                Services
              </Link>
              <span className="pr-1 text-xs text-slate-400 dark:text-slate-500" aria-hidden>
                ▾
              </span>
            </div>
            <div className="pointer-events-none invisible absolute left-0 top-full z-[200] min-w-[220px] pt-1 opacity-0 transition-all duration-150 group-hover:pointer-events-auto group-hover:visible group-hover:opacity-100">
              <div className="rounded-xl border border-slate-200 bg-white py-2 shadow-xl dark:border-helix-border dark:bg-helix-elevated">
                {services.map((s) => (
                  <Link
                    key={s.slug}
                    href={`/services/${s.slug}`}
                    prefetch={false}
                    className="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 hover:text-brand dark:text-slate-200 dark:hover:bg-white/5 dark:hover:text-brand"
                  >
                    {s.title}
                  </Link>
                ))}
                <Link
                  href="/services"
                  prefetch={false}
                  className="mt-1 block border-t border-slate-100 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-brand dark:border-white/10"
                >
                  View all
                </Link>
              </div>
            </div>
          </div>

          <div className="group relative">
            <div
              className={`flex items-center rounded-lg px-2 ${
                pathname.startsWith("/portfolio")
                  ? "bg-brand/10 text-brand dark:bg-white/10 dark:text-white"
                  : ""
              }`}
            >
              <Link
                href="/portfolio"
                prefetch={false}
                className="px-2 py-2 text-sm font-medium text-slate-700 hover:text-helix-heading dark:text-slate-300 dark:hover:text-white"
              >
                Portfolio
              </Link>
              <span className="pr-1 text-xs text-slate-400 dark:text-slate-500" aria-hidden>
                ▾
              </span>
            </div>
            <div className="pointer-events-none invisible absolute left-0 top-full z-[200] min-w-[240px] pt-1 opacity-0 transition-all duration-150 group-hover:pointer-events-auto group-hover:visible group-hover:opacity-100">
              <div className="max-h-[min(70vh,380px)] overflow-y-auto rounded-xl border border-slate-200 bg-white py-2 shadow-xl dark:border-helix-border dark:bg-helix-elevated">
                {projects.map((p) => (
                  <Link
                    key={p.slug}
                    href={`/portfolio/${p.slug}`}
                    prefetch={false}
                    className="block px-4 py-2 text-sm text-slate-700 hover:bg-slate-50 hover:text-brand dark:text-slate-200 dark:hover:bg-white/5 dark:hover:text-brand"
                  >
                    <span className="block font-medium">{p.title}</span>
                    <span className="text-xs text-slate-500 dark:text-slate-400">
                      {p.category}
                    </span>
                  </Link>
                ))}
                <Link
                  href="/portfolio"
                  prefetch={false}
                  className="mt-1 block border-t border-slate-100 px-4 py-2 text-xs font-semibold uppercase tracking-wider text-brand dark:border-white/10"
                >
                  View all
                </Link>
              </div>
            </div>
          </div>

          {navBtn("/contact", "Contact")}
          <ThemeToggle />
          <Link
            href="/contact"
            prefetch={false}
            className="ml-1 rounded-lg bg-gradient-to-r from-brand to-cyan-600 px-4 py-2 text-sm font-semibold text-helix-bg shadow-md shadow-brand/25 transition hover:brightness-110"
          >
            Book a Strategy Session
          </Link>
        </nav>

        <div className="flex items-center gap-2 md:hidden">
          <ThemeToggle />
          <button
            type="button"
            className="inline-flex h-10 w-10 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 dark:border-helix-border dark:bg-helix-elevated"
            aria-expanded={open}
            aria-label="Toggle menu"
            onClick={() => setOpen((v) => !v)}
          >
            <span className="sr-only">Menu</span>
            <div className="flex flex-col gap-1.5">
              <span
                className={`block h-0.5 w-5 rounded bg-slate-800 transition dark:bg-white ${
                  open ? "translate-y-2 rotate-45" : ""
                }`}
              />
              <span
                className={`block h-0.5 w-5 rounded bg-slate-800 transition dark:bg-white ${
                  open ? "opacity-0" : ""
                }`}
              />
              <span
                className={`block h-0.5 w-5 rounded bg-slate-800 transition dark:bg-white ${
                  open ? "-translate-y-2 -rotate-45" : ""
                }`}
              />
            </div>
          </button>
        </div>
      </div>

      {open ? (
        <div className="max-h-[min(85vh,calc(100dvh-4rem))] overflow-y-auto border-b border-slate-200 bg-white/98 dark:border-helix-border dark:bg-helix-bg/98 md:hidden">
            <div className="flex flex-col gap-1 px-4 py-4">
              <Link
                href="/"
                prefetch={false}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-3 text-sm font-medium text-slate-800 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-white/5"
              >
                Home
              </Link>
              <Link
                href="/about"
                prefetch={false}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-3 text-sm font-medium text-slate-800 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-white/5"
              >
                About
              </Link>
              <Link
                href="/blogs"
                prefetch={false}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-3 text-sm font-medium text-slate-800 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-white/5"
              >
                Blog
              </Link>

              <button
                type="button"
                onClick={() => setMobileSvc((v) => !v)}
                className="flex w-full items-center justify-between rounded-lg px-3 py-3 text-left text-sm font-medium text-slate-800 dark:text-slate-200"
              >
                Services
                <span className="text-slate-400">{mobileSvc ? "▴" : "▾"}</span>
              </button>
              {mobileSvc ? (
                <div className="ml-2 flex flex-col border-l border-slate-200 pl-3 dark:border-white/10">
                  {services.map((s) => (
                    <Link
                      key={s.slug}
                      href={`/services/${s.slug}`}
                      prefetch={false}
                      onClick={() => setOpen(false)}
                      className="py-2 text-sm text-slate-600 hover:text-brand dark:text-slate-400"
                    >
                      {s.title}
                    </Link>
                  ))}
                  <Link
                    href="/services"
                    prefetch={false}
                    onClick={() => setOpen(false)}
                    className="py-2 text-xs font-semibold uppercase tracking-wider text-brand"
                  >
                    View all services
                  </Link>
                </div>
              ) : null}

              <button
                type="button"
                onClick={() => setMobilePf((v) => !v)}
                className="flex w-full items-center justify-between rounded-lg px-3 py-3 text-left text-sm font-medium text-slate-800 dark:text-slate-200"
              >
                Portfolio
                <span className="text-slate-400">{mobilePf ? "▴" : "▾"}</span>
              </button>
              {mobilePf ? (
                <div className="ml-2 flex max-h-52 flex-col overflow-y-auto border-l border-slate-200 pl-3 dark:border-white/10">
                  {projects.map((p) => (
                    <Link
                      key={p.slug}
                      href={`/portfolio/${p.slug}`}
                      prefetch={false}
                      onClick={() => setOpen(false)}
                      className="py-2 text-sm text-slate-600 hover:text-brand dark:text-slate-400"
                    >
                      {p.title}
                    </Link>
                  ))}
                  <Link
                    href="/portfolio"
                    prefetch={false}
                    onClick={() => setOpen(false)}
                    className="py-2 text-xs font-semibold uppercase tracking-wider text-brand"
                  >
                    View all projects
                  </Link>
                </div>
              ) : null}

              <Link
                href="/contact"
                prefetch={false}
                onClick={() => setOpen(false)}
                className="rounded-lg px-3 py-3 text-sm font-medium text-slate-800 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-white/5"
              >
                Contact
              </Link>
              <Link
                href="/contact"
                prefetch={false}
                onClick={() => setOpen(false)}
                className="mt-2 rounded-lg bg-brand px-3 py-3 text-center text-sm font-semibold text-helix-bg hover:bg-brand-hover"
              >
                Book a Strategy Session
              </Link>
            </div>
        </div>
      ) : null}
    </header>
  );
}
