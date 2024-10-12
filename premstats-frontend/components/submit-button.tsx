import React from 'react';
import { Button } from '@/components/ui/button';

const SubmitButton = ({ onSubmit }: { onSubmit: (e: React.FormEvent) => void }) => {
  return (
    <Button 
      variant="default"
      type="submit" 
      className="flex-shrink-0"
      onClick={onSubmit}
    >
      Submit
    </Button>
  );
};

export default SubmitButton;