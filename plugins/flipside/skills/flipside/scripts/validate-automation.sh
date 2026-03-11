#!/bin/bash
# Validate automation YAML before deployment

set -e

if [ -z "$1" ]; then
    echo "Usage: validate-automation.sh <automation.yaml>"
    echo ""
    echo "Example:"
    echo "  ./scripts/validate-automation.sh my_pipeline.automation.yaml"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "Error: File not found: $1"
    exit 1
fi

echo "Validating automation: $1"
flipside automations validate "$1"
