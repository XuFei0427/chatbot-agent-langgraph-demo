from typing import Dict, Any, List, Tuple, Annotated, TypedDict, Union
from langchain_core.tools import BaseTool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models import BaseLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END
import json
import re
import uuid
from enum import Enum
import logging

# 设置日志
logger = logging.getLogger("langgraph_agent")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)  # 默认INFO级别

# 定义Agent状态类型
class AgentState(TypedDict):
    """Agent的状态"""
    messages: List[Union[HumanMessage, AIMessage, SystemMessage]]  # 消息历史
    tool_calls: List[Dict[str, Any]]  # 工具调用
    tool_results: List[Dict[str, Any]]  # 工具调用结果

# 决策枚举
class Decision(str, Enum):
    TOOL = "tool"  # 使用工具
    RESPOND = "respond"  # 直接回复

def extract_tool_use(text: str) -> Dict[str, Any]:
    """从文本中提取工具使用信息"""
    # 断点提示: 可以在此处设置断点检查模型输出文本
    # breakpoint()
    
    # 首先检查是否有"行动:"部分
    action_match = re.search(r"行动:(.*?)(?:行动结果:|回答:)", text, re.DOTALL)
    if not action_match:
        return {}
    
    action_text = action_match.group(1).strip()
    
    # 尝试提取工具名称
    tool_name_match = re.search(r"使用工具:\s*(\w+)", action_text, re.DOTALL)
    if not tool_name_match:
        return {}
    
    tool_name = tool_name_match.group(1).strip()
    
    # 尝试提取参数
    params_match = re.search(r"参数:(.*?)(?:$|行动结果:|回答:)", action_text, re.DOTALL)
    params = {}
    
    if params_match:
        params_text = params_match.group(1).strip()
        
        # 尝试提取键值对格式的参数
        param_pairs = re.findall(r"(\w+):\s*([^,\n]+)", params_text)
        for key, value in param_pairs:
            params[key.strip()] = value.strip()
        
        # 如果上面的方法没有提取到参数，尝试解析JSON
        if not params:
            try:
                json_match = re.search(r"\{(.*)\}", params_text, re.DOTALL)
                if json_match:
                    json_str = "{" + json_match.group(1) + "}"
                    params = json.loads(json_str)
            except:
                pass
    
    # 断点提示: 可以在此处设置断点检查提取的工具信息
    # breakpoint()
    
    result = {
        "name": tool_name,
        "params": params
    }
    
    # 打印提取的工具信息（调试用）
    print(f"提取的工具调用: {result}")
    
    return result

class LangGraphAgent:
    """基于LangGraph实现的Agent"""
    
    def __init__(
        self,
        llm: BaseLLM,
        tools: List[BaseTool],
        prompt_template: ChatPromptTemplate,
        verbose: bool = False
    ):
        """
        初始化LangGraph Agent
        
        Args:
            llm: 大语言模型
            tools: 工具列表
            prompt_template: 提示模板
            verbose: 是否显示详细日志
        """
        # 断点提示: 可以在此处设置断点检查初始化参数
        # breakpoint()
        
        self.llm = llm
        self.tools = tools
        self.prompt = prompt_template
        self.tool_map = {tool.name: tool for tool in tools}
        
        # 设置日志级别
        if verbose:
            logger.setLevel(logging.DEBUG)
            logger.debug("启用详细日志模式")
        
        # 初始化图状态
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """构建Agent状态图"""
        # 断点提示: 可以在此处设置断点检查图的构建过程
        # breakpoint()
        
        # 创建状态图
        graph = StateGraph(AgentState)
        
        # 添加节点
        graph.add_node("agent", self._agent_node)
        graph.add_node("action", self._action_node)
        graph.add_node("process_tool", self._process_tool_node)
        
        # 定义路由函数
        def route(state: AgentState) -> str:
            """决定下一步操作"""
            # 断点提示: 可以在此处设置断点检查路由决策过程
            # breakpoint()
            
            messages = state["messages"]
            last_message = messages[-1]
            
            # 提取工具使用信息
            tool_info = extract_tool_use(last_message.content)
            
            if tool_info and tool_info.get("name") in self.tool_map:
                # 需要使用工具
                state["tool_calls"] = [tool_info]
                logger.debug(f"路由: 检测到工具调用 -> {tool_info['name']}")
                return "action"
            else:
                # 直接回复
                logger.debug("路由: 直接回复，无工具调用")
                return "end"
        
        # 添加边和逻辑
        graph.add_conditional_edges(
            "agent",
            route,
            {
                "action": "action",
                "end": END
            }
        )
        graph.add_edge("action", "process_tool")
        graph.add_edge("process_tool", "agent")
        
        # 设置入口节点
        graph.set_entry_point("agent")
        
        logger.debug("状态图构建完成")

        # 1: 逐行注释
        # 画出状态图结构，便于理解节点和流程
        try:
            import graphviz
            dot = graphviz.Digraph(comment="Agent StateGraph")
            dot.node("agent", "Agent节点")
            dot.node("action", "Action节点")
            dot.node("process_tool", "ProcessTool节点")
            dot.node("end", "END(结束)")

            dot.edge("agent", "action", label="需要工具")
            dot.edge("agent", "end", label="直接回复")
            dot.edge("action", "process_tool")
            dot.edge("process_tool", "agent")

            # 渲染为图片并保存
            dot.render("agent_state_graph", format="png", cleanup=True)
            logger.info("状态图已保存为 agent_state_graph.png")
        except Exception as e:
            logger.warning(f"画图失败: {e}")
        return graph.compile()
    
    def _agent_node(self, state: AgentState) -> AgentState:
        """Agent节点，决定下一步行动"""
        # 断点提示: 可以在此处设置断点检查Agent节点的处理过程
        # breakpoint()
        
        logger.debug("进入Agent节点")
        messages = state["messages"]
        
        # 准备工具描述
        tool_descriptions = []
        for tool in self.tools:
            tool_descriptions.append(f"- {tool.name}: {tool.description}")
        
        tools_str = "\n".join(tool_descriptions)
        
        # 准备提示
        user_input = messages[-1].content if messages else ""
        logger.debug(f"用户输入: {user_input}")
        
        prompt_with_tools = self.prompt.format(
            tools=tools_str,
            input=user_input
        )
        
        # 获取模型响应
        logger.debug("调用LLM获取响应")
        response = self.llm.invoke(prompt_with_tools)
        logger.debug(f"LLM响应: {response[:100]}...")  # 只记录前100个字符
        
        # 创建AI消息
        ai_message = AIMessage(content=response)
        
        # 更新消息历史
        messages.append(ai_message)
        
        # 更新状态
        state["messages"] = messages
        
        logger.debug("Agent节点处理完成")
        return state
    
    def _route(self, state: AgentState) -> Union[str, Dict[str, Any]]:
        """路由节点，决定是使用工具还是直接回复"""
        messages = state["messages"]
        last_message = messages[-1]
        
        # 提取工具使用信息
        tool_info = extract_tool_use(last_message.content)
        
        if tool_info and tool_info.get("name") in self.tool_map:
            # 需要使用工具
            state["tool_calls"] = [tool_info]
            return "action"
        else:
            # 直接回复
            return END
    
    def _action_node(self, state: AgentState) -> AgentState:
        """执行工具调用"""
        # 断点提示: 可以在此处设置断点检查工具调用过程
        # breakpoint()
        
        logger.debug("进入Action节点")
        tool_calls = state["tool_calls"]
        tool_results = state.get("tool_results", [])
        
        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            params = tool_call.get("params", {})
            
            logger.debug(f"执行工具调用: {tool_name}, 参数: {params}")
            
            # 获取工具
            if tool_name in self.tool_map:
                tool = self.tool_map[tool_name]
                try:
                    # 执行工具调用
                    result = tool._run(**params)
                    logger.debug(f"工具执行成功: {result[:100]}..." if isinstance(result, str) and len(result) > 100 else f"工具执行成功: {result}")
                    
                    # 保存结果
                    tool_results.append({
                        "tool_name": tool_name,
                        "params": params,
                        "result": result
                    })
                except Exception as e:
                    # 工具执行错误
                    logger.error(f"工具执行错误: {str(e)}")
                    tool_results.append({
                        "tool_name": tool_name,
                        "params": params,
                        "error": str(e)
                    })
        
        # 更新状态
        state["tool_results"] = tool_results
        state["tool_calls"] = []
        
        logger.debug("Action节点处理完成")
        return state
    
    def _process_tool_node(self, state: AgentState) -> AgentState:
        """处理工具调用结果"""
        # 断点提示: 可以在此处设置断点检查工具结果处理过程
        # breakpoint()
        
        logger.debug("进入ProcessTool节点")
        messages = state["messages"]
        tool_results = state["tool_results"]
        
        if tool_results:
            # 获取最新的工具调用结果
            latest_result = tool_results[-1]
            tool_name = latest_result.get("tool_name")
            result = latest_result.get("result", "")
            error = latest_result.get("error", "")
            
            # 构建结果消息
            if error:
                result_message = f"工具 {tool_name} 执行失败: {error}"
                logger.debug(f"工具执行失败消息: {result_message}")
            else:
                result_message = f"工具 {tool_name} 执行结果: {result}"
                logger.debug(f"工具执行结果消息: {result_message[:100]}..." if len(result_message) > 100 else result_message)
            
            # 添加人类消息
            human_message = HumanMessage(content=result_message)
            messages.append(human_message)
        
        # 更新状态
        state["messages"] = messages
        
        logger.debug("ProcessTool节点处理完成")
        return state
    
    def invoke(self, query: str) -> str:
        """
        执行Agent查询
        
        Args:
            query: 用户查询
            
        Returns:
            Agent的响应
        """
        # 断点提示: 可以在此处设置断点检查整个调用流程的开始
        # breakpoint()
        
        logger.info(f"开始处理查询: {query}")
        
        # 准备初始状态
        initial_state = {
            "messages": [HumanMessage(content=query)],
            "tool_calls": [],
            "tool_results": []
        }
        
        # 执行图
        logger.debug("开始执行状态图")
        result = self.graph.invoke(initial_state)
        logger.debug("状态图执行完成")
        
        # 提取回复
        final_messages = result["messages"]
        ai_messages = [msg for msg in final_messages if isinstance(msg, AIMessage)]
        
        if ai_messages:
            # 提取最终回复
            final_response = ai_messages[-1].content
            
            # 尝试提取"回答:"部分
            answer_match = re.search(r"回答:(.*?)(?:$|问题:|思考:|行动:)", final_response, re.DOTALL)
            if answer_match:
                answer = answer_match.group(1).strip()
                logger.info(f"生成最终回答: {answer[:100]}..." if len(answer) > 100 else answer)
                return answer
            
            logger.info(f"生成最终回复: {final_response[:100]}..." if len(final_response) > 100 else final_response)
            return final_response
        
        logger.warning("无法生成回复")
        return "无法生成回复。" 