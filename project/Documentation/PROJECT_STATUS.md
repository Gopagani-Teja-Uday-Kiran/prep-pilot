# PrepPilot: Project Status

**Last updated:** 26 November 2026  
**Current stage:** Month 1 — building the backend and first RAG prototype

## Where the project stands

I’ve built the first working version of PrepPilot’s Python tutor. A user can ask a question, the system searches selected Python documentation for relevant material, and then sends that material to an AI model to help form an answer with citations.

This is an important first milestone, but PrepPilot is not a finished application yet. Features such as quizzes, progress tracking, recommendations, and the frontend still need to be built.

## What I’ve completed so far

### OULAD exploration

I explored the Open University Learning Analytics Dataset (OULAD) in a notebook. I examined student outcomes, calculated VLE click totals in batches, and compared final results across groups with different activity levels.

My report describes a relationship between activity and course results. For example, it reports higher withdrawal in the lowest-click group and better outcomes in the highest-click group. This is an association, though—it doesn’t prove that clicking more caused students to do better.

I’ve documented the work in `analytics/reports/ouladreport.md`. The next analytics question I want to explore is whether activity earlier in a course can tell us anything about later outcomes.

### Python tutor and RAG

For the tutor’s initial knowledge source, I chose selected pages from the Python 3.14 Tutorial. I built a pipeline that:

1. Fetches the selected pages and extracts their main article content.
2. Saves the extracted text with details such as its source URL and section.
3. Splits that text into smaller chunks.
4. Embeds the chunks and stores them in ChromaDB.
5. Searches for relevant chunks when a student asks a question.
6. Sends the retrieved evidence to the AI provider and returns an answer with citations.

The tutor tries Groq first and uses Gemini as a fallback if Groq fails. If the search doesn’t find suitable evidence, it responds that it can’t answer reliably rather than guessing.

### Testing so far

The last reported test run passed all four tests. I also ran a small retrieval evaluation with ten answerable questions and five unrelated ones. In that run, all ten answerable questions had a result from the expected page in the top three, and all five unrelated questions returned no results.

That’s encouraging, but the evaluation set is still small. It checks whether the expected page was retrieved; it doesn’t yet prove that every passage, answer, or citation is correct.

A live tutor request also returned an answer with citations. That confirms the end-to-end flow worked for that request, but more testing is needed before relying on it consistently.

## Why the code changed during development

I made several changes because testing exposed issues in the first versions. For example, the original scraper included navigation text, some generated chunks had duplicate IDs, and a few evaluation questions referred to a tutorial page I hadn’t included yet. I also had to adjust a test mock so it returned the same kind of list that the real retriever returns, and update model settings when the configured model names were unavailable.

These iterations helped me find problems by running the code rather than guessing. Going forward, I want to keep changes small, review what changed, and run the relevant tests after each update.

## What I still need to build

The current work is a backend and RAG prototype. I have not yet built the React frontend, login, quiz creation and grading, user progress storage, mistake analysis, or adaptive recommendations. I also haven’t completed deployment.

The EDKT Parquet files are in the workspace, but I have not analyzed or integrated them. OULAD is being used for a separate offline analytics study, not as the Python tutor’s knowledge source. Keeping those roles separate helps the tutor retrieve relevant teaching material and keeps learning-activity data out of its knowledge base.

## What I plan to do next

First, I want to improve confidence in the tutor:

- Add more evaluation questions, including paraphrases and questions the sources cannot answer.
- Check whether retrieval finds the right section or passage, not just the right page.
- Review whether generated answers are actually supported by their citations.
- Add a test showing that a successful Groq response does not trigger Gemini.
- Keep provider calls mocked in automated tests so tests don’t depend on live services or API keys.

After that, I’ll start the quiz feature: generate structured questions from retrieved source material, check that each question and answer is valid, and grade objective answers. Then I can add attempt storage and topic-level progress.

For OULAD, I’d like to explore early engagement separately. I’ll only use clicks recorded up to a defined point when studying later outcomes, so I don’t accidentally use future activity to predict the past.

## How I run the backend

From the repository root, I start the API with:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload