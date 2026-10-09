"use client";

import { useState, useEffect } from "react";
import { CopilotKit } from "@copilotkit/react-core";
import { CopilotSidebar } from "@copilotkit/react-ui";
import axios from "axios";

interface Candidate {
  id: string;
  name: string;
  email: string;
  position: string;
}

interface Interview {
  id: string;
  candidate_id: string;
  date: string;
  interviewer: string;
}

export default function Home() {
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [interviews, setInterviews] = useState<Interview[]>([]);
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  useEffect(() => {
    fetchCandidates();
    fetchInterviews();
  }, []);

  const fetchCandidates = async () => {
    try {
      const response = await axios.get("http://localhost:8000/candidates");
      setCandidates(response.data.candidates);
    } catch (error) {
      console.error("Error fetching candidates:", error);
    }
  };

  const fetchInterviews = async () => {
    try {
      const response = await axios.get("http://localhost:8000/interviews");
      setInterviews(response.data.interviews);
    } catch (error) {
      console.error("Error fetching interviews:", error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/chat", {
        content: message,
      });
      setResponse(response.data.response);
      setMessage("");
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <CopilotKit
      apiKey={process.env.NEXT_PUBLIC_COPILOT_API_KEY}
      baseURL="http://localhost:8000"
    >
      <div className="min-h-screen bg-gray-100">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold mb-8">HR Assistant</h1>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Chat Interface */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-semibold mb-4">Chat with HR Assistant</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <textarea
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  className="w-full p-2 border rounded"
                  rows={4}
                  placeholder="Ask about candidates, interviews, or HR policies..."
                />
                <button
                  type="submit"
                  className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                >
                  Send
                </button>
              </form>
              {response && (
                <div className="mt-4 p-4 bg-gray-50 rounded">
                  <p className="whitespace-pre-wrap">{response}</p>
                </div>
              )}
            </div>

            {/* Candidates List */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-semibold mb-4">Candidates</h2>
              <div className="space-y-4">
                {candidates.map((candidate) => (
                  <div key={candidate.id} className="border p-4 rounded">
                    <h3 className="font-semibold">{candidate.name}</h3>
                    <p className="text-gray-600">{candidate.email}</p>
                    <p className="text-gray-600">{candidate.position}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Interviews List */}
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-2xl font-semibold mb-4">Interviews</h2>
              <div className="space-y-4">
                {interviews.map((interview) => (
                  <div key={interview.id} className="border p-4 rounded">
                    <h3 className="font-semibold">
                      {candidates.find((c) => c.id === interview.candidate_id)?.name}
                    </h3>
                    <p className="text-gray-600">Date: {interview.date}</p>
                    <p className="text-gray-600">Interviewer: {interview.interviewer}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
      <CopilotSidebar />
    </CopilotKit>
  );
} 