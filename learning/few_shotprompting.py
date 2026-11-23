
from llm_client import generate_response

examples = """
Example 1:

Question: Which keyword defines a function in Python?

A. function
B. def
C. fun
D. define

Answer: B

Explanation: The def keyword is used to define functions.

Example 2:

Question: Which keyword returns a value from a function?

A. print
B. break
C. return
D. pass

Answer: C

Explanation: The return statement sends a result back to the caller.

Example 3:

Question: Can a Python function accept parameters?

A. Yes
B. No
C. Only two
D. Only strings

Answer: A

Explanation: Functions can accept parameters of different types.
"""

topic = input("Enter topic: ")

prompt = f"""
You are a Python quiz generator.

Follow the exact question format demonstrated below.

{examples}

Now generate 5 new questions about: {topic}

Do not repeat the example questions.
Maintain the same structure.
"""

print(generate_response(prompt))
