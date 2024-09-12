from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(
    title="Platform AI Service",
    description="This service provides apis to interact with the platform AI. Currently it only supports a general chatbot, There are yet to come",
)


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


@app.get(
    "/general",
    summary="A simple chatbot to handle question and conversions for platform members",
)
async def stream_response(context: str, user_input: str):
    """
    Ask the model a question based on the context and user input
    """

    async def model_response():
        yield f"Processing context: {context}\n"
        yield f"Processing user input: {user_input}\n"

        # Simulate response generation
        async for i in chain.astream(
            {
                "context": context,
                "input": user_input,
            }
        ):
            yield i.content

    return StreamingResponse(model_response(), media_type="text/plain")  # type: ignore
