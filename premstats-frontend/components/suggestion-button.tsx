import React from 'react';
import { Button } from '@/components/ui/button';
import { Lightbulb } from 'lucide-react';

type SuggestionButtonProps = {
  text: string;
  onQuery: (query: string) => void;
};

export default function SuggestionButton({
  text,
  onQuery,
}: SuggestionButtonProps) {
  const handleSubmit = () => {
    onQuery(text);
  };

  return (
    <Button 
      variant='outline' 
      size='sm' 
      onClick={handleSubmit}
      className="h-auto min-h-[2.5rem] w-full max-w-full py-2 px-3"
    >
      <div className='flex items-start space-x-2 w-full'>
        <Lightbulb className='text-muted-foreground flex-shrink-0 mt-1' size={16} />
        <p className='text-sm text-wrap text-muted-foreground'>{text}</p>
      </div>
    </Button>
  );
}