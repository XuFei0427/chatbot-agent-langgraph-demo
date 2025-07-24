# LangGraph Agent 调试指南

本指南将帮助您理解如何调试和查看LangGraph Agent的执行流程。

## 启用调试选项

### 1. 使用详细日志

通过`--verbose`或`-v`选项启用详细日志输出：

```bash
python cli.py --verbose
```

这将显示执行过程中的每个步骤，包括：
- 节点进入和退出
- 模型输入和输出
- 工具调用和结果
- 路由决策过程

### 2. 使用调试模式

通过`--debug`或`-d`选项启用调试模式：

```bash
python cli.py --debug
```

这类似于详细日志，但在出错时还会显示完整的堆栈跟踪。

### 3. 使用PDB调试器

通过`--pdb`选项启用Python调试器：

```bash
python cli.py --pdb
```

这将允许您使用Python的`breakpoint()`函数在代码中设置断点。

### 4. 设置初始断点

使用`--breakpoint`选项在初始化后立即进入调试器：

```bash
python cli.py --breakpoint
```

### 5. 在会话中进入调试

在运行时输入`debug`指令可以随时进入调试器：

```
用户: debug
```

## PDB调试器基本命令

进入调试器后，您可以使用以下命令：

- `n`: 执行下一行代码(step over)
- `s`: 进入函数(step into)
- `c`: 继续执行直到下一个断点
- `q`: 退出调试器
- `p <变量>`: 打印变量值，例如`p state`
- `pp <变量>`: 格式化打印变量，例如`pp state`
- `l`: 显示当前位置的代码
- `h`: 帮助

## 常用断点位置

在代码中，有几个关键位置可以设置断点：

1. **用户查询入口**：在`invoke`方法开始处
   ```python
   def invoke(self, query: str):
       breakpoint()  # 在此设置断点
   ```

2. **模型响应处理**：在`_agent_node`方法中
   ```python
   def _agent_node(self, state: AgentState):
       breakpoint()  # 在此设置断点
   ```

3. **工具调用**：在`_action_node`方法中
   ```python
   def _action_node(self, state: AgentState):
       breakpoint()  # 在此设置断点
   ```

4. **工具结果处理**：在`_process_tool_node`方法中
   ```python
   def _process_tool_node(self, state: AgentState):
       breakpoint()  # 在此设置断点
   ```

5. **路由决策**：在`route`函数中
   ```python
   def route(state: AgentState):
       breakpoint()  # 在此设置断点
   ```

## 激活代码中的断点

代码中已经添加了断点提示，但它们被注释掉了。要激活断点，请取消注释相应的`breakpoint()`行。例如：

```python
# 断点提示: 可以在此处设置断点检查模型输出文本
breakpoint()  # 取消注释此行
```

## 调试状态的检查

在调试器中，您可以检查以下关键状态：

- `state["messages"]`: 消息历史
- `state["tool_calls"]`: 工具调用信息
- `state["tool_results"]`: 工具调用结果

例如：
```
(Pdb) pp state["messages"]
(Pdb) pp state["tool_calls"]
```

## 输出日志到文件

如果您想将日志保存到文件，可以使用以下命令：

```bash
python cli.py --verbose > agent_log.txt 2>&1
```

这将把所有输出保存到`agent_log.txt`文件中。 