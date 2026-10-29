from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using the user's documents.

Rules:
- For greetings and small talk, reply briefly and do not cite anything.
- For other questions, answer from the context below and cite every fact you use inline as [1], [2], using the numbers given. Never write a fact from the context without a citation.
- If the context does not contain the answer, start with "I could not find it in the uploaded documents." You may then add a short answer from your own knowledge, without any citations.
- Be concise and use Markdown (lists, code blocks) where it helps.

Context:
{context}"""

RAG_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)

CONDENSE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Given the chat history and the user's latest message, rewrite the latest message as a "
            "standalone question that can be understood without the history. Do NOT answer it. "
            "If it is already standalone, return it unchanged. Output only the question.",
        ),
        MessagesPlaceholder("history"),
        ("human", "{question}"),
    ]
)
