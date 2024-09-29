import type { Metadata } from 'next';
import clsx from 'clsx';
import { Noto_Sans } from 'next/font/google';
import { Analytics } from '@vercel/analytics/react';
import './globals.css';

const notosans = Noto_Sans({
  variable: '--font-notosans',
  subsets: ['latin'],
  display: 'swap',
  weight: ['200', '400', '800'],
});

export const metadata: Metadata = {
  title: 'Premstats',
  description: 'Querying Premier League match stats.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang='en' className={clsx(notosans.variable)}>
      <body className={`antialiased`}>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
