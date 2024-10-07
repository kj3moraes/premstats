import type { Metadata } from 'next';
import clsx from 'clsx';
import { Noto_Sans } from 'next/font/google';
import { Analytics } from '@vercel/analytics/react';
import Footer from '@/components/footer';
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
        <div className='flex min-h-screen flex-col'>
          <div className='flex flex-1 flex-col justify-center'>{children}</div>
          <div>
            <Footer />
          </div>
        </div>
        <Analytics />
      </body>
    </html>
  );
}
