# Data Policy

Event Intelligence is designed to distinguish authoritative event schedules from market-data feeds.

## Source priority

1. Official central-bank / statistical-agency source
2. Reputable aggregation source when the official schedule cannot be machine-read
3. Explicit fallback metadata only when a network source is unavailable

## No fabricated live data

The application does not generate a consensus or actual value when none is available. Missing fields are displayed as `—`.

## Market-data caveat

The default `yfinance` connector is suitable for a portfolio/demo dashboard and live-refresh workflow, but it should not be represented as guaranteed exchange-grade real-time data. Replace it with a licensed real-time feed for production trading use.

## Time handling

Official release times are retained where the source exposes them. Where an institution does not publish a machine-readable release time, the UI displays `See source`/`—` rather than inventing a time.
