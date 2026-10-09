import React from 'react';

interface ProgressProps {
  logs: string[];
}

export function Progress({ logs }: ProgressProps) {
  if (!logs || logs.length === 0) {
    return null;
  }

  return (
    <div className="mt-4 p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-medium mb-2">Progress</h3>
      <div className="space-y-2">
        {logs.map((log, index) => (
          <div key={index} className="text-sm text-gray-600">
            {log}
          </div>
        ))}
      </div>
    </div>
  );
} 