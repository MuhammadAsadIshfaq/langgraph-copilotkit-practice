"use client";

import React, { createContext, useContext, useState } from "react";

const ModelSelectorContext = createContext(undefined);

export const ModelSelectorProvider = ({ children }) => {
  const model =
    typeof window === "undefined"
      ? "openai"
      : new URL(window.location.href).searchParams.get("coAgentsModel") ??
        "openai";

  const [hidden, setHidden] = useState(false);

  const setModel = (model) => {
    const url = new URL(window.location.href);
    url.searchParams.set("coAgentsModel", model);
    window.location.href = url.toString();
  };

  const lgcDeploymentUrl =
    typeof window === "undefined"
      ? null
      : new URL(window.location.href).searchParams.get("lgcDeploymentUrl");

  let agent = "research_agent";
  if (model === "google_genai") {
    agent = "research_agent_google_genai";
  } else if (model === "crewai") {
    agent = "research_agent_crewai";
  }

  return (
    <ModelSelectorContext.Provider
      value={{
        model,
        agent,
        lgcDeploymentUrl,
        hidden,
        setModel,
        setHidden,
      }}
    >
      {children}
    </ModelSelectorContext.Provider>
  );
};

export const useModelSelectorContext = () => {
  const context = useContext(ModelSelectorContext);
  if (context === undefined) {
    throw new Error(
      "useModelSelectorContext must be used within a ModelSelectorProvider"
    );
  }
  return context;
};
