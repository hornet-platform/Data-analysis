from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import time
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


llm = ChatOpenAI(
    model="gpt-3.5-turbo-0125",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)




prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant that uses the provided context to answer the user question",
        ),
        ("human", "{context}"),
        ("human", "{input}"),
    ]
)

chain = prompt | llm


@app.get("/model")
async def stream_response(context: str, user_input: str):
    async def model_response():
        # Simulate processing context and user input
        yield f"Processing context: {context}\n"
        time.sleep(1)  # Simulate processing delay

        yield f"Processing user input: {user_input}\n"
        time.sleep(1)  # Simulate processing delay

        # Simulate response generation
        async for i in chain.astream(
            {
                "context": context,
                "input": user_input,
            }
        ):
            yield i.content

    return StreamingResponse(model_response(), media_type="text/plain")

