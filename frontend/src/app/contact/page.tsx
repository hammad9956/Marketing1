import type { Metadata } from "next";
import Link from "next/link";
import { ContactForm } from "@/components/ContactForm";
import {
  ContactMailIcon,
  ContactMapPinIcon,
  ContactPhoneIcon,
} from "@/components/ContactInfoIcons";
import { Reveal } from "@/components/Reveal";
import {
  COMPANY,
  OFFICE_ADDRESS,
  officePhoneTelHref,
  publicContactEmails,
  publicOfficePhones,
} from "@/lib/constants";
import { fetchServicesList } from "@/lib/cms";

export const revalidate = 60;

export const metadata: Metadata = {
  title: "Contact",
  description: `Contact ${COMPANY}—book a call, request a quote, or send a project inquiry.`,
};

export default async function ContactPage() {
  const services = await fetchServicesList();

  return (
    <div className="mx-auto max-w-screen-2xl px-4 py-16 sm:px-6 sm:py-24">
      <div className="grid gap-12 lg:grid-cols-2 lg:gap-16">
        <div>
          <Reveal>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand">
              Contact
            </p>
            <h1 className="mt-3 font-display text-4xl font-bold text-helix-heading dark:text-white sm:text-5xl md:text-6xl">
              Let&apos;s plan your next release
            </h1>
            <p className="mt-6 text-xl leading-relaxed text-slate-600 dark:text-slate-400 sm:text-2xl">
              Use the form for structured inquiries, or email us directly. For live chat,
              use the floating button (configure Tawk.to in env for full widget support).
            </p>
          </Reveal>

          <Reveal delay={0.08} className="mt-10 space-y-6">
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 dark:border-helix-border dark:bg-helix-surface/70">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                Email
              </p>
              <ul className="mt-3 space-y-3">
                {publicContactEmails().map((email) => (
                  <li key={email} className="flex gap-3">
                    <ContactMailIcon className="mt-1 h-5 w-5 shrink-0 text-slate-500 dark:text-slate-400" />
                    <a
                      href={`mailto:${email}`}
                      className="break-all text-lg font-medium text-brand hover:text-brand-hover dark:hover:text-brand"
                    >
                      {email}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 dark:border-helix-border dark:bg-helix-surface/70">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                What to include
              </p>
              <ul className="mt-3 list-inside list-disc space-y-2 text-base text-slate-600 dark:text-slate-400 sm:text-lg">
                <li>Company context and primary goal</li>
                <li>Ideal timeline and budget range</li>
                <li>Links or references that clarify the vision</li>
              </ul>
            </div>
            <div className="rounded-2xl border border-slate-200 bg-slate-50 p-6 dark:border-helix-border dark:bg-helix-surface/70">
              <p className="text-xs font-semibold uppercase tracking-wider text-slate-500">
                {OFFICE_ADDRESS || publicOfficePhones().length > 0
                  ? "Office & phone"
                  : "Explore first"}
              </p>
              {OFFICE_ADDRESS || publicOfficePhones().length > 0 ? (
                <ul className="mt-3 space-y-3 text-base text-slate-600 dark:text-slate-400 sm:text-lg">
                  {OFFICE_ADDRESS ? (
                    <li className="flex gap-3">
                      <ContactMapPinIcon className="mt-1 h-5 w-5 shrink-0 text-slate-500 dark:text-slate-400" />
                      <span className="whitespace-pre-line leading-relaxed">{OFFICE_ADDRESS}</span>
                    </li>
                  ) : null}
                  {publicOfficePhones().map((phone) => (
                    <li key={phone} className="flex gap-3">
                      <ContactPhoneIcon className="mt-1 h-5 w-5 shrink-0 text-slate-500 dark:text-slate-400" />
                      <a
                        href={officePhoneTelHref(phone)}
                        className="font-semibold text-brand hover:text-brand-hover"
                      >
                        {phone}
                      </a>
                    </li>
                  ))}
                </ul>
              ) : null}
              <p
                className={`text-base leading-relaxed text-slate-600 dark:text-slate-400 sm:text-lg ${OFFICE_ADDRESS || publicOfficePhones().length > 0 ? "mt-4 border-t border-slate-200 pt-4 dark:border-white/10" : "mt-3"}`}
              >
                See{" "}
                <Link href="/services" className="font-semibold text-brand hover:text-brand-hover">
                  services
                </Link>
                ,{" "}
                <Link href="/portfolio" className="font-semibold text-brand hover:text-brand-hover">
                  portfolio
                </Link>
                , and{" "}
                <Link href="/about" className="font-semibold text-brand hover:text-brand-hover">
                  about
                </Link>{" "}
                for context—then tell us what you want to ship next.
              </p>
            </div>
          </Reveal>
        </div>

        <Reveal delay={0.06}>
          <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm dark:border-helix-border dark:bg-helix-elevated sm:p-8">
            <h2 className="font-display text-2xl font-semibold text-helix-heading dark:text-white sm:text-3xl">
              Inquiry form
            </h2>
            <p className="mt-3 text-base text-slate-600 dark:text-slate-400 sm:text-lg">
              We review every submission and follow up as soon as we can.
            </p>
            <div className="mt-8">
              <ContactForm serviceOptions={services} />
            </div>
          </div>
        </Reveal>
      </div>
    </div>
  );
}
