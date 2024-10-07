import React from 'react';

const Footer = () => {
  return (
    <footer className='w-full border-t border-border py-4'>
      <div className='mr-5'>
        <div className='flex justify-end'>
          <p className='text-sm text-muted-foreground'>
            made with ❤️ by{' '}
            <a
              className='underline'
              href='https://itskeane.info'
              target='_blank'
              rel='noreferrer'
            >
              Keane
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
