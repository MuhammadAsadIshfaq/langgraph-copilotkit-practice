"use client";

import { useState } from "react";
import { useCopilotReadable, useCopilotAction } from "@copilotkit/react-core";

export default function Home() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  useCopilotReadable({
    description: "Last agent response",
    value: response,
  });

  useCopilotAction({
    name: "sendMessage",
    description: "Send user input to the agent",
    parameters: [{ name: "message", type: "string" }],
    handler: async ({ message }) => {
      const res = await fetch("http://localhost:8000/process-message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await res.json();
      setResponse(data.response);
    },
  });

  return (
    <main style={{ padding: 20 }}>
      <h1>LangGraph + CopilotKit</h1>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type a message"
        style={{ padding: 10, width: "300px", marginRight: 10 }}
      />
      <button
        onClick={async () => {
          const res = await fetch("http://localhost:8000/process-message", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input }),
          });
          const data = await res.json();
          setResponse(data.response);
        }}
      >
        Send
      </button>
      <div style={{ marginTop: 20 }}>
        <strong>Agent:</strong> {response}
      </div>
    </main>
  );
}
