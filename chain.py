# %%
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

agentPrompt = ChatPromptTemplate.from_messages(
    [
        ("user", "{question} '{case}'"),
        MessagesPlaceholder("chat_history", optional=True),
    ]
)

model = ChatOpenAI(temperature=0, model="gpt-4o")


async def chain(question, case):
    """
    Determines if we understand the step of the user.

    Potential interactions with the user is stored in the global_state's human_chat.

    Returns:
    str: The mission of the user.
    """

    chain = agentPrompt | model | StrOutputParser()

    response = chain.ainvoke(
        {
            question: question,
            case: case,
        }
    )

    return str(response)
