"use client";

import React, { createContext, useContext, useState } from "react";

interface ModelSelectorContextType {
  model: string;
  agent: string;
  setModel: (model: string) => void;
  setAgent: (agent: string) => void;
  lgcDeploymentUrl?: string;
}

const ModelSelectorContext = createContext<ModelSelectorContextType>({
  model: "gpt-4",
  agent: "todo_agent",
  setModel: () => {},
  setAgent: () => {},
});

export function ModelSelectorProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const [model, setModel] = useState("gpt-4");
  const [agent, setAgent] = useState("todo_agent");

  return (
    <ModelSelectorContext.Provider
      value={{
        model,
        agent,
        setModel,
        setAgent,
      }}
    >
      {children}
    </ModelSelectorContext.Provider>
  );
}

export function useModelSelectorContext() {
  return useContext(ModelSelectorContext);
} 