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
        <SheetContent
          side={window.innerWidth >= 768 ? 'right' : 'bottom'}
          className='flex flex-col'
        >
          <div className='overflow-auto'>
            <SheetHeader>
              <SheetTitle>All the data</SheetTitle>
              <SheetDescription>
                    <pre className='whitespace-pre-wrap text-sm text-gray-800'>
                      {JSON.stringify(responseData.data)}
                    </pre>
              </SheetDescription>
            </SheetHeader>
          </div>
        </SheetContent>
      </Sheet>
    </div>
  );
}
