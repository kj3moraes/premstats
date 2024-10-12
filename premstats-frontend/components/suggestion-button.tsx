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
      className='h-auto min-h-[2.5rem] w-full max-w-full px-3 py-2'
    >
      <div className='flex w-full items-start space-x-2'>
        <Lightbulb
          className='mt-1 flex-shrink-0 text-muted-foreground'
          size={16}
        />
        <p className='text-wrap text-sm text-muted-foreground'>{text}</p>
      </div>
    </Button>
  );
}
