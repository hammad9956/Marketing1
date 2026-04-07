/**
 * Curated Unsplash URLs (hotlinked per Unsplash guidelines) — replace via Django admin when ready.
 * Index is used for stable assignment; use unsplashForSeed() for slug-based variety.
 */
const UNSPLASH = [
  "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1460925895917-afdab827c52f?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1551434678-e076c223a692?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1523240795612-9a054b0db644?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1600880292203-757bb62b4baf?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1200&q=75",
  "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=75",
] as const;

export function unsplashAt(index: number): string {
  const i = ((index % UNSPLASH.length) + UNSPLASH.length) % UNSPLASH.length;
  return UNSPLASH[i]!;
}

/** Stable “random” image from a string (e.g. slug or title). */
export function unsplashForSeed(seed: string): string {
  let h = 0;
  for (let i = 0; i < seed.length; i++) {
    h = (Math.imul(31, h) + seed.charCodeAt(i)) | 0;
  }
  return unsplashAt(Math.abs(h));
}

export const PLACEHOLDER_HERO = unsplashAt(0);
export const PLACEHOLDER_ABOUT_HERO = unsplashAt(2);
export const PLACEHOLDER_SHOWCASE = (i: number) => unsplashAt(i + 4);
