#!/bin/bash
# Setup script for WeChat Article Fetcher skill

set -e

echo "🚀 Setting up WeChat Article Fetcher skill..."

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Make skill.py executable
chmod +x skill.py
echo "✓ Made skill.py executable"

# Check if MCP tools are available
echo ""
echo "🔍 Checking MCP tools..."

if command -v mcp &> /dev/null; then
    echo "✓ MCP CLI is available"

    # Test WeChat MCP
    if mcp call wechat list_followed_accounts &> /dev/null; then
        echo "✓ WeChat MCP is available"
    else
        echo "⚠️  WeChat MCP may not be configured"
    fi

    # Test Obsidian MCP
    if mcp call obsidian obsidian_list_files_in_vault &> /dev/null; then
        echo "✓ Obsidian MCP is available"
    else
        echo "⚠️  Obsidian MCP may not be configured"
    fi
else
    echo "⚠️  MCP CLI not found. Please install Claude Code CLI first."
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage examples:"
echo "  python3 skill.py fetch                    # Fetch yesterday's articles"
echo "  python3 skill.py fetch --accounts 量子位  # Fetch from specific account"
echo "  python3 skill.py list                     # List followed accounts"
echo ""
