# LangGraph Agent Demo

基于LangGraph和LangChain实现的Agent示例项目，可以调用工具并回答用户问题。

## 项目结构

```
.
├── app.py              # FastAPI应用入口
├── cli.py              # 命令行客户端
├── requirements.txt    # 项目依赖
└── src/                # 源代码目录
    ├── agents/         # Agent实现
    ├── chains/         # LangChain链
    ├── config.py       # DeepSeek API配置
    ├── models/         # 模型配置
    └── tools/          # 工具实现
```

## 功能特点

- 基于LangGraph实现的Agent架构
- 使用LangChain的DeepSeek模型作为大语言模型
- 支持多种工具调用（计算器、天气查询等）
- 提供Web API和命令行两种交互方式
- 灵活的配置管理

## 安装

1. 克隆项目

```bash
git clone https://github.com/yourusername/chatbot-agent-langgraph-demo.git
cd chatbot-agent-langgraph-demo
```

2. 安装依赖

```bash
pip install -r requirements.txt
```

3. 设置环境变量

```bash
# Linux/Mac
export DEEPSEEK_API_KEY=your_api_key_here
export DEEPSEEK_MODEL=deepseek-chat  # 可选，默认为deepseek-chat

# Windows
set DEEPSEEK_API_KEY=your_api_key_here
set DEEPSEEK_MODEL=deepseek-chat  # 可选，默认为deepseek-chat
```

可配置的环境变量:
- `DEEPSEEK_API_KEY`: DeepSeek API密钥（必需）
- `DEEPSEEK_MODEL`: 模型名称（可选，默认为deepseek-chat）
- `DEEPSEEK_TEMPERATURE`: 温度参数（可选，默认为0.7）
- `DEEPSEEK_TOP_P`: Top-p采样参数（可选，默认为0.95）
- `DEEPSEEK_MAX_TOKENS`: 生成的最大令牌数（可选，默认为2048）
- `DEEPSEEK_STREAMING`: 是否启用流式响应（可选，默认为True）
- `DEEPSEEK_API_BASE`: API基础URL（可选，默认为https://api.deepseek.com/v1）

## 使用方法

### 命令行客户端

```bash
python cli.py
```

### Web API

```bash
python app.py
```

启动后，API服务将在 http://localhost:8000 运行。

#### API接口

- `GET /`: 欢迎页面
- `POST /chat`: 发送聊天消息
- `GET /tools`: 获取所有可用工具列表

## 示例

### 使用计算器工具

用户输入: "计算 2 + 2 等于多少？"

Agent会调用计算器工具并返回结果。

### 查询天气

用户输入: "北京今天的天气怎么样？"

Agent会调用天气查询工具并返回相关信息。

## 定制化

### 添加新工具

1. 在 `src/tools/` 目录下创建新的工具类
2. 修改 `src/tools/basic_tools.py` 中的 `get_tools()` 函数，添加新工具

### 修改提示模板

修改 `src/models/model_config.py` 文件中的 `SYSTEM_PROMPT` 变量。

### 配置管理

通过修改 `src/config.py` 或设置环境变量来调整DeepSeek API的配置。

## 许可证

MIT 