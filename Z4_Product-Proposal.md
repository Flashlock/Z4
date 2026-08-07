# Agent Z4 Product Proposal

## Mission

Z4 continuously monitors PC component marketplaces to design the computer that best aligns with a user's goals at the lowest practical cost.

Rather than relying on static compatibility databases, Z4 maintains a continuously evolving model of the hardware ecosystem. As new listings appear and prices change, existing recommendations are automatically re-evaluated.

---

# Core Concept

Every hardware component is represented as:

* A normalized component
* A set of interfaces it provides
* A set of interfaces it requires

These relationships form a directed dependency graph where compatible components naturally connect.

Building a PC becomes a dependency resolution problem. Given a user's goal, Z4 searches the graph for compatible builds and ranks them according to factors such as price, performance, and purchase reliability.

AI is responsible for converting unstructured marketplace listings into a normalized data model. Once normalized, compatibility analysis and PC construction become deterministic graph operations.

---

# Architecture

```text
Marketplace Listings
        │
        ▼
Web Scrapers
        │
        ▼
AI Processing
        │
        ▼
Normalized Database
        │
        ▼
Component Graph
        │
        ▼
Builder
        │
        ▼
Pantheon HITL
```

---

# Database Design

The database is normalized to separate canonical hardware definitions from marketplace listings and historical pricing.

## components

Represents the canonical definition of a hardware component.

**Fields**

* id
* category
* manufacturer
* model
* specifications (JSON)
* created_at

A component exists only once regardless of how many marketplaces list it.

---

## interfaces

Represents every compatibility interface known to the system.

**Fields**

* id
* name
* description

Interfaces define how components connect within the dependency graph.

---

## component_interfaces

Maps components to interfaces.

**Fields**

* component_id
* interface_id
* direction (`Provides` | `Requires`)

This table defines the dependency graph used during PC construction.

---

## listings

Represents an individual marketplace listing.

**Fields**

* id
* component_id
* marketplace
* listing_url
* seller
* condition
* reliability_score
* ai_summary

Multiple listings may reference the same normalized component.

---

# Marketplace Processing

Pantheon Cron Jobs continuously monitor supported marketplaces.

For each batch of listings:

1. Scrape marketplace data.
2. Extract structured component information using AI.
3. Resolve components against the normalized database.
4. Resolve interfaces against the normalized database.
5. Generate the Reliability Score.
6. Store the normalized listing.
7. Record the current price.

Batch AI requests should be used whenever possible to minimize inference costs.

---

# Entity Resolution

Marketplace data is inherently inconsistent. The same component may appear under different names, abbreviations, or incomplete descriptions. Likewise, compatibility interfaces may be expressed differently across marketplaces.

As part of normalization, AI performs **entity resolution** to determine whether newly extracted information should reference an existing entity or create a new one.

For every extracted component, AI answers:

> **Is this an existing component, or should a new component be created?**

For every extracted interface, AI answers:

> **Is this an existing interface, or should a new interface be created?**

These decisions cannot rely on marketplace identifiers or exact string matching. Instead, AI evaluates naming variations, extracted specifications, relationships to other entities, and historical data to determine whether two records represent the same real-world object.

This process allows the normalized database to converge toward a single canonical representation of both components and interfaces over time.

---

# Reliability Score

Every marketplace listing receives a **Reliability Score** between **1 and 10** representing the likelihood that purchasing the component will result in a successful, long-term purchase.

The score estimates whether a listing is likely to become a liability due to hardware defects, misleading information, poor seller practices, or other risk factors.

| Score   | Meaning                                                                                                                                      |
| ------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **1–2** | Extremely high risk. Strong indicators of scams, damaged hardware, misleading information, or severe uncertainty.                            |
| **3–4** | High risk. Significant concerns exist and the listing is generally not recommended.                                                          |
| **5–6** | Moderate risk. The listing appears legitimate but contains enough uncertainty that buyers should proceed cautiously.                         |
| **7–8** | Low risk. The listing is complete, internally consistent, and shows few indicators of future problems.                                       |
| **9**   | Very low risk. Strong evidence suggests the component is accurately represented and is likely to be a dependable purchase.                   |
| **10**  | Exceptional reliability. The listing exhibits virtually no warning signs and closely matches the characteristics of a high-quality purchase. |

The score is derived from multiple signals, including:

* listing completeness and consistency
* seller reputation
* component condition
* image analysis
* pricing anomalies
* evidence of prior repairs or modifications
* duplicate or reused images
* marketplace trust signals
* AI extraction confidence

The Reliability Score is not a guarantee that a component will function correctly. It is a probabilistic assessment of whether purchasing the component is likely to result in a dependable, long-lasting addition to a user's build.

---

# Building the PC

The user begins by providing a goal, such as a budget, workload, or performance target.

The builder searches the dependency graph for compatible configurations that best satisfy those requirements while incorporating current marketplace pricing and listing reliability.

Users may lock purchased components into the build. Locked components become fixed constraints, allowing the remainder of the build to continue adapting as prices and inventory change.

When Z4 identifies a compelling purchasing opportunity, Pantheon HITL notifies the user with a recommendation and the reasoning behind it.
