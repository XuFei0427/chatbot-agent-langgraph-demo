from typing import Dict, Any, List, Optional, Type
from pydantic import BaseModel, Field
from langchain_core.tools import BaseTool

class CalculatorInput(BaseModel):
    """计算器工具的输入"""
    expression: str = Field(description="数学表达式，例如 '2 + 2' 或 '3 * 4'")

class Calculator(BaseTool):
    """一个简单的计算器工具"""
    name: str = "calculator"
    description: str = "对数学表达式进行计算，支持基本的加减乘除运算"
    args_schema: Type[BaseModel] = CalculatorInput
    
    def _run(self, expression: str) -> str:
        """执行计算"""
        try:
            result = eval(expression)
            return f"计算结果: {result}"
        except Exception as e:
            return f"计算错误: {str(e)}"
    
    async def _arun(self, expression: str) -> str:
        """异步执行计算"""
        return self._run(expression)

class WeatherInput(BaseModel):
    """天气查询工具的输入"""
    location: str = Field(description="要查询天气的地点，例如'北京'")

class WeatherTool(BaseTool):
    """一个模拟的天气查询工具"""
    name: str = "weather"
    description: str = "查询指定地点的天气情况"
    args_schema: Type[BaseModel] = WeatherInput
    
    def _run(self, location: str) -> str:
        """获取天气信息（模拟）"""
        # 这里只是模拟返回天气信息
        weather_data = {
            "北京": "晴朗，温度26°C",
            "上海": "多云，温度24°C",
            "广州": "小雨，温度28°C",
            "深圳": "阴天，温度27°C"
        }
        
        return f"{location}的天气: {weather_data.get(location, '无法获取天气信息')}"
    
    async def _arun(self, location: str) -> str:
        """异步获取天气信息"""
        return self._run(location)

def get_tools() -> List[BaseTool]:
    """获取所有可用工具的列表"""
    return [
        Calculator(),
        WeatherTool()
    ] 