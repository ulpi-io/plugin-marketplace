#!/usr/bin/env npx tsx
/**
 * Meme Trader Skill Validation Tests
 * Proves the skill enforcement and validation logic works correctly
 */

import { describe, expect, it } from 'vitest';
import type { MemeToken } from './fetch-meme-data';
import {
  CacheManager,
  MemeAPIClient,
  OutputFormatter,
  RiskCalculator,
} from './fetch-meme-data';

describe('Meme Trader Skill Validation', () => {
  describe('CacheManager', () => {
    it('should cache and retrieve tokens within TTL', () => {
      const cache = new CacheManager();
      const testTokens: MemeToken[] = [
        {
          address: 'TEST123',
          name: 'Test Meme',
          symbol: '$TEST',
          category: 'meme',
          metrics: {
            price: 0.001,
            priceChange24h: 50,
            marketCap: 100000,
            liquidity: 10000,
            volume24h: 50000,
            holders: 200,
            buys24h: 100,
            sells24h: 50,
          },
          security: {
            mintRenounced: true,
            freezeDisabled: true,
            lpLocked: true,
            lpLockDuration: '3 months',
            topHolderPercent: 5,
            top10Percent: 30,
            honeypotRisk: 'none',
          },
          social: {},
          verdict: 'APE',
          riskScore: 3,
        },
      ];

      const key = cache.getCacheKey({
        token: 'TEST123',
        action: 'analyze',
        risk: 'degen',
        format: 'quick',
        limit: 10,
        cache: true,
      });

      cache.set(key, testTokens);
      const retrieved = cache.get(key);

      expect(retrieved).toEqual(testTokens);
    });

    it('should return null for expired cache', () => {
      const cache = new CacheManager();
      const key = 'expired-key';

      // Access private property for testing
      const cacheInternal = cache as CacheManager & {
        cache: Map<string, { data: MemeToken[]; timestamp: number }>;
      };
      cacheInternal.cache.set(key, {
        data: [],
        timestamp: Date.now() - 2 * 60 * 1000, // 2 minutes ago (TTL is 1 min)
      });

      const result = cache.get(key);
      expect(result).toBeNull();
    });
  });

  describe('RiskCalculator', () => {
    const calculator = new RiskCalculator();

    it('should calculate high risk for dangerous tokens', () => {
      const dangerousToken: Partial<MemeToken> = {
        security: {
          mintRenounced: false,
          freezeDisabled: false,
          lpLocked: false,
          topHolderPercent: 35,
          top10Percent: 80,
          honeypotRisk: 'high',
        },
        metrics: {
          price: 0.0001,
          priceChange24h: -50,
          marketCap: 10000,
          liquidity: 5000,
          volume24h: 2000,
          holders: 50,
          buys24h: 5,
          sells24h: 30,
        },
      };

      const riskScore = calculator.calculateRiskScore(dangerousToken);
      expect(riskScore).toBeGreaterThanOrEqual(8);
    });

    it('should calculate low risk for safe tokens', () => {
      const safeToken: Partial<MemeToken> = {
        security: {
          mintRenounced: true,
          freezeDisabled: true,
          lpLocked: true,
          lpLockDuration: '1 year',
          topHolderPercent: 3,
          top10Percent: 20,
          honeypotRisk: 'none',
        },
        metrics: {
          price: 0.01,
          priceChange24h: 25,
          marketCap: 1000000,
          liquidity: 200000,
          volume24h: 500000,
          holders: 1000,
          buys24h: 300,
          sells24h: 150,
        },
      };

      const riskScore = calculator.calculateRiskScore(safeToken);
      expect(riskScore).toBeLessThanOrEqual(4);
    });

    it('should return APE verdict for low risk in degen mode', () => {
      const verdict = calculator.getVerdict(4, 'degen');
      expect(verdict).toBe('APE');
    });

    it('should return AVOID verdict for high risk in conservative mode', () => {
      const verdict = calculator.getVerdict(6, 'conservative');
      expect(verdict).toBe('AVOID');
    });

    it('should calculate appropriate signals for degen mode', () => {
      const mockToken: MemeToken = {
        address: 'TEST',
        name: 'Test',
        symbol: '$T',
        category: 'meme',
        metrics: {
          price: 0.001,
          priceChange24h: 0,
          marketCap: 100000,
          liquidity: 10000,
          volume24h: 50000,
          holders: 100,
          buys24h: 50,
          sells24h: 25,
        },
        security: {
          mintRenounced: true,
          freezeDisabled: true,
          lpLocked: true,
          topHolderPercent: 5,
          top10Percent: 30,
          honeypotRisk: 'none',
        },
        social: {},
        verdict: 'APE',
        riskScore: 3,
      };

      const signals = calculator.calculateSignals(mockToken, 'degen');

      expect(signals.entry).toBe(0.001);
      expect(signals.stopLoss).toBe(0.0005); // 50% SL in degen mode
      expect(signals.takeProfit1).toBe(0.002); // 2x TP1
      expect(signals.takeProfit2).toBe(0.005); // 5x TP2
      expect(signals.positionSize).toBe('5%');
    });
  });

  describe('OutputFormatter', () => {
    const formatter = new OutputFormatter();
    const mockToken: MemeToken = {
      address: 'MOCK123abc',
      name: 'Mock Meme',
      symbol: '$MOCK',
      category: 'meme',
      metrics: {
        price: 0.00042,
        priceChange24h: 125.5,
        marketCap: 500000,
        liquidity: 50000,
        volume24h: 200000,
        holders: 342,
        buys24h: 234,
        sells24h: 89,
      },
      security: {
        mintRenounced: true,
        freezeDisabled: true,
        lpLocked: true,
        lpLockDuration: '6 months',
        topHolderPercent: 8,
        top10Percent: 35,
        honeypotRisk: 'none',
      },
      social: {
        twitter: '@mockmeme',
        telegram: 't.me/mockmeme',
        twitterFollowers: 5000,
        telegramMembers: 2000,
      },
      verdict: 'APE',
      riskScore: 4,
    };

    it('should format token as JSON', () => {
      const result = formatter.format([mockToken], {
        token: 'test',
        action: 'analyze',
        risk: 'degen',
        format: 'json',
        limit: 10,
        cache: true,
      });
      const parsed = JSON.parse(result);
      expect(parsed[0].symbol).toBe('$MOCK');
    });

    it('should format token as quick scan', () => {
      const result = formatter.format([mockToken], {
        token: 'test',
        action: 'analyze',
        risk: 'degen',
        format: 'quick',
        limit: 10,
        cache: true,
      });
      expect(result).toContain('TOKEN: $MOCK');
      expect(result).toContain('VERDICT: APE');
      expect(result).toContain('RISK: 4/10');
    });

    it('should format signal only', () => {
      const result = formatter.format([mockToken], {
        token: 'test',
        action: 'signal',
        risk: 'degen',
        format: 'signal',
        limit: 10,
        cache: true,
      });
      expect(result).toContain('$MOCK: BUY');
      expect(result).toContain('TP');
      expect(result).toContain('SL');
    });

    it('should format multiple tokens as table', () => {
      const tokens = [mockToken, { ...mockToken, symbol: '$MOCK2' }];
      const result = formatter.format(tokens, {
        token: undefined,
        action: 'trending',
        risk: 'degen',
        format: 'table',
        limit: 10,
        cache: true,
      });
      expect(result).toContain('TRENDING MEMES');
      expect(result).toContain('$MOCK');
      expect(result).toContain('$MOCK2');
    });
  });

  describe('MemeAPIClient', () => {
    const client = new MemeAPIClient();

    it('should fetch mock token data', async () => {
      const token = await client.fetchToken('test-address');
      expect(token).toBeDefined();
      expect(token?.symbol).toBe('$SAMPLE');
    });

    it('should fetch trending tokens', async () => {
      const trending = await client.fetchTrending(5);
      expect(trending.length).toBeGreaterThan(0);
      expect(trending.length).toBeLessThanOrEqual(5);
    });

    it('should perform rug check', async () => {
      const result = await client.rugCheck('test-address');
      expect(result).toBeDefined();
      expect(result?.security).toBeDefined();
      expect(result?.riskScore).toBeDefined();
    });

    it('should handle API errors gracefully', async () => {
      // Should return mock data on error
      const token = await client.fetchToken('invalid-address-that-will-fail');
      expect(token).toBeDefined();
    });
  });

  describe('Rug Detection Logic', () => {
    const calculator = new RiskCalculator();

    it('should detect mint authority risk', () => {
      const token: Partial<MemeToken> = {
        security: {
          mintRenounced: false, // DANGER
          freezeDisabled: true,
          lpLocked: true,
          topHolderPercent: 5,
          top10Percent: 30,
          honeypotRisk: 'none',
        },
        metrics: {
          price: 0.01,
          priceChange24h: 0,
          marketCap: 500000,
          liquidity: 100000,
          volume24h: 200000,
          holders: 500,
          buys24h: 100,
          sells24h: 50,
        },
      };

      const risk = calculator.calculateRiskScore(token);
      expect(risk).toBeGreaterThan(5); // Should flag as risky
    });

    it('should detect low liquidity risk', () => {
      const token: Partial<MemeToken> = {
        security: {
          mintRenounced: true,
          freezeDisabled: true,
          lpLocked: true,
          topHolderPercent: 5,
          top10Percent: 30,
          honeypotRisk: 'none',
        },
        metrics: {
          price: 0.01,
          priceChange24h: 0,
          marketCap: 500000,
          liquidity: 5000, // Very low liquidity
          volume24h: 200000,
          holders: 500,
          buys24h: 100,
          sells24h: 50,
        },
      };

      const risk = calculator.calculateRiskScore(token);
      expect(risk).toBeGreaterThan(4);
    });

    it('should detect honeypot risk', () => {
      const token: Partial<MemeToken> = {
        security: {
          mintRenounced: true,
          freezeDisabled: true,
          lpLocked: true,
          topHolderPercent: 5,
          top10Percent: 30,
          honeypotRisk: 'high', // HONEYPOT
        },
        metrics: {
          price: 0.01,
          priceChange24h: 0,
          marketCap: 500000,
          liquidity: 100000,
          volume24h: 200000,
          holders: 500,
          buys24h: 100,
          sells24h: 50,
        },
      };

      const risk = calculator.calculateRiskScore(token);
      expect(risk).toBeGreaterThanOrEqual(6);
    });
  });

  describe('Signal Generation', () => {
    const calculator = new RiskCalculator();
    const baseToken: MemeToken = {
      address: 'TEST',
      name: 'Test',
      symbol: '$T',
      category: 'meme',
      metrics: {
        price: 0.001,
        priceChange24h: 0,
        marketCap: 100000,
        liquidity: 10000,
        volume24h: 50000,
        holders: 100,
        buys24h: 50,
        sells24h: 25,
      },
      security: {
        mintRenounced: true,
        freezeDisabled: true,
        lpLocked: true,
        topHolderPercent: 5,
        top10Percent: 30,
        honeypotRisk: 'none',
      },
      social: {},
      verdict: 'APE',
      riskScore: 3,
    };

    it('should have tighter stops in conservative mode', () => {
      const degenSignals = calculator.calculateSignals(baseToken, 'degen');
      const conservativeSignals = calculator.calculateSignals(baseToken, 'conservative');

      // Conservative SL should be closer to entry (higher value = tighter stop)
      expect(conservativeSignals.stopLoss).toBeGreaterThan(degenSignals.stopLoss);
    });

    it('should have smaller position size in conservative mode', () => {
      const degenSignals = calculator.calculateSignals(baseToken, 'degen');
      const conservativeSignals = calculator.calculateSignals(baseToken, 'conservative');

      expect(degenSignals.positionSize).toBe('5%');
      expect(conservativeSignals.positionSize).toBe('1%');
    });

    it('should have higher take profit targets in degen mode', () => {
      const degenSignals = calculator.calculateSignals(baseToken, 'degen');
      const moderateSignals = calculator.calculateSignals(baseToken, 'moderate');

      expect(degenSignals.takeProfit2).toBeGreaterThan(moderateSignals.takeProfit2);
    });
  });
});
