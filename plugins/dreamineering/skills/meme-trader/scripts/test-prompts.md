# Meme Trader - Test Prompts

Test prompts to validate skill triggers correctly and produces expected outputs.

## Activation Test Prompts

### Category: Token Analysis

**Prompt 1:**
```
Analyze this token: PUMP123abc
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- Token overview
- Price and market cap
- Liquidity assessment
- Risk score
- Entry/exit signals

---

**Prompt 2:**
```
Is this a rug? CA: abc123def456
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- Rug detection checklist
- Mint/freeze authority status
- LP lock status
- Holder distribution
- Verdict (APE/WATCH/AVOID)

---

**Prompt 3:**
```
Give me entry for $DCAT
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- Current price
- Suggested entry point
- Stop loss level
- Take profit targets
- Position size recommendation

---

### Category: Alpha & Discovery

**Prompt 4:**
```
Find me alpha on pump.fun
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- New launches list
- Trending tokens
- Early stage opportunities
- Risk assessments

---

**Prompt 5:**
```
What memes should I ape?
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- Top picks with reasons
- Risk scores
- Quick scan format
- Entry signals

---

**Prompt 6:**
```
Trending Solana memecoins
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- List of trending tokens
- Table format with key metrics
- Volume leaders
- Recent pumps

---

### Category: Risk Assessment

**Prompt 7:**
```
Check liquidity for $SOLPEPE
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- Liquidity depth
- LP lock status
- Liquidity/MCAP ratio
- Slippage estimates

---

**Prompt 8:**
```
Holder distribution for PUMP456xyz
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- Total holders
- Top 10 holder percentage
- Whale wallets identified
- Distribution health assessment

---

### Category: Trade Execution

**Prompt 9:**
```
Give me a degen play
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- High risk opportunity
- Aggressive position sizing (5%)
- Wide stops (50%)
- 2-5x take profit targets

---

**Prompt 10:**
```
Conservative entry for established memes
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- Lower risk picks
- Tight stops (10-15%)
- Smaller position sizes (1%)
- Moderate take profits (20-50%)

---

## Negative Test Prompts (Should NOT Activate)

**Prompt 11:**
```
What's the weather today?
```

**Expected Skill Activation:** NO
**Reason:** Not related to memecoin trading

---

**Prompt 12:**
```
How do I write a React component?
```

**Expected Skill Activation:** NO
**Reason:** Generic programming, not meme trading

---

**Prompt 13:**
```
Tell me about Ethereum staking
```

**Expected Skill Activation:** MAYBE
**Reason:** Crypto-related but not memecoin specific. Should NOT activate unless about meme tokens on ETH.

---

## Edge Cases

**Prompt 14:**
```
memecoin
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- Overview of memecoin market
- Current trends
- Top movers

---

**Prompt 15:**
```
dexscreener
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- How to use Dexscreener
- Current trending pairs
- Analysis guidance

---

**Prompt 16:**
```
pump.fun new launches
```

**Expected Skill Activation:** YES
**Expected Response Contains:**
- Recent launches
- Bonding curve status
- Early opportunities
- Risk warnings

---

## Validation Criteria

For each test prompt:

1. **Skill Activates**: Skill is triggered by the query
2. **Accurate Response**: Information is factual and current
3. **Complete Coverage**: All expected response elements present
4. **Risk Included**: Every trade signal includes risk score and stop loss
5. **Performance**: Response within <5s target
6. **No Errors**: No API timeouts or failures

## Success Rate Target

- **Positive Tests (1-10):** 100% activation (10/10)
- **Negative Tests (11-13):** 0% false positives (0/3)
- **Edge Cases (14-16):** 100% correct handling (3/3)

**Overall Target:** ≥95% accuracy

## CLI Test Commands

```bash
# Test different actions
npx tsx scripts/fetch-meme-data.ts --token "PUMP123" --action analyze
npx tsx scripts/fetch-meme-data.ts --token "ABC123" --action rug_check
npx tsx scripts/fetch-meme-data.ts --action trending --limit 5

# Test different risk levels
npx tsx scripts/fetch-meme-data.ts --token "TEST" --risk degen
npx tsx scripts/fetch-meme-data.ts --token "TEST" --risk conservative

# Test different formats
npx tsx scripts/fetch-meme-data.ts --token "TEST" --format quick
npx tsx scripts/fetch-meme-data.ts --token "TEST" --format deep
npx tsx scripts/fetch-meme-data.ts --token "TEST" --format signal
npx tsx scripts/fetch-meme-data.ts --action trending --format table

# Run validation tests
npx vitest run scripts/validate-meme-trader-skill.test.ts
```

## Test Results Log

| Date | Prompt # | Activated? | Response Quality | Notes |
|------|----------|------------|------------------|-------|
|      |          |            |                  |       |

---

**Last Updated:** 2025-11-21
**Test Suite Version:** 1.0.0
**Maintainer:** Claude Code Validation System
