date:11/11/2026
(a)what I learned ?
today I leaned about the basic knowledge of the AI/ML and the Generative AI
and also i learned the scrpit writing to get the response from the api key 
the scrpit is in below
(1)we need to install the python sdk for api key (i.e pip install google-genai)
(2)we need to import the python sdk of the api key (i.e from google import genai)
(3)we need to call the api key (i.e client=genai.Client(apikey="your api key"))
(3)we need to use the variable to store the response of the api key (i.e response=clinet.models.generate_context(model="genai-3.8-flash",content="explain about AI"))
(4)for printing the output we need to use the print (i.e print(("Response:",repr(response.text)))


(b)What did not understand?
the issue of taking to much time for the reponse from the api key

(c)can i generate the images,videos like real gemini chatboot app?

date 11/12/2026
(a)what i learned ?
I learned about the elements of prompt and difference between the output of grow api,gemeni ai,ollama.
(b)what i did not understand?
i didn't get the point of zero shot prompting
(c)for next day question?
when I developed an chatboot app with ollama and deployed it is it used  ollama for other users which I was deployed?

date 12-11-2026
What I learned ?
What i didnot get?
What is the Tommorow next question?
what is our project plan?
Project title: PrepPilot — An Explainable, RAG-Based AI Study and Quiz Assistant Using Open Educational Resources.
Project objective: Build an AI-powered learning platform that converts openly licensed educational materials into study notes, interactive quizzes, question-answering sessions and personalized revision recommendations.
The important part is that Project should not simply generate answers from an LLM's general knowledge. It should retrieve relevant information from educational sources, generate answers grounded in that information, and show students where the answers came from.
my project demonstrates LLM integration, prompt engineering, embeddings, RAG, vector databases, model comparison and AI evaluation.


Module	                             Main functionality
Educational Resource Library	       Browse and select open educational content
AI Study Notes	                     Generate summaries, definitions and revision notes
Source-Grounded AI Tutor	           Ask questions and receive answers with citations
AI Quiz Generator	                   Generate MCQs, true/false and short-answer questions
Answer Evaluation	                   Evaluate responses and explain mistakes
Adaptive Learning Dashboard	         Track weak topics and recommend revision

intailly use the source of python_documentation as the source:https://docs.python.org/3/whatsnew/3.14.html

Component      	      Technology	                Responsibility
Frontend	            (flask/django)
                      React+javascriptScript	    User interface
Backend	              FastAPI	                    Business logic and APIs
AI service	          Gemini / Groq	              Generate responses
Embeddings	          Sentence Transformers	      Convert text to vectors
Vector store	        ChromaDB	                  Semantic retrieval
Relational database	  SQLite	                    Users, quizzes, scores
Document parser	      PyMuPDF, BeautifulSoup	    Extract educational text
Authentication	      JWT	                        User accounts
Analytics	            Recharts	                  Performance dashboard
