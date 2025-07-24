import os
import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

from src.tools import get_tools
from src.models import get_model, get_prompt
from src.agents import LangGraphAgent
from src.config import get_deepseek_config

# 创建FastAPI应用
app = FastAPI(title="LangGraph Agent API")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化配置
config = get_deepseek_config()

# 初始化工具
tools = get_tools()

# 初始化模型
llm = get_model(config=config)

# 获取提示模板
prompt = get_prompt()

# 初始化Agent
agent = LangGraphAgent(
    llm=llm,
    tools=tools,
    prompt_template=prompt
)

# 定义请求模型
class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    conversation_id: Optional[str] = None

# 定义响应模型
class ChatResponse(BaseModel):
    """聊天响应模型"""
    response: str
    conversation_id: str

@app.get("/")
async def root():
    """根路径处理函数"""
    return {"message": "欢迎使用LangGraph Agent API"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """处理聊天请求"""
    try:
        # 调用Agent
        response = agent.invoke(request.message)
        
        # 生成会话ID
        conversation_id = request.conversation_id or "conv_" + str(hash(request.message))[:8]
        
        return ChatResponse(
            response=response,
            conversation_id=conversation_id
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"处理聊天请求时出错: {str(e)}"}
        )

@app.get("/tools")
async def list_tools():
    """列出所有可用工具"""
    tool_list = []
    for tool in tools:
        tool_list.append({
            "name": tool.name,
            "description": tool.description
        })
    
    return {"tools": tool_list}

if __name__ == "__main__":
    # 启动应用
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 