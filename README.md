# Example

|   | Validator 1 | Validator 2 | Validator 3 | 
|---|---|---|---|
|Stakings|[100]|[50, 50]|[10, 20, 30, 40]|
|Power|$\sqrt{100}=10$|$\sqrt{50}+\sqrt{50}=14.1421$|$\sqrt{10}+\sqrt{20}+\sqrt{30}+\sqrt{40}=19.4362$|

Let's say that there's a newly minted $100$ token here:

* Validator 1 will receive $22.95$ tokens
    * Delegator 1-1 ($100$) will receive $22.95$ tokens
* Validator 2 will receive $32.45$ tokens
    * Delegator 2-1 ($50$) will receive $16.225$ tokens
    * Delegator 2-2 ($50$) will receive $16.225$ tokens
* Validator 3 will receive $44.60$ tokens
    * Delegator 3-1 ($10$) will receive $4.46$ tokens
    * Delegator 3-2 ($20$) will receive $8.92$ tokens
    * Delegator 3-3 ($30$) will receive $13.38$ tokens
    * Delegator 3-4 ($40$) will receive $17.84$ tokens

<!-- more decentralizing -->

---

# TODO

- Simulation env init. (fix and save)
- Cost norm dist.
- Smart agents

# Concept

- Monopoly Cost for Decentralization - Nakamoto Coef.
- Quadratic Funding: More support, more reward

# Discussion

- Identity

<!--
# Detail

- Delegate to same validator more than one is unavailable
- Self-delegating is unavailable
-->

<!--
# How to Use

```bash
$ python simulator/<simulating_env>/run.py
```

For example, run `$ python simulator/cosmos/run.py` to simulate **Cosmos Hub**.

`simulating_env`s:

* Cosmos (Hub): `cosmos`
* Supernova: TBA

# Simulator

Press `[H]` for help.

```
Cosmos Commands
    [N]nextBlocks             <#_of_blocks>
    [B]bondedAmount           <bonded_amount>
    [S]stakingRatio           <%_of_staking_ratio>

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

# TODO
- N step: for loop -> one transition
- Console mode
- Genesis JSON
- Exception handling
- Supernova
    - Distributions
- x-axis w/ time (d/m/y)
-->
