import React from 'react';

const Footer = () => {
  return (
    <footer className='w-full border-t border-border bg-background py-4'>
      <div className='container mx-auto'>
        <div className='flex justify-end'>
          <p className='text-sm text-muted-foreground'>
            made with ❤️ by{' '}
            <a href='https://itskeane.info' target='_blank' rel='noreferrer'>
              Keane
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
