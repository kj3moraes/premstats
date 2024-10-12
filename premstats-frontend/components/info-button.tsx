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
  return (
    <div>
      <Sheet>
        <SheetTrigger>
          <Button variant='accent'>
            Show full data
          </Button>
        </SheetTrigger>
        <SheetContent
          side={window.innerWidth >= 768 ? 'right' : 'bottom'}
          className='flex flex-col sm:w-1/2 sm:max-w-none xl:w-1/3 xl:max-w-none'
        >
          <div className='overflow-y-auto'>
            <SheetHeader>
              <SheetTitle>All the data</SheetTitle>
              <SheetDescription>
                <table className='min-w-full table-auto border-collapse'>
                  <thead>
                    <tr>
                      {Object.keys(responseData.data[0] || {}).map((key) => (
                        <th
                          key={key}
                          className='border bg-gray-300 px-4 py-2 text-left'
                        >
                          {key}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {responseData.data.map((item, index) => (
                      <tr
                        key={index}
                        className={
                          index % 2 === 0 ? 'bg-gray-100' : 'bg-gray-200'
                        }
                      >
                        {Object.values(item).map((value, i) => (
                          <td key={i} className='border px-4 py-2'>
                            {value as React.ReactNode}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </SheetDescription>
            </SheetHeader>
          </div>
        </SheetContent>
      </Sheet>
    </div>
  );
}
