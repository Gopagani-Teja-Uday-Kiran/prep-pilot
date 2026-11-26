import React, { createElement as h } from "react";
import { HashRouter, Navigate, Route, Routes } from "react-router-dom";
import TutorPage from "./pages/TutorPage.js";

export default function App() {
  return h(
    HashRouter,
    null,
    h(
      "div",
      { className: "app-shell" },
      h(
        "header",
        { className: "site-header" },
        h("a", { className: "brand", href: "#/tutor" }, "PrepPilot"),
        h("span", { className: "header-label" }, "Python learning assistant")
      ),
      h(
        "main",
        { className: "main-content" },
        h(
          Routes,
          null,
          h(Route, {
            path: "/tutor",
            element: h(TutorPage),
          }),
          h(Route, {
            path: "/",
            element: h(Navigate, { to: "/tutor", replace: true }),
          }),
          h(Route, {
            path: "*",
            element: h(Navigate, { to: "/tutor", replace: true }),
          })
        )
      )
    )
  );
}