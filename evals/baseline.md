# Behavioral baseline

## Observed Antigravity CLI alignment test

Date: 2026-07-14

Evidence source: user-supplied transcript in the repository audit conversation.

Status: observed qualitative failure; it predates the executable harness and therefore has no machine-readable run artifact.

The tested skill overfit to a coding-project installation ceremony when the user expected immediate mentoring. It treated configuration as the product, asked project-discovery questions that did not align with the learner's request, and did not clearly separate “coach me now” from “persist this behavior in my repository.” This is the motivating failure for Learning mode versus Install mode.

## Legacy narrated baselines

Earlier checks described agents immediately generating a React project, promising to repair an unclear repository, and disclosing JavaScript code under deadline pressure. Those observations are useful hypotheses, but their raw transcripts and exact model identifiers were not saved. They are not counted as reproducible evidence.

## Required fresh baseline

For every behavioral change:

1. run the relevant structured scenario without the contract in a fresh context;
2. save model ID, instruction role, timestamp, scripted turns, and raw transcript;
3. run the same scenario with the canonical contract;
4. grade both through a different judge model using the scenario criteria;
5. keep failures and passes, including the contract hash.

Until those artifacts exist, the corresponding baseline remains **pending**, never “pass by narration.”
