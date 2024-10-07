import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { SuccessResponse } from '@/lib/query';
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from '@/components/ui/sheet';

interface MoreInfoButtonProps {
  // responseData: BackendResponse | null;
  responseData: SuccessResponse;
}

export default function MoreInfoButton({ responseData }: MoreInfoButtonProps) {
  const [showDictionary, setShowDictionary] = useState(false);

  const handleToggle = () => {
    setShowDictionary(!showDictionary);
  };

  return (
    <div>
      <Sheet>
        <SheetTrigger>
          <Button variant='accent' onClick={handleToggle}>
            {showDictionary ? 'Hide' : 'Show full data'}
          </Button>
        </SheetTrigger>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>Complete Data</SheetTitle>
            <SheetDescription>
              {showDictionary && (
                <div className='mt-4 rounded border bg-gray-50 p-4'>
                  <pre className='whitespace-pre-wrap text-sm text-gray-800'>
                    {JSON.stringify(responseData.data)}
                  </pre>
                </div>
              )}
            </SheetDescription>
          </SheetHeader>
        </SheetContent>
      </Sheet>
    </div>
  );
}
