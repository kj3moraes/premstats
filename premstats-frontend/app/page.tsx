'use client';
import { Input } from '@/components/ui/input';
import React, { useState } from 'react';
import { FaFutbol } from 'react-icons/fa';
import { query_backend } from '@/lib/query';
import { Toaster } from '@/components/ui/toaster';
import { useToast } from '@/hooks/use-toast';
import type { BackendResponse, SuccessResponse } from '@/lib/query';
import SuggestionButton from '@/components/suggestion-button';
import SubmitButton from '@/components/submit-button';
import MoreInfoButton from '@/components/info-button';
import ReactMarkdown from 'react-markdown';
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from '@/components/ui/accordion';

export default function Home() {
  const [response, setResponse] = useState<BackendResponse | null>(null);
  const [query, setQuery] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [queryHistory, setQueryHistory] = useState<string[]>([]);
  const { toast } = useToast();

  const handleQuery = async (queryText: string) => {
    setIsLoading(true);
    setResponse(null);
    setQuery(queryText);

    console.log('Querying backend with:', queryText);
    try {
      const response = await query_backend(queryText);
      setResponse(response);
      updateQueryHistory(queryText);
    } catch (error) {
      console.error('Error querying backend:', error);
      toast({
        variant: 'destructive',
        title: 'Error!',
        description: (error as Error).message,
      });
      setResponse(null);
    } finally {
      setIsLoading(false);
    }
  };

  const updateQueryHistory = (newQuery: string) => {
    const updatedHistory = [newQuery, ...queryHistory.slice(0, 9)];
    setQueryHistory(updatedHistory);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;
    await handleQuery(query);
    setQuery('');
  };

  return (
    <div className='flex items-center justify-center bg-background p-4 md:p-8'>
      <div className='flex w-full max-w-6xl flex-col md:flex-row md:items-start md:justify-between'>
        {/* Left Side */}
        <div className='mb-8 flex flex-col items-center gap-2 md:mb-0 md:w-1/2 md:items-start'>
          <div className='flex flex-row items-center justify-center gap-4'>
            <FaFutbol size={40} />
            <h1 className='mb-4 text-center md:text-left'>premstats.xyz</h1>
          </div>
          <form onSubmit={handleSubmit} className='w-full max-w-md'>
            <div className='mb-2 flex'>
              <Input
                type='text'
                placeholder='Ask about any match or team stats...'
                className='mr-2 flex-grow'
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <SubmitButton onSubmit={handleSubmit} />
            </div>
            <p className='mt-2 text-center text-sm text-muted-foreground md:text-left'>
              You can ask about any Premier League season up to but not
              including the current season.
            </p>
          </form>
          <div className='flex w-full max-w-md flex-col gap-2'>
            <SuggestionButton
              text='What seasons has Norwich played in'
              onQuery={handleQuery}
            />
            <SuggestionButton
              text='Matches that Mike Dean refereed in 18/19 season'
              onQuery={handleQuery}
            />
            <SuggestionButton
              text='Betting odds for Liverpool vs ManU 22/23 away game'
              onQuery={handleQuery}
            />
          </div>
          <div>
          </div>
          {/* Query History Accordion */}
          {queryHistory.length > 0 && (
            <Accordion
              type='single'
              collapsible
              className='mt-4 w-full max-w-md'
            >
              <AccordionItem value='item-1'>
                <AccordionTrigger className='text-xl font-semibold'>
                  Previous Queries
                </AccordionTrigger>
                <AccordionContent>
                  <ul className='space-y-2'>
                    {queryHistory.map((historyQuery, index) => (
                      <li
                        key={index}
                        className='cursor-pointer hover:bg-accent'
                        onClick={() => handleQuery(historyQuery)}
                      >
                        {historyQuery}
                      </li>
                    ))}
                  </ul>
                </AccordionContent>
              </AccordionItem>
            </Accordion>
          )}
        </div>
        {/* Right side */}
        <div className='rounded-lg p-4 md:w-1/2'>
          {isLoading ? (
            <div className='flex items-center justify-center'>
              <FaFutbol className='animate-big-bounce text-4xl text-primary' />
            </div>
          ) : (
            response && (
              <>
                <div className='space-y-2'>
                  <ReactMarkdown>
                    {(response as SuccessResponse).message}
                  </ReactMarkdown>
                  <MoreInfoButton responseData={response as SuccessResponse} />
                </div>
              </>
            )
          )}
        </div>
      </div>
      <Toaster />
    </div>
  );
}
