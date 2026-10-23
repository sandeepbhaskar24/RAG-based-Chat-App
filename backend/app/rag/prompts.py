from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

SYSTEM_PROMPT = """You are a helpful assistant that answers questions using the user's documents.

Rules:
- Answer ONLY from the context below. If the context does not contain the answer, say you could not find it in the uploaded documents - do not guess.
- When you use information from the context, cite it inline like [1] or [2] using the numbers given.
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
