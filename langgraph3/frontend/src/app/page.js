'use client';

import { useState } from 'react';
import { useCopilotKit } from '@copilotkit/react-core';
import ResumeUpload from '../components/ResumeUpload';
import CandidateForm from '../components/CandidateForm';
import Results from '../components/Results';
import ChatAssistant from '../components/ChatAssistant';

export default function Home() {
  const { copilotKit } = useCopilotKit();
  const [selectedFile, setSelectedFile] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    position: '',
    job_description: '',
    company_name: '',
    interviewer: '',
    interviewer_email: '',
    interview_location: ''
  });
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [currentStep, setCurrentStep] = useState('');
  const [processingStatus, setProcessingStatus] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setCurrentStep('');
    setProcessingStatus('');

    const formDataToSend = new FormData();
    formDataToSend.append('file', selectedFile);
    Object.keys(formData).forEach(key => {
      formDataToSend.append(key, formData[key]);
    });

    try {
      console.log('Sending request to backend...');
      const response = await fetch('http://localhost:8000/process-resume', {
        method: 'POST',
        body: formDataToSend,
        headers: {
          'Accept': 'text/event-stream',
        },
      });

      if (!response.ok) {
        const errorText = await response.text();
        console.error('Server response:', errorText);
        throw new Error(`Failed to process resume: ${errorText}`);
      }

      console.log('Response received, starting to read stream...');
      
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { value, done } = await reader.read();
        
        if (done) {
          console.log('Stream complete');
          if (buffer.trim()) {
            console.log('Processing remaining buffer:', buffer);
            processBuffer(buffer);
          }
          break;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.trim() === '') continue;
          console.log('Processing line:', line);
          processLine(line);
        }
      }
    } catch (error) {
      console.error('Error:', error);
      setError(error.message || 'An error occurred while processing the resume');
      setLoading(false);
    }
  };

  const processLine = (line) => {
    if (line.startsWith('data: ')) {
      const data = line.slice(6);
      console.log('Processing data:', data);
      
      if (data === '[DONE]') {
        console.log('Processing complete');
        setLoading(false);
        return;
      }

      try {
        const parsedData = JSON.parse(data);
        console.log('Parsed data:', parsedData);
        
        if (parsedData.next_step) {
          console.log('Updating step to:', parsedData.next_step);
          setCurrentStep(parsedData.next_step);
          setProcessingStatus(`Processing ${parsedData.next_step}...`);
        }

        if (parsedData.screening_result) {
          console.log('Updating results with:', parsedData.screening_result);
          setResults(parsedData);
        }

        if (parsedData.status) {
          console.log('Status update:', parsedData.status);
          if (parsedData.message) {
            setProcessingStatus(parsedData.message);
          }
        }

        if (parsedData.error) {
          console.error('Error in data:', parsedData.error);
          throw new Error(parsedData.error);
        }
      } catch (e) {
        console.error('Error parsing SSE data:', e);
        setError('Error processing server response');
      }
    }
  };

  const processBuffer = (buffer) => {
    const lines = buffer.split('\n');
    for (const line of lines) {
      if (line.trim()) {
        processLine(line);
      }
    }
  };

  return (
    <main className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow sm:rounded-lg">
            <div className="px-4 py-5 sm:p-6">
              <h1 className="text-2xl font-semibold text-gray-900 mb-6">
                Automated Hiring System
              </h1>

              {!results ? (
                <form onSubmit={handleSubmit} className="space-y-6">
                  <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                    <div>
                      <ResumeUpload
                        onFileSelect={setSelectedFile}
                        selectedFile={selectedFile}
                      />
                    </div>
                    <div>
                      <CandidateForm
                        formData={formData}
                        setFormData={setFormData}
                      />
                    </div>
                  </div>

                  {error && (
                    <div className="rounded-md bg-red-50 p-4">
                      <div className="flex">
                        <div className="ml-3">
                          <h3 className="text-sm font-medium text-red-800">
                            Error
                          </h3>
                          <div className="mt-2 text-sm text-red-700">
                            <p>{error}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {loading && (
                    <div className="rounded-md bg-blue-50 p-4">
                      <div className="flex">
                        <div className="ml-3">
                          <h3 className="text-sm font-medium text-blue-800">
                            Processing
                          </h3>
                          <div className="mt-2 text-sm text-blue-700">
                            <p>{processingStatus || 'Processing your request...'}</p>
                            {currentStep && (
                              <p className="mt-1">Current step: {currentStep}</p>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="flex justify-end">
                    <button
                      type="submit"
                      disabled={loading || !selectedFile}
                      className={`inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white ${
                        loading || !selectedFile
                          ? 'bg-gray-400 cursor-not-allowed'
                          : 'bg-blue-600 hover:bg-blue-700'
                      } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
                    >
                      {loading ? 'Processing...' : 'Submit'}
                    </button>
                  </div>
                </form>
              ) : (
                <div>
                  <Results results={results} />
                  <div className="mt-6">
                    <button
                      onClick={() => {
                        setResults(null);
                        setSelectedFile(null);
                        setFormData({
                          name: '',
                          email: '',
                          position: '',
                          job_description: '',
                          company_name: '',
                          interviewer: '',
                          interviewer_email: '',
                          interview_location: ''
                        });
                      }}
                      className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    >
                      Process Another Resume
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
      <ChatAssistant />
    </main>
  );
}
