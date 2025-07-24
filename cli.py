import os
import argparse
import sys
import pdb
from typing import Dict, Any

from src.tools import get_tools
from src.models import get_model, get_prompt
from src.agents import LangGraphAgent
from src.config import get_deepseek_config

def main():
    """主函数"""
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="LangGraph Agent CLI")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细日志")
    parser.add_argument("--debug", "-d", action="store_true", help="启用调试模式")
    parser.add_argument("--pdb", action="store_true", help="启用pdb调试器")
    parser.add_argument("--breakpoint", action="store_true", help="在初始化后立即设置断点")
    args = parser.parse_args()
    
    # 如果启用了pdb，设置sys.breakpointhook为pdb.set_trace
    if args.pdb:
        sys.breakpointhook = pdb.set_trace
    
    # 获取配置
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
        prompt_template=prompt,
        verbose=args.verbose or args.debug  # 如果--verbose或--debug任一为True，则启用详细日志
    )
    
    print("=" * 50)
    print("欢迎使用LangGraph Agent CLI")
    print("输入 'exit' 或 'quit' 退出")
    if args.verbose:
        print("详细日志模式已启用")
    if args.debug:
        print("调试模式已启用")
    if args.pdb:
        print("PDB调试器已启用 - 可以使用breakpoint()函数设置断点")
    print("=" * 50)
    
    # 如果设置了断点参数，在此处设置断点
    if args.breakpoint:
        print("断点已设置，请按'n'继续执行下一步...")
        breakpoint()
    
    conversation_id = None
    
    while True:
        # 获取用户输入
        user_input = input("\n用户: ")
        
        # 检查退出命令
        if user_input.lower() in ["exit", "quit"]:
            print("谢谢使用，再见！")
            break
        
        # 检查是否设置断点
        if user_input.lower() == "debug":
            print("设置断点，进入调试模式...")
            breakpoint()
            continue
        
        try:
            # 调用Agent
            response = agent.invoke(user_input)
            
            # 打印回复
            print(f"\nAI助手: {response}")
            
        except Exception as e:
            print(f"\n错误: {str(e)}")
            if args.debug:
                import traceback
                traceback.print_exc()
            
            # 在异常发生时自动进入调试模式
            if args.pdb:
                print("发生异常，进入调试模式...")
                pdb.post_mortem()

if __name__ == "__main__":
    main() 