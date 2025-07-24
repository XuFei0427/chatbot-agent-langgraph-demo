from typing import List, Dict, Any, Tuple, Optional
from langchain_core.tools import BaseTool
from langchain_core.language_models import BaseLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.messages import AIMessage, HumanMessage

def create_agent_chain(
    llm: BaseLLM,
    tools: List[BaseTool],
    prompt: ChatPromptTemplate
) -> AgentExecutor:
    """
    创建一个具有工具调用能力的Agent执行链
    
    Args:
        llm: 大语言模型
        tools: 可用工具列表
        prompt: 提示模板
        
    Returns:
        配置好的Agent执行器
    """
    # 创建工具调用Agent
    agent = create_tool_calling_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )
    
    # 创建Agent执行器
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,  # 最大工具调用次数
        early_stopping_method="generate"  # 生成回答时停止
    )
    
    return agent_executor

def format_tool_descriptions(tools: List[BaseTool]) -> str:
    """
    格式化工具描述，用于插入到提示中
    
    Args:
        tools: 工具列表
        
    Returns:
        格式化后的工具描述字符串
    """
    formatted_tools = []
    
    for tool in tools:
        tool_desc = f"- {tool.name}: {tool.description}"
        formatted_tools.append(tool_desc)
    
    return "\n".join(formatted_tools) 