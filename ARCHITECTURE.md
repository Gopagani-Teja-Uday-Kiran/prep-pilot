# PrepPilot — Architecture and Project Plan
## 1. Project objective

PrepPilot is an AI-powered study and quiz assistant. It supports a complete learning cycle:

**Learn → Test → Detect → Adapt**

- **Learn:** answer student questions and generate notes grounded in approved public educational material.
- **Test:** generate topic-specific quizzes with answer keys and explanations.
- **Detect:** evaluate attempts and identify likely concept or reasoning errors.
- **Adapt:** recommend revision content and targeted practice based on stored topic-level performance.

PrepPilot is not intended to be a generic chatbot. The core technical value is a source-grounded RAG workflow, measurable answer quality, quiz evaluation and explainable adaptive recommendations.

## 2. Scope separation: knowledge corpus vs analytics data

Two data pipelines must remain separate.

### A. Knowledge/RAG corpus

Purpose: provide subject knowledge to the tutor, notes and quiz-generation modules.

Initial candidate content:
- OpenStax textbook chapters whose individual licence permits the intended extraction, embedding, adaptation and public use.
- Think Python, after verifying the applicable licence and attribution requirements.
- Official Python documentation, subject to its documentation licence and terms.

This corpus is document/chunk oriented. Each chunk retains document title, author/publisher, source URL, licence, attribution, retrieval date, chapter/section and page/anchor where available.

### B. Learning analytics datasets

Purpose: investigate learner interactions, assessment outcomes and engagement patterns.

Initial dataset: Open University Learning Analytics Dataset (OULAD), especially `studentVle.csv`, with approximately 10.66 million click records reported for the dataset.

Secondary candidate: EdNet, a much larger TOEIC English-learning interaction dataset. It is not a Python/SQL textbook corpus and its KT variants overlap. Its original CC BY-NC 4.0 licence must be reviewed before any public deployment or redistribution.

Analytics data is maintained as CSV/Parquet files outside the application repository. Pandas processes the files in batches, fastparquet handles Parquet reading/writing where needed, and selected validated records are imported into a separate SQLite analytics database for SQL queries. Analytics data is not automatically embedded into the RAG vector index.

## 3. Proposed technology stack

(1)Frontend===>React, JavaScript ES6+,
(2)Styling===>HTML5, CSS3, normal CSS,
(3)Routing===>React Router DOM
(4)API client===>Axios or Fetch
(5)Backend===>FastAPI (Python) because Designed for API development,Integrates naturally with Python AI/ML and RAG libraries,Automatic API documentation through Swagger UI,Request and response validation using Pydantic,Supports asynchronous endpoints.
(6)API server===>Uvicorn  because it is  FastAPI is an ASGI framework  
(7)Validation===>Pydantic because It prevents your API from blindly accepting incorrect data from the React frontend, external services or other clients. 
(8)ORM/database access===>SQLAlchemy with SQLite (two separate database files: analytics.db and application.db)
(9)Embeddings===>model(all-MiniLM-L6-v2),libarary(Sentence Transformers),Local vector store(ChromaDB) 
(10)LLM===>Gemini and Groq APIs because Compare providers using identical test cases 
(11)PDF extraction===>PyMuPDF because Extract permitted PDF text 
(12)HTML extraction===>BeautifulSoup because Process permitted HTML content
(13)Analytics===>Pandas + fastparquet + SQLite because Pandas processes source files in batches, fastparquet handles Parquet file operations, and SQLite executes SQL queries on selected data imported into analytics.db. SQLite does not query Parquet files directly.
(14)Data preparation===>Pandas + fastparquet for batch cleaning, validation, transformation and CSV/Parquet format conversion 
(15)Charts===>Recharts (web), Matplotlib (analysis) because  User-facing and research visualizations 
(16)Tests===>Pytest, Postman because API and service validation 
(17)Version control===> Git + GitHub because Code, documentation and reproducibility

## 4. Backend selection

**Proposed backend: FastAPI.**

The application is primarily a Python REST API that orchestrates retrieval, embeddings, LLM calls, quiz generation, mistake analysis and analytics queries. FastAPI fits this workload and provides request validation and automatic OpenAPI documentation. Flask and Django were considered.

The selection remains a proposal until a small endpoint, provider call and deployment smoke test are completed.

## 5. Data ingestion and preparation

### Knowledge ingestion

1. Identify a public source and exact resource/version.
2. Verify the licence permits the planned use: access, extraction, text processing, embedding, derivative summaries/questions, storage and public display.
3. Record source metadata and attribution.
4. Download or access the approved file.
5. Extract text using PyMuPDF or an HTML parser.
6. Preserve chapter, section and page metadata.
7. Clean headers, footers, repeated navigation and malformed text.
8. Split text into chunks.
9. Generate embeddings in batches.
10. Store chunk text and metadata in a relational/document store; store vectors in a vector index.
11. Run retrieval tests and inspect failures.

Initial chunking hypothesis: approximately 500 tokens with approximately 80-token overlap. Initial retrieval hypothesis: top-k 4. These are tunable starting points, not proven optimal values.

### Analytics ingestion

1. Obtain the original dataset from its authoritative source.
2. Record download URL, retrieval date, licence and checksum.
3. Inspect archive contents and file sizes.
4. Inspect schema and data types.
5. Profile row counts, nulls, duplicates, key uniqueness, date ranges and category distributions.
6. Convert CSV to Parquet where useful.
7. Partition large Parquet files by a meaningful field only when query patterns justify it.
8. Use Pandas to read and process CSV files in chunks; do not load the complete large dataset into memory.
9. Use fastparquet through Pandas for Parquet reading/writing and selected-column or row-group operations where appropriate.
10. Import only the required, validated records into analytics.db in batches, then use SQLite SQL for filtering, joins, grouping and aggregations. SQLite does not query Parquet files directly.
11. Store analysis outputs and reproducible scripts; do not upload raw or processed multi-GB datasets to the application repository.

## 6. RAG and LLM flow

1. Student sends a question to the React frontend.
2. React calls `POST /api/tutor/ask`.
3. FastAPI validates the request and user identity.
4. The embedding service converts the question to a vector.
5. The retrieval service searches the vector index with subject/topic filters.
6. A relevance/context-sufficiency check decides whether evidence is adequate.
7. If evidence is adequate, the selected LLM receives the question and retrieved context.
8. The model generates an answer with references to retrieved chunk IDs.
9. The backend maps chunk IDs to source titles and page/section references.
10. The backend returns answer, citations, model metadata and a reliability/insufficient-context state.

The model must not fabricate citations. Retrieved content is untrusted data, not instructions. Empty or weak retrieval should produce an explicit insufficient-evidence response.

## 7. Quiz generation and evaluation flow

1. Student selects subject, topic, difficulty, question type and question count.
2. Backend retrieves relevant approved educational context.
3. LLM generates structured questions with options where applicable, expected answer, explanation and source chunk IDs.
4. Backend validates schema, option count, answer key and source references.
5. Quiz is stored and returned to React.
6. Student submits answers.
7. Backend evaluates objective questions deterministically where possible.
8. Short answers use a rubric/reference answer and may use an LLM-assisted evaluation; uncertain cases are flagged rather than treated as perfectly objective.
9. Attempt, responses, score, topic and difficulty are stored.
10. Results feed the mistake analyzer and adaptive-learning engine.

## 8. Learn → Test → Detect → Adapt

### Learn
- AI Tutor and Study Notes retrieve content from the approved knowledge corpus.
- Answers and notes retain citations.

### Test
- Quiz generation uses retrieved topic content.
- Store question IDs, source IDs, difficulty and expected answers.

### Detect
- Compare student responses with expected answers/rubrics.
- Classify likely errors: concept misunderstanding, incorrect condition, logic error, syntax error, off-by-one, formula or terminology.
- Error categories are probabilistic suggestions and should show uncertainty.

### Adapt
- Compute topic accuracy and recent performance.
- Start with transparent rules, not a complex ML model.
- Example initial rules: below 50% → revisit prerequisites and easy practice; 50–75% → targeted practice; above 75% across multiple attempts → consider harder questions or next topic.
- Thresholds are configurable hypotheses and must be evaluated.
- Store the recommendation reason so it is explainable.

## 9. Main React screens

1. Login / Register
2. Dashboard
3. AI Tutor
4. Study Notes
5. Quiz Center
6. Quiz Attempt
7. Quiz Results / Mistake Analyzer
8. My Progress
9. Adaptive Learning
10. Resource Library
11. Settings

The UI must include loading, empty, validation, error and insufficient-context states. React communicates only with the backend; provider API keys are never placed in browser code.

## 10. Proposed API routes

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/subjects`
- `GET /api/subjects/{subject_id}/topics`
- `GET /api/resources`
- `POST /api/tutor/ask`
- `POST /api/study/notes`
- `POST /api/quizzes`
- `POST /api/quizzes/{quiz_id}/submit`
- `GET /api/quizzes/history`
- `GET /api/analytics/progress`
- `GET /api/analytics/weak-topics`
- `GET /api/learning/recommendations`
- `GET /health`

## 11. Storage and scale design

- Do not store public source datasets in Git history.
- Keep source references, metadata, checksums, schema summaries and ingestion scripts in Git.
- Keep raw and processed analytics files outside the application repository.
- Use Pandas chunk-based processing and fastparquet for Parquet file operations; import selected validated records into a separate SQLite analytics database for SQL queries.
- SQLite queries imported database tables; it does not execute SQL directly against external Parquet files.
- Do not load tens of millions of rows into Pandas memory at once.
- Keep the RAG knowledge corpus separate from student interaction analytics.
- Store only application operational records (users, quizzes, attempts and progress) in application.db (SQLite).
- Keep selected public dataset records used for SQL analysis in a separate analytics.db (SQLite); never mix public dataset identities with real PrepPilot user identities.
- Store embeddings in a dedicated vector index, not as large JSON blobs in ordinary relational rows.
- Ingestion and re-indexing should be batch/offline jobs, not long synchronous HTTP requests on a free web service.

## 12. Deployment proposal

Proposed first public demo:
- React production build → Render Static Site.
- FastAPI → Render Free Web Service.
- Application operational data → SQLite in persistent storage, or a hosted SQLite-compatible service such as Turso only after validating the Python client, SQLAlchemy integration, persistence, limits and pricing. Do not use an ephemeral filesystem for the live SQLite database.
- Dataset analytics database → keep analytics.db and large CSV/Parquet files in the offline research workspace; do not deploy the bulk analytics database with the free web application.
- Vector index → separate persistent vector service, after a free-tier proof-of-concept and licence review.
- LLM calls → Gemini/Groq from the backend using server-side environment secrets.
- Large analytics files and analytics.db → local/offline research workspace or permitted external dataset hosting; not the free application server.

Why Render for the frontend and Python API: it supports static sites and Python web services, and one provider can simplify deployment and troubleshooting. However, the free web service has ephemeral local storage, so a SQLite database stored on its local filesystem will not provide reliable persistence across restarts/redeploys. Use a genuinely persistent database service or a hosting plan with a persistent disk; verify current plan limits before deployment. This is a demo environment, not a production guarantee.

Vercel is a static React hosting alternative, but check the current Hobby plan terms and limits before using it. Its Python Functions are serverless with execution and bundle limits; it is less suitable as the primary long-running RAG/API service. It can be used for the React frontend only if the project use is within the applicable plan terms.

A hosted SQLite-compatible service such as Turso may be evaluated for the live application database if local SQLite persistence is not available on the selected host. Validate the current Python client, SQLAlchemy integration, transaction behaviour, limits and pricing before selecting it. It does not replace Parquet file storage, the offline analytics workflow or a vector database.

## 13. Security and reliability

- API keys only in backend environment variables.
- `.env` excluded from Git; provide `.env.example`.
- Password hashing and authentication.
- Per-user data isolation and authorization.
- Upload type/size validation.
- CORS allowlist for deployed frontend.
- Prompt-injection handling for retrieved documents.
- Provider timeout, rate-limit and error handling.
- Avoid returning stack traces or secrets.
- Record external model-provider disclosure in privacy notice.
- Retain licence and attribution metadata for all content.


## 14. Acceptance criteria

- Public URL opens the React application.
- React can call the deployed FastAPI API.
- Student can ask a question and receive a source-grounded answer or an insufficient-context response.
- Student can generate and attempt a quiz.
- Quiz results are persisted and used to calculate topic performance.
- Mistake analysis and recommendation include an explanation of their basis.
- At least 50 evaluation questions have expected answers and source references.
- Retrieval relevance, answer correctness, citation accuracy, quiz correctness, latency and provider failures are measured.
- Deployment limitations and data licences are documented.
