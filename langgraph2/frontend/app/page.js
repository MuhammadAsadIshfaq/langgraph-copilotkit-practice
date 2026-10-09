'use client';

import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { DocumentArrowUpIcon } from '@heroicons/react/24/outline';

export default function Home() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [candidateInfo, setCandidateInfo] = useState({
    name: '',
    email: '',
    position: '',
    company_name: '',
    interviewer: '',
    interviewer_email: '',
    interview_location: ''
  });

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      setFile(acceptedFiles[0]);
      setError(null);
    },
    onDropRejected: (rejectedFiles) => {
      setError('Invalid file type. Please upload PDF, DOC, or DOCX files.');
    }
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setCandidateInfo(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const validateForm = () => {
    if (!file) {
      setError('Please upload a resume');
      return false;
    }
    if (!jobDescription || jobDescription.trim().length < 10) {
      setError('Job description is required and must be at least 10 characters long');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateForm()) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);
    formData.append('candidate_info', JSON.stringify(candidateInfo));

    try {
      const response = await axios.post('/api/process-resume', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'An error occurred while processing the resume';
      setError(errorMessage);
      console.error('Error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-center mb-8">Hiring Workflow System</h1>
      
      <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-md p-6">
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full h-32 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
              placeholder="Enter the job description..."
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload Resume
            </label>
            <div
              {...getRootProps()}
              className={`border-2 border-dashed rounded-md p-6 text-center cursor-pointer transition-colors
                ${isDragActive ? 'border-primary bg-blue-50' : 'border-gray-300 hover:border-primary'}`}
            >
              <input {...getInputProps()} />
              <DocumentArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
              <p className="mt-2 text-sm text-gray-600">
                {file ? file.name : 'Drag and drop a resume (PDF, DOC, or DOCX), or click to select'}
              </p>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Candidate Name
              </label>
              <input
                type="text"
                name="name"
                value={candidateInfo.name}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Enter candidate name"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Candidate Email
              </label>
              <input
                type="email"
                name="email"
                value={candidateInfo.email}
                onChange={handleInputChange}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Enter candidate email"
              />
            </div>
          </div>

          {error && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-2 px-4 rounded-md text-white font-medium transition-colors
              ${loading ? 'bg-gray-400 cursor-not-allowed' : 'bg-primary hover:bg-blue-700'}`}
          >
            {loading ? (
              <span className="flex items-center justify-center">
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                Processing...
              </span>
            ) : 'Process Resume'}
          </button>
        </form>

        {result && (
          <div className="mt-8 p-4 bg-gray-50 rounded-md">
            <h2 className="text-xl font-semibold mb-4">Results</h2>
            <div className="space-y-4">
              <div>
                <h3 className="font-medium">Decision:</h3>
                <p className="text-gray-700">{result.final_decision}</p>
              </div>
              {result.screening_result && (
                <div>
                  <h3 className="font-medium">Screening Results:</h3>
                  <ul className="list-disc list-inside text-gray-700">
                    <li>Score: {result.screening_result.overall_score}/100</li>
                    <li>Qualified: {result.screening_result.qualified ? 'Yes' : 'No'}</li>
                    <li>Recommendation: {result.screening_result.recommendation}</li>
                  </ul>
                </div>
              )}
              {result.emails_sent && result.emails_sent.length > 0 && (
                <div>
                  <h3 className="font-medium">Emails Sent:</h3>
                  <ul className="list-disc list-inside text-gray-700">
                    {result.emails_sent.map((email, index) => (
                      <li key={index}>
                        To: {email.recipient} - {email.subject}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
} 