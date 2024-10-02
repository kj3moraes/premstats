import { Button } from '@/components/ui/button';
import { Lightbulb } from 'lucide-react';
import { query_backend } from '@/lib/query';

type SuggestionButtonProps = {
  text: string;
};

export default function SuggestionButton({ text }: SuggestionButtonProps) {
  const handleSubmit = () => {
    query_backend(text);
  };

  return (
    <Button variant='outline' size='sm' onClick={handleSubmit}>
      <div className='flex flex-row space-x-2'>
        <Lightbulb className='text-muted-foreground' size={16} />
        <p className='text-sm text-muted-foreground'>{text}</p>
      </div>
    </Button>
  );
}
