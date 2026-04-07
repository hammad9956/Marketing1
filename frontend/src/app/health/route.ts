import { NextResponse } from "next/server";

/** Fast probe for Railway — never calls Django (unlike `/`, which SSR-fetches CMS). */
export const dynamic = "force-static";

export function GET() {
  return NextResponse.json({ ok: true }, { status: 200 });
}
