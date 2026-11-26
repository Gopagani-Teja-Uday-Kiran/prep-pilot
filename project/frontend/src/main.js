import React from "react";
import { createRoot } from "react-dom/client";
import App from "./App.js";


const rootElement = document.getElementById("root");

if (!rootElement) {
  throw new Error("Could not find the React root element.");
}

createRoot(rootElement).render(React.createElement(App));