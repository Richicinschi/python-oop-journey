import { Metadata } from 'next';
import Link from 'next/link';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { ChevronLeft, Shield, Eye, Database, Lock, Cookie, UserCheck, Globe } from 'lucide-react';

export const metadata: Metadata = {
  title: 'Privacy Policy | Python OOP Journey',
  description: 'Privacy Policy and GDPR compliance information for Python OOP Journey',
};

export default function PrivacyPage() {
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
            <Shield className="h-6 w-6 text-primary" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Privacy Policy</h1>
            <p className="text-muted-foreground">
              Last updated: March 2026 • GDPR Compliant
            </p>
          </div>
        </div>
      </div>

      {/* Introduction */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Eye className="h-5 w-5" />
            Overview
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            At Python OOP Journey, we take your privacy seriously. This Privacy Policy 
            explains how we collect, use, store, and protect your personal information when 
            you use our educational platform.
          </p>
          <p>
            We are committed to complying with the General Data Protection Regulation (GDPR) 
            and other applicable privacy laws. By using our platform, you consent to the 
            practices described in this policy.
          </p>
        </CardContent>
      </Card>

      {/* Information We Collect */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Database className="h-5 w-5" />
            Information We Collect
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">
            We collect the following types of information:
          </p>
          
          <div className="space-y-4">
            <div>
              <h4 className="font-medium mb-2">Account Information</h4>
              <ul className="space-y-1 text-muted-foreground list-disc list-inside">
                <li>Email address (via Google OAuth)</li>
                <li>Name and profile picture (optional)</li>
                <li>Account creation date</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium mb-2">Learning Data</h4>
              <ul className="space-y-1 text-muted-foreground list-disc list-inside">
                <li>Problem solutions and code submissions</li>
                <li>Progress tracking data</li>
                <li>Bookmarks and notes</li>
                <li>Time spent on problems</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium mb-2">Technical Data</h4>
              <ul className="space-y-1 text-muted-foreground list-disc list-inside">
                <li>IP address (for security purposes)</li>
                <li>Browser type and version</li>
                <li>Device information</li>
                <li>Usage patterns and analytics</li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* How We Use Your Information */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">How We Use Your Information</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>We use your information to:</p>
          <ul className="space-y-2 list-disc list-inside">
            <li>Provide and maintain the platform&apos;s educational services</li>
            <li>Track your learning progress across devices</li>
            <li>Personalize your learning experience</li>
            <li>Generate insights and recommendations</li>
            <li>Communicate with you about your account and updates</li>
            <li>Improve our platform and develop new features</li>
            <li>Ensure platform security and prevent abuse</li>
          </ul>
        </CardContent>
      </Card>

      {/* Data Storage and Security */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Lock className="h-5 w-5" />
            Data Storage and Security
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            Your data is stored securely using industry-standard encryption and security 
            practices. We implement appropriate technical and organizational measures to 
            protect your personal data against unauthorized access, alteration, disclosure, 
            or destruction.
          </p>
          <p>
            Code submissions and learning progress are stored in our secure database. 
            Local storage is used on your device for offline functionality, which you can 
            clear at any time through your browser settings.
          </p>
        </CardContent>
      </Card>

      {/* Cookies */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Cookie className="h-5 w-5" />
            Cookies and Local Storage
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            We use cookies and local storage to enhance your experience:
          </p>
          <ul className="space-y-2 list-disc list-inside">
            <li><strong>Authentication:</strong> To keep you logged in securely</li>
            <li><strong>Preferences:</strong> To remember your settings and theme</li>
            <li><strong>Progress:</strong> To sync your learning data across devices</li>
            <li><strong>Analytics:</strong> To understand how users interact with the platform</li>
          </ul>
          <p>
            You can control cookies through your browser settings. Note that disabling 
            certain cookies may limit platform functionality.
          </p>
        </CardContent>
      </Card>

      {/* Your Rights (GDPR) */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <UserCheck className="h-5 w-5" />
            Your Rights (GDPR)
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            Under the GDPR, you have the following rights:
          </p>
          <ul className="space-y-2 list-disc list-inside">
            <li><strong>Right to Access:</strong> Request a copy of your personal data</li>
            <li><strong>Right to Rectification:</strong> Correct inaccurate or incomplete data</li>
            <li><strong>Right to Erasure:</strong> Request deletion of your personal data</li>
            <li><strong>Right to Restrict Processing:</strong> Limit how we use your data</li>
            <li><strong>Right to Data Portability:</strong> Export your data in a standard format</li>
            <li><strong>Right to Object:</strong> Object to certain types of processing</li>
          </ul>
          <p>
            To exercise any of these rights, please contact us at{' '}
            <a href="mailto:privacy@oopjourney.dev" className="text-primary hover:underline">
              privacy@oopjourney.dev
            </a>.
          </p>
        </CardContent>
      </Card>

      {/* Data Retention */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Data Retention</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            We retain your personal data only for as long as necessary to provide our 
            services and fulfill the purposes outlined in this policy. You can request 
            deletion of your account and associated data at any time through your profile 
            settings or by contacting us.
          </p>
          <p>
            Anonymized usage data may be retained for analytical purposes indefinitely, 
            but this data cannot be linked back to you.
          </p>
        </CardContent>
      </Card>

      {/* Third-Party Services */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-lg">
            <Globe className="h-5 w-5" />
            Third-Party Services
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            We use the following third-party services to provide our platform:
          </p>
          <ul className="space-y-2 list-disc list-inside">
            <li><strong>Google OAuth:</strong> For secure authentication</li>
            <li><strong>Vercel:</strong> For hosting and deployment</li>
            <li><strong>Analytics:</strong> For understanding platform usage</li>
          </ul>
          <p>
            These services have their own privacy policies and may collect data in 
            accordance with their terms. We only share necessary data with these providers.
          </p>
        </CardContent>
      </Card>

      {/* Changes to Policy */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle className="text-lg">Changes to This Policy</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            We may update this Privacy Policy from time to time. We will notify you of any 
            changes by posting the new policy on this page and updating the &ldquo;last updated&rdquo; 
            date. For significant changes, we may also send you an email notification.
          </p>
          <p>
            We encourage you to review this policy periodically to stay informed about how 
            we protect your information.
          </p>
        </CardContent>
      </Card>

      {/* Contact */}
      <Card className="mb-8">
        <CardHeader>
          <CardTitle className="text-lg">Contact Us</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4 text-muted-foreground">
          <p>
            If you have any questions about this Privacy Policy or our data practices, 
            please contact us:
          </p>
          <ul className="space-y-2 list-disc list-inside">
            <li>
              Email:{' '}
              <a href="mailto:privacy@oopjourney.dev" className="text-primary hover:underline">
                privacy@oopjourney.dev
              </a>
            </li>
            <li>
              Data Protection Officer:{' '}
              <a href="mailto:dpo@oopjourney.dev" className="text-primary hover:underline">
                dpo@oopjourney.dev
              </a>
            </li>
          </ul>
        </CardContent>
      </Card>

      {/* Footer */}
      <div className="text-center text-sm text-muted-foreground">
        <Separator className="mb-6" />
        <p>
          Your privacy is important to us. We are committed to being transparent about our 
          data practices and protecting your personal information.
        </p>
        <div className="mt-4 flex items-center justify-center gap-4">
          <Link href="/terms" className="hover:underline">
            Terms of Service
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
