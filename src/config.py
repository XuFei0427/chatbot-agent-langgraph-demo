import os
from typing import Dict, Any, Optional

# DeepSeek API配置
class DeepSeekConfig:
    """DeepSeek API配置类"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "deepseek-chat",
        temperature: float = 0.7,
        top_p: float = 0.95,
        max_tokens: int = 2048,
        streaming: bool = True,
        api_base_url: str = "https://api.deepseek.com/v1",
    ):
        """
        初始化DeepSeek API配置
        
        Args:
            api_key: API密钥，如果为None则从环境变量获取
            model_name: 模型名称
            temperature: 温度参数，控制生成文本的随机性
            top_p: Top-p采样参数
            max_tokens: 生成的最大令牌数
            streaming: 是否启用流式响应
            api_base_url: API基础URL
        """
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY", "")
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.streaming = streaming
        self.api_base_url = api_base_url
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将配置转换为字典
        
        Returns:
            包含配置参数的字典
        """
        return {
            "model_name": self.model_name,
            "api_key": self.api_key,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens,
            "streaming": self.streaming,
            "api_base_url": self.api_base_url,
        }
    
    @classmethod
    def from_env(cls) -> "DeepSeekConfig":
        """
        从环境变量创建配置
        
        配置可以通过以下环境变量设置:
        - DEEPSEEK_API_KEY: DeepSeek API密钥（必需）
        - DEEPSEEK_MODEL: 模型名称（可选，默认为deepseek-chat）
        - DEEPSEEK_TEMPERATURE: 温度参数（可选，默认为0.7）
        - DEEPSEEK_TOP_P: Top-p采样参数（可选，默认为0.95）
        - DEEPSEEK_MAX_TOKENS: 生成的最大令牌数（可选，默认为2048）
        - DEEPSEEK_STREAMING: 是否启用流式响应（可选，默认为True）
        - DEEPSEEK_API_BASE_URL: API基础URL（可选，默认为https://api.deepseek.com/v1）
        
        示例:
        ```
        # Windows
        set DEEPSEEK_API_KEY=your_api_key_here
        set DEEPSEEK_MODEL=deepseek-chat
        
        # Linux/Mac
        export DEEPSEEK_API_KEY=your_api_key_here
        export DEEPSEEK_MODEL=deepseek-chat
        ```
        
        Returns:
            配置实例
        """
        return cls(
            api_key=os.getenv("DEEPSEEK_API_KEY", ""),
            model_name=os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
            temperature=float(os.getenv("DEEPSEEK_TEMPERATURE", "0.7")),
            top_p=float(os.getenv("DEEPSEEK_TOP_P", "0.95")),
            max_tokens=int(os.getenv("DEEPSEEK_MAX_TOKENS", "2048")),
            streaming=os.getenv("DEEPSEEK_STREAMING", "True").lower() == "true",
            api_base_url=os.getenv("DEEPSEEK_API_BASE_URL", "https://api.deepseek.com/v1"),
        )

# 默认配置
default_config = DeepSeekConfig.from_env()

# 获取DeepSeek配置
def get_deepseek_config() -> DeepSeekConfig:
    """
    获取DeepSeek配置
    
    首先尝试从环境变量获取配置，如果未设置则使用默认值
    
    Returns:
        DeepSeek配置实例
    """
    return default_config 