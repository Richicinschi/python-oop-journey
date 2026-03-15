"use client";

import { Suspense } from "react";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";
import { Loader2, CheckCircle, XCircle } from "lucide-react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

function AuthCallbackContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { verifyToken } = useAuth();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("Completing sign in...");

  useEffect(() => {
    const handleAuth = async () => {
      const token = searchParams.get("token");
      const error = searchParams.get("error");
      const success = searchParams.get("success");

      if (error) {
        setStatus("error");
        setMessage(`Authentication failed: ${error}`);
        setTimeout(() => {
          router.push("/auth/login");
        }, 3000);
        return;
      }

      // Google OAuth returns success=true and sets cookies via redirect
      if (success === "true") {
        try {
          // Cookies are already set by backend, fetch user
          const response = await fetch(`${API_URL}/api/v1/auth/me`, {
            credentials: "include",
          });

          if (response.ok) {
            setStatus("success");
            setMessage("Sign in successful! Redirecting...");
            setTimeout(() => {
              router.push("/");
            }, 1500);
            return;
          } else {
            throw new Error("Failed to get user");
          }
        } catch (e) {
          setStatus("error");
          setMessage("Failed to complete sign in");
          setTimeout(() => {
            router.push("/auth/login");
          }, 3000);
          return;
        }
      }

      // Magic link auth uses token in URL
      if (token) {
        try {
          const success = await verifyToken(token);
          if (success) {
            setStatus("success");
            setMessage("Sign in successful! Redirecting...");
            setTimeout(() => {
              router.push("/");
            }, 1500);
          } else {
            setStatus("error");
            setMessage("Invalid or expired token");
            setTimeout(() => {
              router.push("/auth/login");
            }, 3000);
          }
        } catch (e) {
          setStatus("error");
          setMessage("Failed to complete sign in");
          setTimeout(() => {
            router.push("/auth/login");
          }, 3000);
        }
        return;
      }

      // No token or success param
      setStatus("error");
      setMessage("No authentication information received");
      setTimeout(() => {
        router.push("/auth/login");
      }, 3000);
    };

    handleAuth();
  }, [searchParams, router, verifyToken]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/50">
      <div className="text-center space-y-4">
        {status === "loading" && (
          <>
            <Loader2 className="h-12 w-12 animate-spin mx-auto text-primary" />
            <h1 className="text-xl font-semibold">{message}</h1>
            <p className="text-muted-foreground">Please wait...</p>
          </>
        )}
        
        {status === "success" && (
          <>
            <CheckCircle className="h-12 w-12 mx-auto text-green-500" />
            <h1 className="text-xl font-semibold">{message}</h1>
          </>
        )}
        
        {status === "error" && (
          <>
            <XCircle className="h-12 w-12 mx-auto text-red-500" />
            <h1 className="text-xl font-semibold">{message}</h1>
            <p className="text-muted-foreground">Redirecting to login...</p>
          </>
        )}
      </div>
    </div>
  );
}

export default function AuthCallbackPage() {
  return (
    <Suspense fallback={
      <div className="flex min-h-screen items-center justify-center bg-muted/50">
        <div className="text-center space-y-4">
          <Loader2 className="h-12 w-12 animate-spin mx-auto text-primary" />
          <h1 className="text-xl font-semibold">Loading...</h1>
          <p className="text-muted-foreground">Please wait...</p>
        </div>
      </div>
    }>
      <AuthCallbackContent />
    </Suspense>
  );
}
