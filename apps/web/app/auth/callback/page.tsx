"use client";

import { Suspense } from "react";
import { useEffect, useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/contexts/auth-context";
import { Loader2, CheckCircle, XCircle } from "lucide-react";

function AuthCallbackContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { setToken } = useAuth();
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");
  const [message, setMessage] = useState("Completing sign in...");

  useEffect(() => {
    const handleAuth = async () => {
      const token = searchParams.get("token");
      const error = searchParams.get("error");

      if (error) {
        setStatus("error");
        setMessage(`Authentication failed: ${error}`);
        setTimeout(() => {
          router.push("/auth/login");
        }, 3000);
        return;
      }

      if (!token) {
        setStatus("error");
        setMessage("No authentication token received");
        setTimeout(() => {
          router.push("/auth/login");
        }, 3000);
        return;
      }

      try {
        // Store the token
        setToken(token);
        setStatus("success");
        setMessage("Sign in successful! Redirecting...");
        
        // Redirect to dashboard after short delay
        setTimeout(() => {
          router.push("/");
        }, 1500);
      } catch (e) {
        setStatus("error");
        setMessage("Failed to complete sign in");
        setTimeout(() => {
          router.push("/auth/login");
        }, 3000);
      }
    };

    handleAuth();
  }, [searchParams, router, setToken]);

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
