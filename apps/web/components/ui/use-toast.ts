"use client"

import { toast as sonnerToast, type ToastT, type ExternalToast } from "sonner"
import { ReactNode } from "react"

type ToastVariant = "default" | "success" | "error" | "warning" | "info"

interface ToastOptions extends Omit<ExternalToast, "description"> {
  title?: string | ReactNode
  description?: string | ReactNode
  variant?: ToastVariant
  duration?: number
}

const variantStyles: Record<ToastVariant, { icon?: string; className?: string }> = {
  default: {},
  success: {
    className: "border-green-500/30 bg-green-500/10",
  },
  error: {
    className: "border-red-500/30 bg-red-500/10",
  },
  warning: {
    className: "border-yellow-500/30 bg-yellow-500/10",
  },
  info: {
    className: "border-blue-500/30 bg-blue-500/10",
  },
}

function toast(options: ToastOptions) {
  const { title, description, variant = "default", duration = 4000, className, ...rest } = options

  const variantClassName = variantStyles[variant]?.className || ""
  const combinedClassName = `${variantClassName} ${className || ""}`.trim()

  const toastOptions: ExternalToast = {
    description,
    duration,
    className: combinedClassName || undefined,
    ...rest,
  }

  switch (variant) {
    case "success":
      return sonnerToast.success(title as string, toastOptions)
    case "error":
      return sonnerToast.error(title as string, toastOptions)
    case "warning":
      return sonnerToast.warning(title as string, toastOptions)
    case "info":
      return sonnerToast.info(title as string, toastOptions)
    default:
      return sonnerToast(title as string, toastOptions)
  }
}

function useToast() {
  return {
    toast,
    dismiss: sonnerToast.dismiss,
    loading: sonnerToast.loading,
    promise: sonnerToast.promise,
  }
}

export { useToast, toast }
export type { ToastOptions, ToastVariant }
