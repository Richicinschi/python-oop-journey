import { Metadata } from 'next';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { ChevronLeft, Scale, FileText, Shield, AlertCircle } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Terms of Service | Python OOP Journey',
  description: 'Terms of Service for Python OOP Journey platform',
};

export default function TermsPage() {
  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      {/* Header */}
      <div className="mb-8">
        <Button variant="ghost" size="sm" asChild className="mb-4">
          <Link href="/auth/login">
            <ChevronLeft className="h-4 w-4 mr-2" />
            Back to Login
          </Link>
        </Button>
        
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-primary/10">
            <Scale className="h-6 w-6 text-primary" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Terms of Service</h1>
            <p className="text-muted-foreground">
              Last updated: March 2026
            </p>
          </div>
        </div>
      </div>

      {/* Introduction */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <FileText className="h-5 w-5" />
            Introduction
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            Welcome to Python OOP Journey. These Terms of Service govern your use of our 
            educational platform and services. By accessing or using the platform, you 
            agree to be bound by these terms.
          </p>
          <p>
            Please read these terms carefully before using our services. If you do not 
            agree to these terms, you may not access or use the platform.
          </p>
        </CardContent>
      </Card>

      {/* Account Terms */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Shield className="h-5 w-5" />
            Account Terms
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">
            To use certain features of the platform, you must create an account. You agree to:
          </p>
          <ul className="space-y-2 text-muted-foreground list-disc list-inside">
            <li>Provide accurate and complete information when creating your account</li>
            <li>Maintain the security of your account credentials</li>
            <li>Promptly notify us of any unauthorized use of your account</li>
            <li>Accept responsibility for all activities that occur under your account</li>
            <li>Be at least 13 years of age to use the platform</li>
          </ul>
        </CardContent>
      </Card>

      {/* Acceptable Use */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <AlertCircle className="h-5 w-5" />
            Acceptable Use
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">
            You agree to use the platform only for lawful purposes and in accordance with 
            these terms. You agree not to:
          </p>
          <ul className="space-y-2 text-muted-foreground list-disc list-inside">
            <li>Use the platform in any way that violates applicable laws or regulations</li>
            <li>Attempt to gain unauthorized access to any part of the platform</li>
            <li>Interfere with or disrupt the platform or servers connected to it</li>
            <li>Share solutions in a way that undermines the learning experience of others</li>
            <li>Use automated systems to access or interact with the platform</li>
            <li>Upload malicious code or content that could harm the platform or other users</li>
          </ul>
        </CardContent>
      </Card>

      {/* Intellectual Property */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Intellectual Property</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            The platform and its original content, features, and functionality are owned by 
            Python OOP Journey and are protected by international copyright, trademark, and 
            other intellectual property laws.
          </p>
          <p>
            You retain ownership of any code you write on the platform. By submitting code, 
            you grant us a license to store and process it for the purpose of providing our 
            services, including running tests and providing feedback.
          </p>
        </CardContent>
      </Card>

      {/* Termination */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Termination</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            We may terminate or suspend your account and access to the platform immediately, 
            without prior notice or liability, for any reason, including if you breach these 
            terms.
          </p>
          <p>
            Upon termination, your right to use the platform will immediately cease. All 
            provisions of these terms which by their nature should survive termination shall 
            survive.
          </p>
        </CardContent>
      </Card>

      {/* Limitation of Liability */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Limitation of Liability</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            In no event shall Python OOP Journey be liable for any indirect, incidental, 
            special, consequential, or punitive damages, including without limitation, loss 
            of profits, data, use, goodwill, or other intangible losses.
          </p>
          <p>
            The platform is provided on an &ldquo;as is&rdquo; and &ldquo;as available&rdquo; basis. We make no 
            warranties, expressed or implied, regarding the platform&apos;s operation or the 
            information, content, or materials included therein.
          </p>
        </CardContent>
      </Card>

      {/* Changes to Terms */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Changes to Terms</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            We reserve the right to modify or replace these terms at any time. If a revision 
            is material, we will provide at least 30 days&apos; notice prior to any new terms 
            taking effect.
          </p>
          <p>
            By continuing to access or use our platform after any revisions become effective, 
            you agree to be bound by the revised terms.
          </p>
        </CardContent>
      </Card>

      {/* Contact */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-lg">Contact Us</CardTitle>
        </CardHeader>
        <CardContent className="text-muted-foreground">
          <p>
            If you have any questions about these Terms of Service, please contact us at{' '}
            <a href="mailto:support@oopjourney.dev" className="text-primary hover:underline">
              support@oopjourney.dev
            </a>.
          </p>
        </CardContent>
      </Card>

      {/* Footer */}
      <div className="text-center text-sm text-muted-foreground">
        <Separator className="mb-6" />
        <p>
          By using Python OOP Journey, you acknowledge that you have read, understood, and 
          agree to be bound by these Terms of Service.
        </p>
        <div className="mt-4 flex items-center justify-center gap-4">
          <Link href="/privacy" className="hover:underline">
            Privacy Policy
          </Link>
          <span>•</span>
          <Link href="/auth/login" className="hover:underline">
            Back to Login
          </Link>
        </div>
      </div>
    </div>
  );
}
