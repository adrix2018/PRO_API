from enum import Enum
import datetime as dt
import random
import os
import sqlite3
from typing import Union, Tuple, NamedTuple, Iterator, Any, List, Optional

timedelta = dt.timedelta
date = dt.date
datetime = dt.datetime
random = random
dateformat = "%Y-%m-%d %H:%M:%S"
sec_in_days = 86400
cwd = os.path.dirname(os.path.realpath(__file__)) + "\\"
create_uservar = """CREATE TABLE IF NOT EXISTS Var (
name text PRIMARY KEY ON CONFLICT REPLACE,
value numeric,
date text,
days integer
);"""

class Guild(NamedTuple):
	id: int
	name: str
	rank: int


class Region(Enum):
	kanto = 1
	johto = 2
	hoenn = 3
	sinnoh = 4


class PokedexEntry:
	@property
	def region(self)->Region: pass

	@property
	def id(self)->int: pass

	@property
	def caught(self)->bool: pass

	@property
	def evolved(self)->bool: pass


class Pokedex:
	def __iter__(self)->Iterator[PokedexEntry]: pass

	def __contains__(self, item: Union[str, int])->bool: pass

	def __getitem__(self, item: Union[str, int])->PokedexEntry: pass

	def add(self, item: Union[str, int], caught: bool=False, evolved: bool=False): pass


class PokemonSkills:
	def __contains__(self, item: str)->bool: pass


class Pokemon:
	def __init__(self, poke: Union[int, str], lvl: int, shiny: bool=False, form: int=0, ability: int=-1): pass

	@property
	def name(self)->str: pass

	@property
	def dex_id(self)->int: pass

	@property
	def shiny(self)->bool: pass

	@shiny.setter
	def shiny(self, val: bool): pass

	@property
	def pos(self)->int: pass

	@property
	def form(self)->int: pass

	@property
	def level(self)->int: pass

	@property
	def happiness(self)->int: pass

	@happiness.setter
	def happiness(self, val: int): pass

	@property
	def region(self)->Region: pass

	@property
	def iv_atk(self)->int: pass

	@iv_atk.setter
	def iv_atk(self, val: int): pass

	@property
	def iv_def(self)->int: pass

	@iv_def.setter
	def iv_def(self, val: int): pass

	@property
	def iv_spd(self)->int: pass

	@iv_spd.setter
	def iv_spd(self, val: int): pass

	@property
	def iv_spatk(self)->int: pass

	@iv_spatk.setter
	def iv_spatk(self, val: int): pass

	@property
	def iv_spdef(self)->int: pass

	@iv_spdef.setter
	def iv_spdef(self, val: int): pass

	@property
	def iv_hp(self)->int: pass

	@iv_hp.setter
	def iv_hp(self, val: int): pass

	@property
	def total_ivs(self)->int: pass

	@property
	def ev_atk(self)->int: pass

	@ev_atk.setter
	def ev_atk(self, val: int): pass

	@property
	def ev_def(self)->int: pass

	@ev_def.setter
	def ev_def(self, val: int): pass

	@property
	def ev_spd(self)->int: pass

	@ev_spd.setter
	def ev_spd(self, val: int): pass

	@property
	def ev_spatk(self)->int: pass

	@ev_spatk.setter
	def ev_spatk(self, val: int): pass

	@property
	def ev_spdef(self)->int: pass

	@ev_spdef.setter
	def ev_spdef(self, val: int): pass

	@property
	def ev_hp(self)->int: pass

	@ev_hp.setter
	def ev_hp(self, val: int): pass

	@property
	def hidden_power(self)->str: pass

	@property
	def skills(self)->PokemonSkills: pass

	@skills.setter
	def skills(self, val: List[str]): pass

	def can_learn(self, name: str)->bool: pass


class UserPokemon:
	@property
	def id(self)->int: pass

	@property
	def ot(self)->str: pass

	@property
	def name(self)->str: pass

	@property
	def dex_id(self)->int: pass

	@property
	def shiny(self)->bool: pass

	@property
	def pos(self)->int: pass

	@property
	def form(self)->int: pass

	@property
	def level(self)->int: pass

	@property
	def happiness(self)->int: pass

	@property
	def region(self)->Region: pass

	@property
	def iv_atk(self)->int: pass

	@property
	def iv_def(self)->int: pass

	@property
	def iv_spd(self)->int: pass

	@property
	def iv_spatk(self)->int: pass

	@property
	def iv_spdef(self)->int: pass

	@property
	def iv_hp(self)->int: pass

	@property
	def total_ivs(self)->int: pass

	@property
	def ev_atk(self)->int: pass

	@property
	def ev_def(self)->int: pass

	@property
	def ev_spd(self)->int: pass

	@property
	def ev_spatk(self)->int: pass

	@property
	def ev_spdef(self)->int: pass

	@property
	def ev_hp(self)->int: pass

	@property
	def hidden_power(self)->str: pass

	@property
	def skills(self)->PokemonSkills: pass

	def can_learn(self, name: str)->bool: pass

	def learn(self, name: str): pass


class Pokes:
	def __iter__(self)->Iterator[UserPokemon]: pass

	def __getitem__(self, item: int)->UserPokemon: pass

	def __delitem__(self, key: int): pass

	def __contains__(self, item: Union[int, str])->bool: pass

	def add(self, poke: Pokemon): pass

	def heal(self): pass


class NPC:
	@property
	def hide(self)->bool: pass

	@hide.setter
	def hide(self, val: bool): pass

	def hide_for(self, td: timedelta): pass

	team: List[Pokemon]

	@property
	def los(self)->int: pass

	def emote(self, eid: int): pass

	@property
	def last_fight(self)->datetime: pass


class BattleResult(Enum):
	pass


class UserVars:
	conn = None

	@staticmethod
	def delete_var(item: str):
		c = UserVars.conn.cursor()
		c.execute(f"DELETE FROM Var WHERE name='{item}'")
		UserVars.conn.commit()

	def __getattr__(self, item: str)->Any:
		c = UserVars.conn.cursor()
		c.execute(f"SELECT value, date FROM Var WHERE name='{item}'")
		res = c.fetchone()
		if res is None:
			return res

		# If res is not an expire var
		if res[1] is None:
			return res[0]

		# res is an expire var we must check for expiration
		if Expire.check_expire(item) is None:
			return None
		return res[0]

	def __setattr__(self, key: str, value: Any):
		c = UserVars.conn.cursor()
		c.execute(f"INSERT INTO Var(name, value) VALUES('{key}', {repr(value)})")
		UserVars.conn.commit()

	def set(self, key: str, value: Any, expire: timedelta):
		c = UserVars.conn.cursor()
		c.execute(f"INSERT INTO Var VALUES('{key}', {repr(value)}, '{datetime.now().strftime(dateformat)}', {expire.total_seconds()/sec_in_days})")
		UserVars.conn.commit()


class Expire:
	@staticmethod
	def check_expire(item: str) -> Union[None, timedelta]:
		c = UserVars.conn.cursor()
		c.execute(f"SELECT date, days FROM Var WHERE name='{item}'")
		res = c.fetchone()
		if res is None:
			return res
		# parse the set date
		dateobj = datetime.strptime(res[0], dateformat)
		# get the old delta
		olddelta = timedelta(seconds=res[1]*sec_in_days)
		# compare the set date with now
		datedelta = datetime.now() - dateobj
		# compare this with the original delta ("days")
		newdelta = olddelta - datedelta
		if newdelta.total_seconds() < 0:
			UserVars.delete_var(item)
			return None
		return newdelta

	def __getattr__(self, item: str) -> timedelta:
		return Expire.check_expire(item)

UserVars.conn = sqlite3.connect(f'{cwd}user_var.db')
c = UserVars.conn.cursor()
c.execute(create_uservar)


class Items:
	def __iter__(self)->Iterator[Tuple[str, int]]: pass

	def __getitem__(self, item: str)->int: pass

	def __setitem__(self, key: str, value: int): pass

	def __delitem__(self, key: str): pass

	def __contains__(self, item: str)->bool: pass


class User:
	def say(self, msg: str):
		print(msg)

	def teleport(self, mname: str, x: int, y: int)->bool: pass

	def battle(self, a: Union[Pokemon, NPC],
			   noexp: Optional[bool]=False,
			   no_teleport: Optional[bool]=False)->BattleResult: pass

	def say_system(self, msg: str): pass

	def play_music(self, mid: int): pass

	def play_sound(self, sid: int): pass

	def play_cry(self, cid: int): pass

	def shop(self, shop_id: int): pass

	def pause(self)->Union[bool, None]: pass

	def select(self, question: str, choices: list)->Tuple[int, str]:
		print(question)
		for i, choice in enumerate(choices):
			print(f"{i}: {choice}")
		while True:
			choice = input("> ")
			if choice.isdecimal():
				val = int(choice)
				if 0 <= val < len(choices):
					return val, choices[val]
				else:
					print(f"{val} is out of the range of possible choices [0,{len(choices)-1}]")
			else:
				print("Select your choice by typing the appropriate number.")

	def select_pokemon(self, question: str)->UserPokemon: pass

	id: int
	username: str
	position: Tuple[int, int]
	security: Tuple[int, str]
	money: int
	coins: int
	playtime: timedelta
	guild: Guild
	vars = UserVars()
	expire = Expire()
	pokes: Pokes
	team: Pokes
	items: Items
	dex: Pokedex
	registration_date: date
	membership: bool
	black_membership: bool


class NPCs:
	@staticmethod
	def __getitem__(item: int)->NPC: pass


npc = NPC()
npcs = NPCs()
user = User()
