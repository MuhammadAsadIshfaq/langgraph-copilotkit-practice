import { CheckCircleIcon, XCircleIcon } from '@heroicons/react/24/outline';

export default function Results({ results }) {
  if (!results) return null;

  const { screening_result, emails_sent, final_decision } = results;

  return (
    <div className="space-y-8">
      {/* Screening Results */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Screening Results</h3>
        
        <div className="flex items-center mb-4">
          {screening_result.qualified ? (
            <CheckCircleIcon className="h-8 w-8 text-green-500 mr-2" />
          ) : (
            <XCircleIcon className="h-8 w-8 text-red-500 mr-2" />
          )}
          <span className={`text-lg font-medium ${screening_result.qualified ? 'text-green-700' : 'text-red-700'}`}>
            {screening_result.qualified ? 'Qualified' : 'Not Qualified'}
          </span>
        </div>

        <div className="mb-4">
          <p className="text-sm font-medium text-gray-700">Overall Score</p>
          <div className="mt-1 w-full bg-gray-200 rounded-full h-2.5">
            <div
              className="bg-blue-600 h-2.5 rounded-full"
              style={{ width: `${screening_result.overall_score}%` }}
            ></div>
          </div>
          <p className="text-sm text-gray-500 mt-1">{screening_result.overall_score}/100</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Strengths</h4>
            <ul className="list-disc list-inside space-y-1">
              {screening_result.strengths.map((strength, index) => (
                <li key={index} className="text-sm text-gray-600">{strength}</li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="text-sm font-medium text-gray-700 mb-2">Gaps</h4>
            <ul className="list-disc list-inside space-y-1">
              {screening_result.gaps.map((gap, index) => (
                <li key={index} className="text-sm text-gray-600">{gap}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-4">
          <h4 className="text-sm font-medium text-gray-700 mb-2">Recommendation</h4>
          <p className="text-sm text-gray-600">{screening_result.recommendation}</p>
        </div>
      </div>

      {/* Emails Sent */}
      {emails_sent && emails_sent.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Emails Sent</h3>
          <div className="space-y-4">
            {emails_sent.map((email, index) => (
              <div key={index} className="border rounded-lg p-4">
                <p className="text-sm font-medium text-gray-700">To: {email.recipient}</p>
                <p className="text-sm font-medium text-gray-700">Subject: {email.subject}</p>
                <div className="mt-2 p-3 bg-gray-50 rounded">
                  <pre className="text-sm text-gray-600 whitespace-pre-wrap">{email.content}</pre>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Final Decision */}
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Final Decision</h3>
        <p className="text-gray-600">{final_decision}</p>
      </div>
    </div>
  );
} 