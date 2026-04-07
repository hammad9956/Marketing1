import type { Metadata } from "next";
import { BlogsListingClient } from "@/components/BlogsListingClient";
import { Reveal } from "@/components/Reveal";
import { COMPANY } from "@/lib/constants";
import { fetchBlogsList } from "@/lib/cms";

export const revalidate = 60;

export const metadata: Metadata = {
  title: "Blog",
  description: `Insights and playbooks from ${COMPANY} — SEO, product delivery, and growth.`,
};

export default async function BlogsPage() {
  const posts = await fetchBlogsList();

  return (
    <div className="border-b border-slate-200 pb-20 dark:border-helix-border sm:pb-28">
      <section className="border-b border-slate-200 bg-gradient-to-b from-slate-50 to-white py-16 dark:border-helix-border dark:from-helix-bg dark:to-helix-surface sm:py-20">
        <div className="mx-auto max-w-6xl px-4 text-center sm:px-6">
          <Reveal>
            <p className="text-sm font-semibold uppercase tracking-[0.2em] text-brand">
              Insights
            </p>
            <h1 className="mt-4 font-display text-4xl font-bold text-helix-heading dark:text-white sm:text-5xl">
              Blog
            </h1>
            <p className="mx-auto mt-5 max-w-2xl text-lg leading-relaxed text-slate-600 dark:text-slate-400">
              Search by title, then open an article for the full story. Titles and excerpts come from
              CMS → Blog posts in Django Admin.
            </p>
          </Reveal>
        </div>
      </section>

      <div className="pt-14">
        <BlogsListingClient posts={posts} />
      </div>
    </div>
  );
}
