#!/usr/bin/env python3
"""
Simple ReAct Agent
"""

from langchain.agents import AgentExecutor, create_react_agent
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate

from tools import calculator_tool 

LLM = "qwen2.5:7b"

tools = [
    calculator_tool,
    # Add more tools here, e.g.:
    # random_int_tool, etc.
]

# ReAct Prompt Template
# Modify this prompt to change how the agent thinks and acts
# In general, change only the first line to tell the agent what to do, do not change the rest.
PROMPT_TEMPLATE = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""

PROMPT = PromptTemplate.from_template(PROMPT_TEMPLATE)


def create_agent():
    agent = create_react_agent(
        llm=ChatOllama(
        model=LLM,
        temperature=0,
        ),
        tools=tools,
        prompt=PROMPT,
    )

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
    )
    
    return agent_executor


def main():
    print(f"🤖 Agent with Ollama ({LLM})")
    print("=" * 60)
    print("This agent can perform calculations using the calculator tool.")
    print("Type 'exit' or 'quit' to stop.\n")
    
    agent_executor = create_agent()
    
    while True:
        # Get user input
        try:
            query = input("📝 Enter your query: ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['exit', 'quit']:
                print("\n👋 Goodbye!")
                break
            
            print("\n" + "-" * 60)
            
            # Run the agent
            result = agent_executor.invoke({"input": query})
            
            print("-" * 60)
            print(f"✅ Final Answer: {result['output']}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}\n")


if __name__ == "__main__":
    main()

