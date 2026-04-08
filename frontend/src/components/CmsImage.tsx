import Image from "next/image";

/** If the API returns a root-relative /media/... URL, load it from the Django origin. */
function resolveCmsSrc(src: string): string {
  const s = src.trim();
  if (/^https?:\/\//i.test(s)) return s;
  if (s.startsWith("/")) {
    const base = process.env.NEXT_PUBLIC_API_URL?.replace(/\/$/, "") ?? "";
    if (base) return `${base}${s}`;
  }
  return s;
}

type Props = {
  src: string | null | undefined;
  alt: string;
  className?: string;
  width?: number;
  height?: number;
  fill?: boolean;
  sizes?: string;
  priority?: boolean;
};

export function CmsImage({
  src,
  alt,
  className,
  width = 1200,
  height = 800,
  fill,
  sizes,
  priority,
}: Props) {
  if (!src) return null;

  const resolved = resolveCmsSrc(src);

  if (fill) {
    return (
      <Image
        src={resolved}
        alt={alt}
        fill
        className={className}
        sizes={sizes}
        priority={priority}
        unoptimized={
          resolved.includes("127.0.0.1") ||
          resolved.includes("localhost") ||
          resolved.includes("images.unsplash.com") ||
          resolved.includes("res.cloudinary.com")
        }
      />
    );
  }

  return (
    <Image
      src={resolved}
      alt={alt}
      width={width}
      height={height}
      className={className}
      priority={priority}
      unoptimized={
        resolved.includes("127.0.0.1") ||
        resolved.includes("localhost") ||
        resolved.includes("images.unsplash.com") ||
        resolved.includes("res.cloudinary.com")
      }
    />
  );
}
