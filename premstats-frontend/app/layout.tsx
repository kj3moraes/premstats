import type { Metadata } from 'next';
import clsx from 'clsx';
import localFont from 'next/font/local';
import { Noto_Sans } from 'next/font/google';
import { Analytics } from '@vercel/analytics/react';
import './globals.css';

const geistSans = localFont({
  src: './fonts/GeistVF.woff',
  variable: '--font-geist-sans',
  weight: '100 900',
});
const geistMono = localFont({
  src: './fonts/GeistMonoVF.woff',
  variable: '--font-geist-mono',
  weight: '100 900',
});

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
    <html lang='en'  className={clsx(
      geistSans.variable,
      geistMono.variable,
      notosans.variable
    )}>
      <body
        className={`antialiased`}
      >
        {children}
        <Analytics />
      </body>
    </html>
  );
}
