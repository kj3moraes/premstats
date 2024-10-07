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
    <Button variant='outline' size='sm' onClick={handleSubmit}>
      <div className='flex flex-row space-x-2'>
        <Lightbulb className='text-muted-foreground' size={16} />
        <p className='text-sm text-muted-foreground'>{text}</p>
      </div>
    </Button>
  );
}
