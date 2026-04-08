import type { Metadata } from "next";
import { DM_Sans, Syne } from "next/font/google";
import { ClientShell } from "@/components/ClientShell";
import { Footer } from "@/components/Footer";
import { ThemeProvider } from "@/components/ThemeProvider";
import { getFooterSocialLinks } from "@/lib/footerSocial";
import { COMPANY } from "@/lib/constants";
import "./globals.css";

const themeBootScript = `(function(){try{var t=localStorage.getItem('helix-theme');document.documentElement.classList.toggle('dark',t!=='light');}catch(e){document.documentElement.classList.add('dark');}})();`;

function metadataBaseUrl(): URL {
  const raw = process.env.NEXT_PUBLIC_SITE_URL?.trim();
  if (raw) {
    try {
      return new URL(raw);
    } catch {
      /* invalid env URL */
    }
  }
  return new URL("https://helixprimesolutions.com");
}

const dm = DM_Sans({
  subsets: ["latin"],
  variable: "--font-geist-sans",
  display: "swap",
});

const syne = Syne({
  subsets: ["latin"],
  variable: "--font-syne",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: metadataBaseUrl(),
  title: {
    default: `${COMPANY} | Dominate Your Market. Explode Your Revenue.`,
    template: `%s | ${COMPANY}`,
  },
  description:
    "Helix Prime Solutions builds conversion-obsessed websites, dominates SEO, ships profit-driving apps, and provides elite staff augmentation—engineered for US businesses that want measurable revenue growth.",
  icons: {
    icon: [{ url: "/logo.png", type: "image/png" }],
    apple: [{ url: "/logo.png", type: "image/png" }],
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    siteName: COMPANY,
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const socialLinks = getFooterSocialLinks();

  return (
    <html
      lang="en"
      className={`dark ${dm.variable} ${syne.variable}`}
      suppressHydrationWarning
    >
      <body className="min-h-screen font-sans" suppressHydrationWarning>
        <script dangerouslySetInnerHTML={{ __html: themeBootScript }} />
        <ThemeProvider>
          <ClientShell>{children}</ClientShell>
          <Footer socialLinks={socialLinks} />
        </ThemeProvider>
      </body>
    </html>
  );
}
