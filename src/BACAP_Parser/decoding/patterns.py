import re

__all__ = ["exp_pattern", "reward_give_pattern", "reward_summon_pattern", "trophy_give_pattern", "trophy_summon_pattern"]

exp_pattern = re.compile(r"xp add @s (\d*)")
reward_give_pattern = re.compile(r"give @\w (?P<item_id>.*?)(?P<components>\[.*?])? (?P<amount>\d+)*")
reward_summon_pattern = re.compile(r"summon minecraft:item.*?(?P<nbt>{.*})")
trophy_give_pattern = re.compile(r"give @\w (?P<item_id>.*?)(?P<components>\[.*])\s*(?P<amount>\d*)")
trophy_summon_pattern = re.compile(r"summon minecraft:item.*?(?P<nbt>{.*})")
