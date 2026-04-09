export const COMPANY = "Helix Prime Solutions";

/** Footer / contact — set in env (supports \n for multi-line address). */
export const OFFICE_ADDRESS =
  process.env.NEXT_PUBLIC_OFFICE_ADDRESS?.trim().replace(/\\n/g, "\n") || "";

export const OFFICE_PHONE = process.env.NEXT_PUBLIC_OFFICE_PHONE?.trim() || "";

/** Second public line — optional; shown as a separate link next to `OFFICE_PHONE`. */
export const OFFICE_PHONE_2 = process.env.NEXT_PUBLIC_OFFICE_PHONE_2?.trim() || "";

/** Office numbers with values set in env, first and second in order. */
export function publicOfficePhones(): string[] {
  return [OFFICE_PHONE, OFFICE_PHONE_2].filter((p) => p.length > 0);
}

/** `tel:` href for a display phone string (digits and leading + kept). */
export function officePhoneTelHref(phone: string): string {
  return `tel:${phone.replace(/[^\d+]/g, "")}`;
}

export const CONTACT_EMAIL =
  process.env.NEXT_PUBLIC_CONTACT_EMAIL || "info@helixprimesolutions.com";

/** General inquiries — shown next to `CONTACT_EMAIL` when different. */
export const INFO_EMAIL =
  process.env.NEXT_PUBLIC_INFO_EMAIL?.trim() || "info@helixprimesolutions.com";

/** Distinct public inboxes for mailto links (deduped). */
export function publicContactEmails(): readonly string[] {
  const a = CONTACT_EMAIL.trim();
  const b = INFO_EMAIL.trim();
  if (!b) return [a];
  if (a.toLowerCase() === b.toLowerCase()) return [a];
  return [a, b];
}

type SocialId =
  | "linkedin"
  | "x"
  | "facebook"
  | "github"
  | "instagram"
  | "whatsapp";

/** Set env to `""` to hide a network. Replace URLs with your real profiles. */
export const SOCIAL_LINKS: { id: SocialId; label: string; href: string }[] = [
  {
    id: "linkedin",
    label: "LinkedIn",
    href:
      process.env.NEXT_PUBLIC_SOCIAL_LINKEDIN?.trim() ??
      "https://www.linkedin.com/company/helix-prime-solutions",
  },
  {
    id: "x",
    label: "X",
    href: process.env.NEXT_PUBLIC_SOCIAL_X?.trim() ?? "https://x.com/helixprimesolutions",
  },
  {
    id: "facebook",
    label: "Facebook",
    href:
      process.env.NEXT_PUBLIC_SOCIAL_FACEBOOK?.trim() ??
      "https://www.facebook.com/helixprimesolutions",
  },
  {
    id: "github",
    label: "GitHub",
    href:
      process.env.NEXT_PUBLIC_SOCIAL_GITHUB?.trim() ??
      "https://github.com/helix-prime-solutions",
  },
  {
    id: "instagram",
    label: "Instagram",
    href: process.env.NEXT_PUBLIC_SOCIAL_INSTAGRAM?.trim() ?? "",
  },
  {
    id: "whatsapp",
    label: "WhatsApp",
    href: process.env.NEXT_PUBLIC_SOCIAL_WHATSAPP?.trim() ?? "",
  },
].filter((l): l is { id: SocialId; label: string; href: string } => l.href.length > 0);

/** Optional sort order for home “Services” grid when CMS returns items (slug → position). */
export const SERVICE_SLUG_ORDER: readonly string[] = [];

