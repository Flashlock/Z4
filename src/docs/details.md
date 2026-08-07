# Z4

Z4 continuously monitors PC component marketplaces to design the computer that best aligns with a user's goals at the lowest practical cost.

## How it works

1. Marketplace listings are scraped on a schedule.
2. AI normalizes unstructured listings into canonical components and interfaces.
3. Compatibility is modeled as a directed dependency graph.
4. The builder searches that graph for builds that meet the user's goals.
5. Compelling purchase opportunities surface through Pantheon HITL.

## Surfaces

- **API** — health, jobs, and agent HTTP endpoints Hub cron / Docs / invoke call.
- **MFE** — industrial workstation UI for builds, listings, and human approval breakpoints.
