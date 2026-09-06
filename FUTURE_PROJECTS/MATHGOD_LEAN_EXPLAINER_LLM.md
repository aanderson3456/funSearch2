# Mathgod Lean Explainer LLM: The Interactive Formal Mathematics Tutor

> *"Don't compete with the big dogs on raw benchmark solving speed. Build the most patient, structured, interactive explainer in the world."*

---

## 1. The Spark & Philosophy

### Origin
Ever since the early days of generative language models (sparked by the classic Computerphile demonstrations of GPT-2 generating token-by-token text sequences), it became apparent that transformer models are not just text generators—they are state-transition engines for human reasoning.

While the frontier AI labs (DeepMind with AlphaProof, DeepSeek-Prover, OpenAI) race to solve International Mathematical Olympiad (IMO) problems with massive compute and brute-force search, they produce:
- **Monolithic, unreadable tactic blobs**: 500-line obscure tactic scripts that pass the Lean kernel but teach the reader nothing.
- **Zero pedagogy**: If a proof fails or you don't understand a step, the model cannot patiently deconstruct *why*.
- **A high barrier to entry**: Mathematicians and students are intimidated by formal verification because compiler errors look like cryptic type theory hieroglyphics.

### The Mathgod Mission
**We do not need to compete on solving unsolved research conjectures.** 
Instead, Mathgod builds **The Socrates of Formal Mathematics**:
A dedicated, open-weight, interactive model fine-tuned to be an **infinitely patient, structured tutor** that weaves together **Natural Intuition (English)**, **Textbook Rigor ($\LaTeX$)**, and **Machine-Verified Truth (Lean 4)**.

---

## 2. The Tri-Modal Representation (English $\leftrightarrow$ $\LaTeX$ $\leftrightarrow$ Lean 4)

Every mathematical concept and proof step exists simultaneously in three planes. The Mathgod LLM treats translation between these three representations as its primary cognitive primitive:

```
                  ┌───────────────────────────────┐
                  │    Natural English Intuition  │
                  │   ("Zoom in until it's flat")  │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │        LaTeX Blackboard       │
                  │   lim_{h→0} (f(z+h)-f(z))/h   │
                  └───────────────┬───────────────┘
                                  │
                                  ▼
                  ┌───────────────────────────────┐
                  │       Lean 4 Kernel Truth     │
                  │   HasDerivAt f f' z           │
                  └───────────────────────────────┘
```

### Tri-Modal Example
| Plane | What It Shows | Example |
| :--- | :--- | :--- |
| **Natural English** | The high-level human intuition and strategic roadmap | *"We want to show the path derivative is zero everywhere, which forces the function to be locally constant along any curve connecting $z$ to $w$."* |
| **$\LaTeX$** | The standard blackboard algebraic derivation | $$f(z) - f(w) = \int_{0}^1 \frac{d}{dt} f(\gamma(t)) \, dt = \int_{0}^1 0 \, dt = 0$$ |
| **Lean 4** | The mechanically verified tactic state | `have h_deriv_zero : ∀ x, deriv f x = 0 := ...`<br>`rw [pathDeriv_eq_deriv]` |

---

## 3. Core Capabilities & User Experience

### A. The "Deconstruct This Tactic" Explainer
When Lean produces an opaque goal transition:
```lean
apply Classical.choose_spec (hf x)
```
The model provides an immediate interactive breakdown:
1. **What just happened:** *"We invoked the Axiom of Choice to extract the existential witness."*
2. **Before State:** What hypotheses and goals existed.
3. **After State:** How the goal transformed.
4. **Why this step:** Why a simpler tactic like `exact` or `simp` would have failed here.

### B. Patient Compiler Error Translation
Lean 4 compiler errors are notoriously dense (e.g., `type mismatch: expected (?m_1 + ?m_2), got ...`).
The Mathgod LLM parses the error through the Lean AST and explains:
> *"Lean is expecting a term of type `ℝ`, but you handed it `ℂ`. Notice that `(pathDeriv γ t₀).re` returns a real number, but when you added `I * ...`, Lean couldn't automatically cast the scalar. Wrap the real component in `( ... : ℂ)` or use `push_cast` to unify the types."*

### C. Interactive Socratic Proving
Instead of dumping a full 100-line proof at once:
1. **Roadmap first:** Proposes the overall outline with 2–3 sub-lemmas (`have h1 : ...`, `have h2 : ...`).
2. **Interactive Check-In:** Asks the user: *"Does this general outline match your geometric intuition before we formalize the $\epsilon$-$\delta$ bounds?"*
3. **Tactic-by-Tactic Guidance:** Lets the user try a move, validates it against a local Lean REPL, and offers gentle hints when stuck.

---

## 4. Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                       User Interface                        │
│          (Web Chat / VS Code Extension / Jupyter)           │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                 Mathgod Orchestration Engine                │
│    - Splits prompts into Strategy vs Tactic phases          │
│    - Manages multi-turn conversation history                │
└──────────────┬──────────────────────────────┬───────────────┘
               │                              │
               ▼                              ▼
┌──────────────────────────────┐┌──────────────────────────────┐
│       Mathgod Lean LLM       ││     Lean 4 REPL / LSP        │
│   (Fine-tuned 8B - 14B)      ││   (Live Kernel Verification) │
│ - Natural English Dialogue   ││ - Checks syntax & types      │
│ - LaTeX Mathematical Form    ││ - Returns real tactic states │
│ - Lean 4 Tactic Predictions  ││ - Catches syntax errors      │
└──────────────────────────────┘└──────────────────────────────┘
```

### 1. Ground Truth Verification Loop
The LLM is **never allowed to hallucinate Lean tactics in a vacuum**.
Every proposed tactic is fed directly to a background Lean 4 REPL process. If Lean throws an error, the error is fed back to the model internally to self-correct before presenting the final, verified step to the user.

### 2. Base Model Selection
- Start with a solid modern open base (e.g. **Llama-3-8B**, **Qwen-2.5-Coder-7B/14B**, or **DeepSeek-Coder**).
- Fine-tune on curated pairs of:
  - Human mathematical textbook proofs (Sarason, Spivak, Rudin, Artin).
  - Corresponding Mathlib formalizations.
  - Socratic dialogue transcripts explaining step-by-step logic.

---

## 5. Phased Roadmap

### Phase 1: Curated Dataset of Socratic Formal Math
- Build a dataset of 5,000+ tri-modal examples:
  `[Natural English Motivation] <-> [LaTeX Derivation] <-> [Annotated Lean 4 Proof]`.
- Pull real-world formalization examples from active repositories (e.g., Sarason Complex Analysis, VanEck sequences, Snakey formal proofs).

### Phase 2: Lean REPL Sidecar Tooling
- Develop a lightweight Python/Rust daemon that connects the LLM to a live Lean 4 language server.
- Expose tools: `eval_tactic`, `inspect_goal_state`, `explain_diagnostic`.

### Phase 3: Fine-Tuning & Evaluation
- Fine-tune the base model using LoRA / QLoRA on high-quality didactic data.
- Benchmark metric: **Didactic Clarity Score** (evaluated by human mathematicians) rather than purely automated benchmark solve rate.

### Phase 4: Frontend & IDE Integration
- Interactive Web App (Markdown + LaTeX rendering via KaTeX + Lean syntax highlighting).
- VS Code / Antigravity plugin for real-time side-by-side formalization pairing.

---

## 6. Summary Quote
> *"The future of mathematics isn't an AI that solves problems in the dark and hands you an incomprehensible certificate. The future is an AI that sits with you at the blackboard, understands your informal thoughts, and patiently teaches you how to make them completely bulletproof."*
