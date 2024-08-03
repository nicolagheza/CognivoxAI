from typing import Literal

from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.constants import END, START
from langgraph.graph import MessagesState, StateGraph

from AgentsFactory import AgentsFactory


class State(MessagesState):
    summary: str


class GraphManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GraphManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self.memory = SqliteSaver.from_conn_string(":memory:")
        self._initialized = True

    def create_graph(self):
        graph_builder = StateGraph(State)

        llm = AgentsFactory.create_agent()

        def chatbot(state: State):
            summary = state.get("summary")
            if summary:
                system_message = f"Summary of conversation earlier: {summary}"
                messages = [SystemMessage(content=system_message)] + state["messages"]
            else:
                messages = state["messages"]
            response = llm.invoke({"messages": messages})
            return {"messages": [response]}

        def summarize_conversation(state: State):
            # First, we summarize the conversation
            summary = state.get("summary", "")
            if summary:
                # If a summary already exists, we use a different system prompt
                # to summarize it than if one didn't
                summary_message = (
                    f"This is summary of the conversation to date: {summary}\n\n"
                    "Extend the summary by taking into account the new messages above:"
                )
            else:
                summary_message = "Create a summary of the conversation above:"

            messages = state["messages"] + [HumanMessage(content=summary_message)]
            response = llm.invoke({"messages": messages})
            # We now need to delete messages that we no longer want to show up
            # I will delete all but the last two messages, but you can change this
            delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:-2]]
            return {"summary": response.content, "messages": delete_messages}

        # We now define the logic for determining whether to end or summarize the conversation
        def should_continue(state: State) -> Literal["summarize_conversation", END]:
            """Return the next node to execute."""
            messages = state["messages"]
            # If there are more than six messages, then we summarize the conversation
            if len(messages) > 6:
                return "summarize_conversation"
            # Otherwise we can just end
            return END

        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_conditional_edges(
            # First, we define the start node. We use `conversation`.
            # This means these are the edges taken after the `conversation` node is called.
            "chatbot",
            # Next, we pass in the function that will determine which node is called next.
            should_continue,
        )

        graph_builder.add_node(summarize_conversation)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("summarize_conversation", END)

        return graph_builder.compile(checkpointer=self.memory)
