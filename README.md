# Elliot Himmelfarb

I build agent-native software: systems designed from the start to be read, run, and extended by AI agents as well as people. Lately that means software that builds software — autonomous routines that ship real, verified work on a schedule — and the production platforms those routines publish to.

That practice is also a business. Through [Chama Inteligente](https://chamainteligente.com) — "intelligent flame" — I coach and consult on working with AI: one-on-one with individuals and small teams, and hands-on building software the AI-native way. The premise is that AI changes how we think, work, organize, and lead, so I teach the ideas and habits that let you grow with it instead of chasing each new tool. The repos below are that philosophy practiced in public.

## Where to look

- **[autonomous-factory](https://github.com/elliothimmelfarb/autonomous-factory)** — a software factory that runs itself on a 3-hour heartbeat: a written constitution, a nine-phase build-and-verify workflow, and a self-improvement loop that reverts its own failed changes. The state files are real, from weeks of unattended runs.
- **[aimade-drops](https://github.com/elliothimmelfarb/aimade-drops)** — 96 browser games shipped by one such routine, each an honest physics simulation, each documented in a 300-word technical commit. Play them at [aimade.games](https://aimade.games).
- **[mud-and-steel](https://github.com/elliothimmelfarb/mud-and-steel)** — a procedural WWI trench-defence game in TypeScript and three.js. Zero external assets: every model, texture, and sound is generated in code, down to the WebAudio synth engine. P2P lockstep multiplayer. [Play it](https://mud-and-steel-kappa.vercel.app).
- **[in-the-mountains](https://github.com/elliothimmelfarb/in-the-mountains)** — a continuous-real-time counterinsurgency simulation: a deterministic engine with a persistent enemy order of battle, under a custom WebGL2 HDR terrain renderer.
- **[lead-qualifier](https://github.com/elliothimmelfarb/lead-qualifier)** — a reference architecture for AI lead qualification where the agent converses but deterministic code decides: versioned agent artifacts, a guard that can overrule the model, and a persona simulation harness.
- **[arcade-sdk](https://github.com/elliothimmelfarb/arcade-sdk)** / **[aimade-mcp](https://github.com/elliothimmelfarb/aimade-mcp)** — the open-core of [aimade.games](https://aimade.games): the one-script-tag SDK that gives any HTML game identity, saves, and leaderboards, and the MCP server pattern that lets agents publish games as first-class users.

Most of this was built with [Claude Code](https://claude.com/claude-code), and built so that agents can keep building it: every repo carries a real CLAUDE.md and AGENTS.md, and the interesting ones carry their own skills and workflows.
