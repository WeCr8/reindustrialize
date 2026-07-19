---
name: quest-generator
description: Generate quest chains for REINDUSTRIALIZE mapped to real manufacturing workflows (setup, handoffs, MTConnect, presetting, robot install). Use for tutorials, tier gates, recovery quests, and Shop Mode real-data quests.
---

# Quest Generator

Every quest teaches a real workflow. If you can't name the real-world lesson in one
sentence, the quest doesn't ship.

## Procedure
1. Read `data/quests.json` and the tier table in GAME_DESIGN.md.
2. Classify: `tutorial` | `tier_gate` | `recovery` (post-failure) | `daily` |
   `shop_mode` (real-data-linked).
3. Write objective steps as verifiable sim events (the quest engine listens to the
   event bus — see game-core/src/quests/engine.ts).
4. Write Zach's intro + outro dialog (2-3 lines each, his voice).

## Schema
```json
{
  "id": "connect_machine_live", "type": "tier_gate", "tier": 3,
  "lesson": "Machine monitoring turns invisible downtime into money.",
  "steps": [
    {"event":"machine.purchased","filter":{"mtconnect":true}},
    {"event":"network.node_installed"},
    {"event":"machine.connected"},
    {"event":"dashboard.viewed","count":1}
  ],
  "rewards": {"coins":1500,"xp":400,"unlock":"oee_dashboard"},
  "zachIntro": ["That machine's been lying to you about its uptime.",
                "Let's wire it up and see the truth."],
  "zachOutro": ["See that idle bar? That's money leaking.",
                "Now we can fix what we can see."]
}
```

## Shop Mode quests (type: shop_mode)
Steps reference **bridge events** (`bridge.handoff_completed`, `bridge.machine_connected`,
`bridge.oee_improved`) which the server emits from real JobLine data. Rules:
- Rewards for real events are 2-3x Arcade equivalents (real behavior is the product).
- Never require actions that could pressure unsafe or rushed real-world work.
- Anonymize any leaderboard-visible outcome by default.

## Balance
- Tutorial chain <= 8 quests, first reward within 90 seconds of play.
- Tier gates require using the *previous* tier's lesson, not just buying things.
- Recovery quests always net-positive: failure must end in learning + partial refund.
