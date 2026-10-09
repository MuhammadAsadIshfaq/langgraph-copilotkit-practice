import { copilotKitEndpoint } from "@copilotkit/runtime";

export const runtime = "edge";

export async function POST(req) {
  console.log("Received request at /api/copilotkit");
  
  try {
    const response = await copilotKitEndpoint({
      remoteUrl: process.env.REMOTE_ACTION_URL || "http://localhost:8000/copilotkit",
    })(req);
    
    console.log("Response status:", response.status);
    return response;
  } catch (error) {
    console.error("Error in CopilotKit endpoint:", error);
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
