---
name: flipside
description: |
  Query blockchain data across 40+ chains using Flipside's AI agents. Use when
  working with blockchain data, crypto wallets, DeFi protocols, NFTs, token
  transfers, or on-chain analytics.
  Requires the Flipside CLI (https://docs.flipsidecrypto.xyz/get-started/cli).
compatibility: Requires flipside CLI installed and authenticated (flipside login)
allowed-tools: Bash(flipside:*) Read Write
metadata:
  author: flipside
  version: "2.0"
  homepage: https://flipsidecrypto.xyz
---

# Flipside CLI

First, check if the CLI is installed:

```bash
flipside --version
```

If the command is not found, install it:

```bash
curl -fsSL https://raw.githubusercontent.com/FlipsideCrypto/flipside-tools/main/install.sh | sh
```

Then get started:

```bash
flipside llm onboard
```
