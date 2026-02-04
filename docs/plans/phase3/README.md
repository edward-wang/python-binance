# Phase 3: Spot API Implementation

This directory contains the implementation plan for Phase 3 of the Binance Python Wrapper project.

## Plan Structure

| File | Tasks | Lines | Description |
|------|-------|-------|-------------|
| [00-overview.md](./00-overview.md) | - | ~150 | Prerequisites, scope, verification milestones |
| [01-generate-endpoints.md](./01-generate-endpoints.md) | 1-3 | ~350 | Run generator, create api/spot/ modules |
| [02-generate-schemas.md](./02-generate-schemas.md) | 4-6 | ~400 | Generate _schemas/spot.py, write schema tests |
| [03-async-client.md](./03-async-client.md) | 7-9 | ~500 | Create AsyncClient entry point |
| [04-integration-testing.md](./04-integration-testing.md) | 10-12 | ~400 | Test on Binance testnet |

**Total: 12 tasks across 4 implementation files**

## Quick Start

1. Read [00-overview.md](./00-overview.md) to understand prerequisites
2. Execute each file in order using `superpowers:executing-plans` skill
3. Each task follows TDD: write test → run (fail) → implement → run (pass) → commit

## Execution Options

After reviewing the plan:

**Option 1: Subagent-Driven (this session)**
- Dispatch fresh subagent per task
- Review between tasks
- Fast iteration

**Option 2: Parallel Session (separate)**
- Open new session in worktree
- Use `superpowers:executing-plans` skill
- Batch execution with checkpoints

## Dependencies

This plan requires:
- **Phase 1 Complete:** `binance/_core/` infrastructure
- **Phase 2 Complete:** `generator/` can parse and emit code
- **Testnet Keys:** For integration tests (optional for unit tests)

## Output

After Phase 3 completion:

```
binance/
├── __init__.py              # Export AsyncClient
├── client.py                # AsyncClient entry point
├── _core/                   # From Phase 1
├── _schemas/
│   ├── common.py            # From Phase 1
│   └── spot.py              # Generated
└── api/
    └── spot/
        ├── general.py       # ping, time, exchange_info
        ├── market.py        # klines, depth, trades
        ├── trade.py         # orders, cancel
        └── account.py       # account, my_trades
```

## Verification

| Milestone | Command |
|-----------|---------|
| Generator runs | `python -m generator spot` |
| Code valid | `python -c "from binance import AsyncClient"` |
| Types check | `mypy binance/ --strict` |
| Unit tests | `pytest tests/unit/ -v` |
| Integration | `pytest tests/integration/ -v` |
