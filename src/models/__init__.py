# 模型包初始化文件
from src.models.model_config import get_model, get_prompt, SYSTEM_PROMPT
from src.models.deepseek import CustomDeepSeek

__all__ = ["get_model", "get_prompt", "SYSTEM_PROMPT", "CustomDeepSeek"] 