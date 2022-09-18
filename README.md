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
-->
