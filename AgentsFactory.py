import operator
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_together import ChatTogether


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    sender: str


class AgentsFactory:

    @staticmethod
    def create_agent():
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are a helpful assistant named Cognivox. Answer all questions to the best of your ability. 
                    You are allowed to use emojis when needed."""
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        chat = ChatTogether(
            model="meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo"
        )

        chain = prompt | chat

        return chain
