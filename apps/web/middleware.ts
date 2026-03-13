import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Paths that require authentication
const protectedPaths = [
  "/profile",
  "/bookmarks",
  "/progress",
];

// Paths that are only accessible to non-authenticated users
const authPaths = ["/auth/login", "/auth/callback"];

// Cookie name for auth token (matches localStorage key in auth-context)
const AUTH_COOKIE_NAME = "auth_token";

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check for auth token in cookies
  const authToken = request.cookies.get(AUTH_COOKIE_NAME)?.value;
  const isAuthenticated = !!authToken;

  // Check if current path is protected
  const isProtectedPath = protectedPaths.some(
    (path) => pathname === path || pathname.startsWith(`${path}/`)
  );

  // Check if current path is an auth path
  const isAuthPath = authPaths.some(
    (path) => pathname === path || pathname.startsWith(`${path}/`)
  );

  // Redirect unauthenticated users from protected paths to login
  if (isProtectedPath && !isAuthenticated) {
    const returnUrl = encodeURIComponent(pathname);
    const loginUrl = new URL(`/auth/login?returnUrl=${returnUrl}`, request.url);
    return NextResponse.redirect(loginUrl);
  }

  // Redirect authenticated users from auth paths to home
  if (isAuthPath && isAuthenticated && pathname !== "/auth/callback") {
    // Allow callback page even when authenticated (for token exchange)
    const homeUrl = new URL("/", request.url);
    return NextResponse.redirect(homeUrl);
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    /*
     * Match all request paths except:
     * - _next/static (static files)
     * - _next/image (image optimization files)
     * - favicon.ico (favicon file)
     * - public folder
     */
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
