'use client';
import { Input } from '@/components/ui/input';
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert';
import React, { useState } from 'react';
import { Trophy } from 'lucide-react';
import { query_backend } from '@/lib/query';
import { Toaster } from '@/components/ui/toaster';
import { useToast } from '@/hooks/use-toast';

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
        description: (error as Error).message
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
        <div className='mb-8 flex flex-col items-center space-y-2 md:mb-0 md:w-1/2 md:items-start'>
          <div className='flex flex-row justify-center space-x-4'>
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
          <div>
            <Alert className='w-full max-w-md'>
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
          {isLoading && <p>Loading...</p>}
        </div>
      </div>
      <Toaster />
    </div>
  );
}
