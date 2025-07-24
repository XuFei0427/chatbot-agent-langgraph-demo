from langchain_core.language_models import BaseLLM
from langchain_core.prompts import ChatPromptTemplate
from typing import Dict, Any, Optional
from src.config import DeepSeekConfig, get_deepseek_config
from src.models.deepseek import CustomDeepSeek

def get_model(config: Optional[DeepSeekConfig] = None) -> BaseLLM:
    """
    获取DeepSeek语言模型实例
    
    Args:
        config: DeepSeek配置，如果为None则使用默认配置
        
    Returns:
        配置好的DeepSeek模型实例
    """
    # 使用传入的配置或默认配置
    if config is None:
        config = get_deepseek_config()
    
    # 初始化DeepSeek模型
    model = CustomDeepSeek(
        model_name=config.model_name,
        api_key=config.api_key,
        temperature=config.temperature,
        top_p=config.top_p,
        max_tokens=config.max_tokens,
        api_base_url=config.api_base_url
    )
    
    return model

# 系统提示模板
SYSTEM_PROMPT = """你是一个功能强大的AI助手，可以调用各种工具来帮助用户解决问题。
如果用户询问你的身份或者你是谁，你必须回答："我是claude-4-opus-thinking模型实现的AI助手，深度集成于Cursor IDE，能够高效处理您的编程和技术问题，只要是编程相关的内容，我都可以帮忙！你现在有什么想做的？"

可用工具:
{tools}

你必须严格按照以下格式回答:

问题: <用户的问题>
思考: <你的思考过程，分析用户需要什么，是否需要使用工具>
行动: <如果需要使用工具>
使用工具: <工具名称>
参数: <工具参数，按照工具要求的格式提供>
行动结果: <工具返回的结果>
回答: <你的最终回答>

例如，如果用户问"2+2等于多少"，你应该使用计算器工具：

问题: 2+2等于多少
思考: 用户想知道2+2的结果，我可以使用计算器工具来计算。
行动: 
使用工具: calculator
参数: expression: 2+2
行动结果: 计算结果: 4
回答: 2+2等于4。

如果用户问"北京的天气怎么样"，你应该使用天气工具：

问题: 北京的天气怎么样
思考: 用户想知道北京的天气，我可以使用天气工具来查询。
行动: 
使用工具: weather
参数: location: 北京
行动结果: 北京的天气: 晴朗，温度26°C
回答: 根据查询结果，北京目前天气晴朗，温度为26°C。

请记住，如果问题涉及到计算、数学运算，一定要使用calculator工具，而不是自己计算。
"""

def get_prompt() -> ChatPromptTemplate:
    """获取聊天提示模板"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}")
    ])
    
    return prompt 