import React, { useState } from 'react';
import { Button } from '@/components/ui/button';

interface MoreInfoButtonProps {
  responseData: string;
}

export default function MoreInfoButton({
  responseData,
}: MoreInfoButtonProps) {
  const [showDictionary, setShowDictionary] = useState(false);

  const handleToggle = () => {
    setShowDictionary(!showDictionary);
  };

  return (
    <div>
      <Button variant='accent' onClick={handleToggle}>
        {showDictionary ? 'Hide' : 'Show full data'}
      </Button>
      {showDictionary && (
        <div className='mt-4 rounded border bg-gray-50 p-4'>
          <h3 className='mb-2 text-lg font-semibold'>Data Dictionary:</h3>
          <pre className='whitespace-pre-wrap text-sm text-gray-800'>
            {JSON.stringify(responseData, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

