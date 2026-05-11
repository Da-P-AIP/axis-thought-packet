# Universal Formula v0.1

The Universal Formula is a compact way to describe thinking as a structured process.

In this repository, the working form is:

```text
thought = state + transition + translation
```

## 1. Thought State

A thought state is the current structured condition of a mind, agent, or collaborative system.

It may include:

- focus
- intent
- assumptions
- constraints
- emotional or evaluative stance
- confidence
- unresolved questions

## 2. State Transition

A state transition describes how one thought state becomes another.

Examples:

- a question becomes a plan
- a plan becomes an implementation
- a private draft becomes a public specification
- one agent hands off context to another agent

## 3. State Translation

A state translation describes how a thought state is represented for another viewpoint or agent.

Examples:

- human notes translated into a machine-readable packet
- an AI planning state translated into a public README
- a private concept translated into a Zenodo-ready research artifact

## Working Formula

```text
T_next = translate(transition(T_current, action), target_context)
```

Where:

- `T_current` is the current thought state
- `action` is the operation applied to it
- `target_context` is the human, agent, system, or publication context receiving it
- `T_next` is the next usable thought state

