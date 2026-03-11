#!/bin/bash
# Validate agent YAML before deployment

set -e

if [ -z "$1" ]; then
    echo "Usage: validate-agent.sh <agent.yaml>"
    echo ""
    echo "Example:"
    echo "  ./scripts/validate-agent.sh my_agent.agent.yaml"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: File not found: $1"
    exit 1
fi

echo "Validating agent: $1"
flipside agents validate "$1"
