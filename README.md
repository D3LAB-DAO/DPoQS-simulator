
# Quadratic Staking

## Example

|   | Validator 1 | Validator 2 | Validator 3 | 
|---|---|---|---|
|Stakings|[100]|[50, 50]|[10, 20, 30, 40]|
|Power|$\sqrt{100}=10$|$\sqrt{50}+\sqrt{50}=14.1421$|$\sqrt{10}+\sqrt{20}+\sqrt{30}+\sqrt{40}=19.4362$|

Let's say that there's a newly minted $100$ token here:

* Validator 1 will receive $100 * 10 / (10 + 14.1421 + 19.4362) = 22.95$ tokens
    * Delegator 1-1 ($100$) will receive $22.95 * 100 / (100) = 22.95$ tokens
* Validator 2 will receive $100 * 14.1421 / (10 + 14.1421 + 19.4362) = 32.45$ tokens
    * Delegator 2-1 ($50$) will receive $32.45 * 50 / (50 + 50) = 16.225$ tokens
    * Delegator 2-2 ($50$) will receive $32.45 * 50 / (50 + 50) = 16.225$ tokens
* Validator 3 will receive $100 * 19.4362 / (10 + 14.1421 + 19.4362) = 44.60$ tokens
    * Delegator 3-1 ($10$) will receive $44.60 * 10 / (10 + 20 + 30 + 40) = 4.46$ tokens
    * Delegator 3-2 ($20$) will receive $44.60 * 20 / (10 + 20 + 30 + 40) = 8.92$ tokens
    * Delegator 3-3 ($30$) will receive $44.60 * 30 / (10 + 20 + 30 + 40) = 13.38$ tokens
    * Delegator 3-4 ($40$) will receive $44.60 * 40 / (10 + 20 + 30 + 40) = 17.84$ tokens

<!--
* Level 1: Distributes Quadratic
    * Level 2: Distributes Linearly
-->

<!-- effect: more decentralizing -->

## Features

- Monopoly Cost for Decentralization - Represented as Nakamoto Coef.
- Quadratic Funding: More support, more rewards.

## Discussion

- Identity

## Notes

- Self-delegating is unavailable

# References

- Quadratic Voting
- Quadratic Funding
- Governor-C
- Do the Rich Get Richer? Fairness Analysis for Blockchain Incentives

## Special thanks to

- Chainlink

---

# How to Use

```bash
$ python simulator/<simulating_env>/run.py
```

For example, run `$ python simulator/all/run.py` to simulate **All Envs**.

`simulating_env`s:

* All environments: `all`
* PoS: `pos`
* DPoS: `dpos`
* DPoQS: `dpoqs`

# Simulator

Press `[H]` for help.

```
Simulator Commands
    [N]nextBlocks             <#_of_blocks>
    [B]bondedAmount           <bonded_amount>
    [S]stakingRatio           <%_of_staking_ratio>
    [V]validate_cost          <amount>
    [C]delegate_cost          <amount>

Logs Commands
    [P]step(window)           <size_of_step>
    [K]saveFigs               <name> [dpi]
    [L]saveLogs               <name>
```

> **NOTE**: Please input `:` before typing the command.

For example,

```
: N 10000000
```

Pass by 10,000,000 blocks.

```
: L test
```

Save `test_provs.csv` and `test_state.csv` files in `logs/`.

```
: K test 600
```

Save `test_provs.png` and `test_state.png` files in `plots/`.

<!--
# TODO
- set bondedAmount
- Cost norm dist.
- Smart agents (AI)
- Transition Progress Bar
-->

<!--
# TODO?
- N step: for loop -> one transition
- Console mode
- Genesis JSON
- Exception handling
- Supernova
    - Distributions
- x-axis w/ time (d/m/y)
-->
