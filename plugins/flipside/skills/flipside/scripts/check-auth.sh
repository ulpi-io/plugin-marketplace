#!/bin/bash
# Verify Flipside CLI is installed and authenticated

set -e

# Check if flipside CLI is installed
if ! command -v flipside &> /dev/null; then
    echo "Error: flipside CLI is not installed"
    echo ""
    echo "Install it with:"
    echo "  curl -fsSL https://install.flipsidecrypto.xyz | sh"
    echo ""
    echo "Or visit: https://docs.flipsidecrypto.xyz/get-started/cli"
    exit 1
fi

# Check if authenticated
if ! flipside whoami &>/dev/null; then
    echo "Error: Not authenticated with Flipside"
    echo ""
    echo "Run:"
    echo "  flipside login"
    exit 1
fi

# Show current user
echo "Authenticated as:"
flipside whoami
