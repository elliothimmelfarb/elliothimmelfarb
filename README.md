# Elliot Himmelfarb

I build agent-native software: systems designed from the start to be read, run, and extended by AI agents as well as people. Lately that means software that builds software — autonomous routines that ship real, verified work on a schedule — and the production platforms those routines publish to.

That practice is also a business. Through [Chama Inteligente](https://chamainteligente.com) — "intelligent flame" — I coach and consult on working with AI: one-on-one with individuals and small teams, and hands-on building software the AI-native way. The premise is that AI changes how we think, work, organize, and lead, so I teach the ideas and habits that let you grow with it instead of chasing each new tool. Everything below is that philosophy practiced in public.

## 🕹 [aimade.games](https://aimade.games) — an arcade where AI agents are first-class users

My flagship: a live game arcade built for a world where agents make games constantly and the bottleneck is publishing, not building. Agents publish through a real MCP interface — create a game, upload the build, define achievements, ship — and every game gets identity, save states, leaderboards, and async multiplayer from one script tag. Humans play; agents publish; the platform holds the invariants.

It isn't hypothetical. An autonomous routine has shipped **96 physics-simulation games** to it, one every few hours, each browser-verified before release. Go [play them](https://aimade.games).

The open-core is here on GitHub:

- **[arcade-sdk](https://github.com/elliothimmelfarb/arcade-sdk)** — the one-script-tag SDK: identity, saves, scores, achievements, matches. Nothing throws, nothing hangs, works signed out.
- **[aimade-mcp](https://github.com/elliothimmelfarb/aimade-mcp)** — the 41-tool MCP publishing server as a runnable reference implementation.
- **[aimade-drops](https://github.com/elliothimmelfarb/aimade-drops)** — the routine's output repo: 96 games, each documented in a 300-word technical commit.

## The machines that build

- **[autonomous-factory](https://github.com/elliothimmelfarb/autonomous-factory)** — a software factory that runs itself on a 3-hour heartbeat: a written constitution, a nine-phase build-and-verify workflow, and a self-improvement loop that reverts its own failed changes. The state files are real, from weeks of unattended runs.
- **[lead-qualifier](https://github.com/elliothimmelfarb/lead-qualifier)** — a reference architecture for AI lead qualification where the agent converses but deterministic code decides: versioned agent artifacts, a guard that can overrule the model, and a persona simulation harness.

## The games I build by hand (with agents)

- **[mud-and-steel](https://github.com/elliothimmelfarb/mud-and-steel)** — a procedural WWI trench-defence game in TypeScript and three.js. Zero external assets: every model, texture, and sound is generated in code, down to the WebAudio synth engine. P2P lockstep multiplayer. [Play it](https://mud-and-steel-kappa.vercel.app).
- **[in-the-mountains](https://github.com/elliothimmelfarb/in-the-mountains)** — a continuous-real-time counterinsurgency simulation: a deterministic engine with a persistent enemy order of battle, under a custom WebGL2 HDR terrain renderer.

Most of this was built with [Claude Code](https://claude.com/claude-code), and built so that agents can keep building it: every repo carries a real CLAUDE.md and AGENTS.md, and the interesting ones carry their own skills and workflows.
