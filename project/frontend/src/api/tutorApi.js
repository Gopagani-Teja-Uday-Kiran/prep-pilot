export async function askTutor(question) {
  const response = await fetch("/api/tutor/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });

  const body = await response.json();

  if (!response.ok) {
    throw new Error(body.detail || `Request failed (${response.status}).`);
  }

  return body;
}