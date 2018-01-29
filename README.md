# About

This is a game for two to eight players, played locally (for example at a table) and on their smartphones.

# Story

You are a group of hackers, trying to get a valuable file. Of course there are rivalries in your group, so you want to be first to get your hands on this file. That's why you also make your mate's lives harder by blocking their resources. But be aware: Every attack on them has a toll on your system as well! Better recover once in a while.

# Rules

Each player chooses a username and joins the local game (found by its name).

The game runs in rounds.

## Goal

The goal is to get your own download to finish first. It advances automatically, dependent on the status of your system.

## Your System's Status

There are three measures that define what resources on your system are used: The available CPU usage, the available bandwidth and the available route. If only one of them is blocked (not available), your download can not proceed!

The lowest of the three values determines, how much you can download per round. So if you don't have enough CPU available, it will be a bottleneck.

## Attack Your Adversaries

You have three possible attacks every round. You can choose one of them and who to attack. The used attack is then replaced by a new one, the others you can still use in the next rounds. There is only one adversary you can attack each round - so better team up with other players!

## Recover Your System

Instead of attacking, you can also try to recover one of your system's resources. But you can not choose, which one. You'll have to take what's possible.

## Discuss

The game is not only about your own tactics and attacks, but also about discussing and teaming up with your friends! So try to convince them to help you, or make a deal that they will leave you alone just for this round!

# How To Start

Install Python 3 (latest version) and the bottle module. The latter you can do by typing

```Bash
$ pip install -r requirements.txt
```
in your favourite console.

Then, from the folder your `main.py` is in, start the server typing
```Bash
$ python main.py
```

The server then runs on your `localhost` at port `80`.
