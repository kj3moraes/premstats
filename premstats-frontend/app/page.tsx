'use client';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import React, { useState } from 'react';
import { Trophy } from 'lucide-react';
import { query_backend } from '@/lib/query';
import { Toaster } from '@/components/ui/toaster';
import { useToast } from '@/hooks/use-toast';
import SuggestionButton from '@/components/suggestion-button';

export default function Home() {
  const [response, setResponse] = useState<string>('');
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    // Reset state
    setIsLoading(true);
    setResponse('');

    // Query backend
    console.log('Querying backend with:', query);
    try {
      const response = await query_backend(query);
      setResponse(response);
    } catch (error) {
      console.error('Error querying backend:', error);
      toast({
        variant: 'destructive',
        title: 'Error!',
        description: (error as Error).message,
      });
      setResponse('');
    } finally {
      setIsLoading(false);
      setQuery('');
    }
  };

  return (
    <div className='flex min-h-screen items-center justify-center bg-background p-4 md:p-8'>
      <div className='flex w-full max-w-6xl flex-col md:flex-row md:items-center md:justify-between'>
        {/* Left Side */}
        <div className='mb-8 flex flex-col items-center gap-2 md:mb-0 md:w-1/2 md:items-start'>
          <div className='flex flex-row items-center justify-center'>
            <Trophy size={48} />
            <h1 className='mb-4 text-center md:text-left'>premstats.xyz</h1>
          </div>
          <form onSubmit={handleSubmit} className='w-full max-w-md'>
            <Input
              type='text'
              placeholder='Ask about any match or team stats...'
              className='mb-2 w-full'
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <p className='mt-2 text-center text-sm text-muted-foreground md:text-left'>
              You can ask about any Premier League season up to but not
              including the current season.
            </p>
          </form>
          <div className='grid w-full max-w-md grid-cols-2 gap-2'>
            <SuggestionButton text='Seasons QPR played in' />
            <SuggestionButton text='Matches with > 6 goals' />
          </div>
          <div className='flex w-full max-w-md flex-col gap-2'>
            <SuggestionButton text='Matches that Mike Dean refereed in 19/18 season' />
            <SuggestionButton text='betting odds for Liverpool vs ManU 22/23 away game' />
          </div>
          <div>
            <Alert variant='highlight' className='w-full max-w-md'>
              <AlertTitle className='text-lg font-semibold'>
                Heads up!
              </AlertTitle>
              <AlertDescription>
                This site is in beta mode and may not be fully functional.
                Please report any issues to the developer.
              </AlertDescription>
            </Alert>
          </div>
        </div>

        {/* Right side */}
        <div className='rounded-lg p-4 md:w-1/2'>
          {response && <p>{response}</p>}
          {isLoading && (
            <div className='flex items-center justify-center'>
              <div className='h-8 w-8 animate-spin rounded-full border-b-2 border-t-2 border-gray-900'></div>
            </div>
          )}
        </div>
      </div>
      <Toaster />
    </div>
  );
}
