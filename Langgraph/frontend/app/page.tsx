import { useState } from "react";
import { useCopilotKit } from "@copilotkit/react";
import { useGroq } from "@groq/groq-js";

export default function Home() {
  const [jobDescription, setJobDescription] = useState("");
  const [resumeFile, setResumeFile] = useState<File | null>(null);
  const [screeningResult, setScreeningResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const { copilotKit } = useCopilotKit();
  const { groq } = useGroq();

  const handleResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setResumeFile(file);
    }
  };

  const handleSubmit = async () => {
    if (!resumeFile || !jobDescription) return;

    setLoading(true);
    try {
      const formData = new FormData();
      formData.append("resume", resumeFile);
      formData.append("job_description", jobDescription);

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/upload-resume`, {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      setScreeningResult(result);

      // Use CopilotKit for next steps
      if (result.meets_threshold) {
        const nextSteps = await copilotKit.generate(
          `Based on the screening result: ${JSON.stringify(result)}, suggest next steps for the hiring process.`,
          {
            model: "llama-3.3-70b-versatile",
          }
        );
        console.log("Next steps:", nextSteps);
      }
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl font-bold mb-8 text-center">LangGraph Hiring System</h1>
        
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              className="w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter job description..."
              rows={4}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Upload Resume
            </label>
            <input
              type="file"
              onChange={handleResumeUpload}
              className="w-full p-2 border rounded-md"
              accept=".pdf,.doc,.docx"
            />
          </div>

          <button
            onClick={handleSubmit}
            disabled={loading || !resumeFile || !jobDescription}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Processing..." : "Screen Resume"}
          </button>

          {screeningResult && (
            <div className="mt-8 p-6 bg-gray-50 rounded-lg">
              <h2 className="text-xl font-semibold mb-4">Screening Result</h2>
              <div className="space-y-4">
                <div>
                  <span className="font-medium">Score:</span> {screeningResult.score}
                </div>
                <div>
                  <span className="font-medium">Meets Threshold:</span>{" "}
                  {screeningResult.meets_threshold ? "Yes" : "No"}
                </div>
                <div className="mt-4">
                  <h3 className="font-medium mb-2">Analysis:</h3>
                  <p className="text-gray-700">{screeningResult.analysis}</p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
