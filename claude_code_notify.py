#!/usr/bin/env python3
"""
Claude Code 通知钩子脚本

此脚本的主要作用是：
1. 监听来自 Claude Code 的消息
2. 根据消息内容类型显示不同的桌面通知
3. 播放声音以提醒用户

支持的系统：主要针对 macOS 系统设计
"""
# 导入必要的库
import json      # 用于解析 JSON 数据
import sys       # 用于访问标准输入
import subprocess # 用于执行系统命令
import platform   # 用于检测当前操作系统

try:
    # 从标准输入读取 JSON 格式的数据
    data = json.load(sys.stdin)
    # 提取消息内容，如果没有消息则使用默认提示
    message = data.get("message", "Claude Code 需要您的注意")

    # 根据消息内容确定通知类型和图标
    if any(w in message.lower() for w in ("waiting", "input")):
        # 当消息包含等待或输入相关词汇时，显示等待图标
        notification = f"⌛ {message}"
    elif any(w in message.lower() for w in ("permission", "confirm")):
        # 当消息包含权限或确认相关词汇时，显示疑问图标
        notification = f"❔ {message}"
    elif any(w in message.lower() for w in ("error", "failed")):
        # 当消息包含错误或失败相关词汇时，显示警告图标
        notification = f"⚠️ {message}"
    else:
        # 其他情况下显示普通消息图标
        notification = f"💬 {message}"

    # 检查当前是否为 macOS 系统（Darwin 是 macOS 的系统名称）
    if platform.system() == "Darwin":
        try:
            # 优先尝试使用 terminal-notifier 工具发送通知
            # 这是一个更强大的 macOS 通知工具
            subprocess.run([
                "terminal-notifier",          # 通知工具名称
                "-message", notification,     # 通知消息内容
                "-title", "Claude Code",      # 通知标题
                "-sound", "Glass",           # 通知声音
                "-activate", "com.todesktop.230313m2l4w4u92"  # 点击通知时激活的应用
            ], check=False, capture_output=True)
        except FileNotFoundError:
            # 如果 terminal-notifier 不可用，则回退到使用 osascript（AppleScript）
            subprocess.run([
                "osascript", "-e",
                # 使用 AppleScript 显示通知
                f'display notification "{notification}" with title "Claude Code" sound name "Glass"'
            ], capture_output=True)

except Exception as e:
    # 捕获所有异常并输出到标准错误流
    print(f"通知钩子错误: {e}", file=sys.stderr)
    # 以错误状态退出脚本
    sys.exit(1)
