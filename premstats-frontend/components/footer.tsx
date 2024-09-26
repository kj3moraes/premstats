import React from 'react';

const Footer = () => {
  return (
    <footer className="w-full py-4 bg-background border-t border-border">
      <div className="container mx-auto">
        <div className="flex justify-end">
          <p className="text-sm text-muted-foreground">
            made with ❤️ by{" "} <a href="https://itskeane.me" target="_blank" rel="noreferrer">Keane</a> 
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;