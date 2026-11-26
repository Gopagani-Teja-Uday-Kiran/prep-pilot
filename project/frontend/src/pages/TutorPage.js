import React, { createElement as h, useState } from "react";
import { askTutor } from "../api/tutorApi.js";

export default function TutorPage() {
  const [question, setQuestion] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submitQuestion(event) {
    event.preventDefault();

    const trimmedQuestion = question.trim();
    if (trimmedQuestion.length < 3) {
      setError("Enter a question with at least 3 characters.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch("/api/tutor/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question: trimmedQuestion }),
      });

      const body = await askTutor(trimmedQuestion);
     

      if (!response.ok) {
        throw new Error(body.detail || `Request failed (${response.status}).`);
      }

      setResult(body);
    } catch (requestError) {
      console.error("Tutor request failed:", requestError);
      setError(
        requestError instanceof Error
          ? requestError.message
          : "The tutor request failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return h(
    "section",
    { className: "tutor-page" },
    h("p", { className: "eyebrow" }, "LEARN WITH SOURCES"),
    h("h1", null, "Ask the Python tutor"),
    h(
      "p",
      { className: "intro" },
      "Ask a Python question. The tutor uses the indexed Python documentation and shows its sources."
    ),
    h(
      "form",
      { className: "question-form", onSubmit: submitQuestion },
      h("label", { htmlFor: "question" }, "Your question"),
      h("textarea", {
        id: "question",
        name: "question",
        rows: 4,
        minLength: 3,
        maxLength: 2000,
        required: true,
        placeholder: "For example: How can I access command-line arguments?",
        value: question,
        onChange: (event) => setQuestion(event.target.value),
      }),
      h(
        "div",
        { className: "form-footer" },
        h("span", { className: "character-count" }, `${question.length}/2000`),
        h(
          "button",
          { type: "submit", disabled: loading },
          loading ? "Searching..." : "Ask tutor"
        )
      )
    ),
    loading
      ? h("p", { className: "status-message", role: "status" }, "Searching the Python documentation...")
      : null,
    error
      ? h("p", { className: "error-message", role: "alert" }, error)
      : null,
    result
      ? h(
          "section",
          {
            className: result.insufficient_evidence
              ? "answer-card insufficient"
              : "answer-card",
            "aria-live": "polite",
          },
          h(
            "h2",
            null,
            result.insufficient_evidence ? "Not enough source evidence" : "Tutor answer"
          ),
          h("p", { className: "answer-text" }, result.answer),
          result.citations?.length
            ? h(
                "div",
                { className: "citations" },
                h("h3", null, "Sources"),
                h(
                  "ul",
                  null,
                  result.citations.map((citation, index) =>
                    h(
                      "li",
                      {
                        key: `${citation.url}-${citation.section}-${index}`,
                      },
                      h(
                        "a",
                        {
                          href: citation.url,
                          target: "_blank",
                          rel: "noreferrer",
                        },
                        citation.title
                      ),
                      h("span", null, ` — ${citation.section}`)
                    )
                  )
                )
              )
            : null
        )
      : null
  );
}