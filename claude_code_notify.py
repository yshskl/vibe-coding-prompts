#!/usr/bin/env python3
"""
Notification hook for Claude Code – plays a sound and shows a desktop banner
"""
import json, sys, subprocess, platform

try:
    data = json.load(sys.stdin)
    message = data.get("message", "Claude Code needs your attention")

    if any(w in message.lower() for w in ("waiting", "input")):
        notification = f"⌛ {message}"
    elif any(w in message.lower() for w in ("permission", "confirm")):
        notification = f"❔ {message}"
    elif any(w in message.lower() for w in ("error", "failed")):
        notification = f"⚠️ {message}"
    else:
        notification = f"💬 {message}"

    if platform.system() == "Darwin":
        try:
            subprocess.run([
                "terminal-notifier",
                "-message", notification,
                "-title", "Claude Code",
                "-sound", "Glass",
                "-activate", "com.todesktop.230313m2l4w4u92"
            ], check=False, capture_output=True)
        except FileNotFoundError:
            subprocess.run([
                "osascript", "-e",
                f'display notification "{notification}" with title "Claude Code" sound name "Glass"'
            ], capture_output=True)

except Exception as e:
    print(f"Notification hook error: {e}", file=sys.stderr)
    sys.exit(1)
