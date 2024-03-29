import discord
import dotenv
import os
import functools
import typing
from discord.ext import commands
from assistant import assistant

import logging
logging.basicConfig(level=logging.DEBUG)

# Change only the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

# Our bot operator
intents = discord.Intents.default()
intents.members = True
intents.typing = True
intents.presences = True
intents.message_content = True

client = commands.Bot(
	intents=intents,
    command_prefix='!', 
    description="Becca's Bingo/Overwatch Bot",
    help_command = help_command
    )

# Load .env file
dotenv.load_dotenv()

# Main option name
option_name = "all_options.csv"

# Special function to async sync functions
async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
	func = functools.partial(blocking_func, *args, **kwargs)
	return await client.loop.run_in_executor(None, func)

# Command functions
@client.command(help="Add new potential tasks")
async def add(ctx, for_tank, for_dps, for_support, *task):
	from options import options
	# Require for_XXX to be 0 or 1
	if for_tank != "0" and for_tank != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	if for_dps != "0" and for_dps != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	if for_support != "0" and for_support != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	task = " ".join(task)
	o = options(option_name)
	o.add_entry(bool(int(for_tank)), bool(int(for_dps)), bool(int(for_support)), task)
	await ctx.send("Task added to list")

@client.command(help="List all available tasks")
async def list(ctx):
	from options import options
	# Print out the dataframe data
	o = options(option_name)
	# Get output as batches of strings
	out_str = o.print_all()
	# Loop through the batches
	for s in out_str:
		await ctx.send("```"+s+"```")

@client.command(help="Generate a new random card")
async def generate(ctx, name, for_tank, for_dps, for_support):
	from card import card
	# Require for_XXX to be 0 or 1
	if for_tank != "0" and for_tank != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	if for_dps != "0" and for_dps != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	if for_support != "0" and for_support != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	c = card(name)
	c.generate_random_card(bool(int(for_tank)),bool(int(for_dps)),bool(int(for_support)))
	await ctx.send(f"Generated card : {name}")

@client.command(help="Print out existing card state")
async def card(ctx, name):
	from card import card
	c = card(name)
	await ctx.send("```"+c.print_card()+"```")

@client.command(help="Print out existing card tasks")
async def print(ctx, name):
	from card import card
	c = card(name)
	await ctx.send("```diff\n"+c.print_tasks()+"```")

@client.command(help="Mark a task as completed")
async def complete(ctx, name, idx):
	from card import card
	c = card(name)
	e,completed = c.complete_entry(idx, True)
	if e:
		await ctx.send(f"Marked task [{idx}] as complete")
		for co in completed:
			await ctx.send(f"COMPLETED {co}")
	else:
		await ctx.send(f"Error with options {name} and {idx}")

@client.command(help="Mark a task as not completeted")
async def incomplete(ctx, name, idx):
	from card import card
	c = card(name)
	e,completed = c.complete_entry(idx, False)
	if e:
		await ctx.send(f"Marked task [{idx}] as incomplete")
		for co in completed:
			await ctx.send(f"COMPLETED {co}")
	else:
		await ctx.send(f"Error with options {name} and {idx}")

@client.command(help="Get a role")
async def role(ctx):
	import hero
	r = hero.get_role()
	await ctx.send(f"```{r}```")

@client.command(help="Get a random hero")
async def hero(ctx):
	import hero
	r = hero.get_any_hero()
	await ctx.send(f"```{r}```")

@client.command(help="Get a random support")
async def support(ctx):
	import hero
	r = hero.get_any_support()
	await ctx.send(f"```{r}```")

@client.command(help="Get a random dps")
async def dps(ctx):
	import hero
	r = hero.get_any_dps()
	await ctx.send(f"```{r}```")

@client.command(help="Get a random tank")
async def tank(ctx):
	import hero
	r = hero.get_any_tank()
	await ctx.send(f"```{r}```")

@client.command(hidden=True)
async def fuck(ctx, *x):
	await ctx.send("Naughty naughty")

@client.command(hidden=True)
async def hummus(ctx, *x):
	await ctx.send("That's wierd")

@client.command(hidden=True)
async def sucks(ctx, *x):
	await ctx.send("Don't be rude")

# New using assistant (assuming not to expensive...)
@client.command(help="Ask AI bot a question")
async def question(ctx, *question):
	ai = assistant()
	author = ctx.author.display_name
	logging.info(author)
	async with ctx.channel.typing():
		message_in = " ".join(question)
		a = await run_blocking(ai.interact,author,message_in)
	await ctx.send(a)

@client.event
async def on_message(message):
	if message.author.bot == False and client.user.mentioned_in(message):
		# Bot was mentioned, so pull the singlton
		ai = assistant()
		author = message.author.display_name
		# Hack to help resolve tagging into name
		message_in = message.content.replace("<@&"+str(client.user.id)+">", client.user.name)
		async with message.channel.typing():
			a = await run_blocking(ai.interact,author,message_in)
		await message.channel.send(a)
	else:
		await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send(f"**What a strange command to use, {ctx.message.author.display_name}...**")
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send('**Please pass in all requirements.**')
	if isinstance(error, commands.MissingPermissions):
		await ctx.send("**You dont have all the requirements or permissions for using this command :angry:**")




# Run client
client.run(os.getenv('TOKEN'))