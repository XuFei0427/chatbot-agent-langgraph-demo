import json
import requests
from typing import Dict, Any, List, Optional, Union
from langchain_core.language_models import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from pydantic import Field

class CustomDeepSeek(LLM):
    """
    自定义DeepSeek LLM实现
    """
    
    model_name: str = Field(default="deepseek-chat")
    api_key: str
    api_base_url: str = Field(default="https://api.deepseek.com/v1")
    temperature: float = Field(default=0.7)
    top_p: float = Field(default=0.95)
    max_tokens: int = Field(default=2048)
    
    @property
    def _llm_type(self) -> str:
        """返回LLM类型"""
        return "custom_deepseek"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        """
        调用DeepSeek API
        
        Args:
            prompt: 输入提示
            stop: 停止词列表
            run_manager: 回调管理器
            
        Returns:
            模型响应文本
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        messages = [{"role": "user", "content": prompt}]
        
        payload = {
            "model": self.model_name,
            "messages": messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "max_tokens": self.max_tokens
        }
        
        if stop:
            payload["stop"] = stop
        
        response = requests.post(
            f"{self.api_base_url}/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )
        
        if response.status_code != 200:
            error_msg = f"API请求失败: {response.status_code} - {response.text}"
            raise ValueError(error_msg)
        
        response_data = response.json()
        
        if "choices" not in response_data or not response_data["choices"]:
            raise ValueError(f"API响应格式异常: {response_data}")
        
        return response_data["choices"][0]["message"]["content"] 