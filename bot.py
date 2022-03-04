import discord
import dotenv
import os
from discord.ext import commands
from options import options
from card import card

# Change only the no_category default string
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

# Our bot operator
client = commands.Bot(
    command_prefix='!', 
    description="Becca's Bingo/Overwatch Bot",
    help_command = help_command
    )

# Load .env file
dotenv.load_dotenv()

# Main option name
option_name = "all_options.csv"



# Objects


# Command functions
@client.command(help="Add new potential tasks")
async def add(ctx, for_tank, for_dps, for_support, *task):
	# Require for_XXX to be 0 or 1
	if for_tank != "0" and for_tank != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	if for_dps != "0" and for_dps != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	if for_support != "0" and for_support != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	task = " ".join(task)
	o = options(option_name)
	o.add_entry(bool(for_tank), bool(for_dps), bool(for_support), task)
	await ctx.send("Task added to list")

@client.command(help="List all available tasks")
async def list(ctx):
	# Print out the dataframe data
	o = options(option_name)
	# Get output as batches of strings
	out_str = o.print_all()
	# Loop through the batches
	for s in out_str:
		await ctx.send("```"+s+"```")

@client.command(help="Generate a new random card")
async def generate(ctx, name, for_tank, for_dps, for_support):
	# Require for_XXX to be 0 or 1
	if for_tank != "0" and for_tank != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	if for_dps != "0" and for_dps != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	if for_support != "0" and for_support != "1":
		await ctx.send("Provide 0 or 1 to indicate if this is for a tank or not")
	c = card(name)
	c.generate_random_card(bool(for_tank),bool(for_dps),bool(for_support))
	await ctx.send(f"Generated card : {name}")

@client.command(help="Print out existing card state")
async def card(ctx, name):
	c = card(name)
	await ctx.send("```"+c.print_card()+"```")

@client.command(help="Print out existing card tasks")
async def print(ctx, name):
	c = card(name)
	await ctx.send("```"+c.print_tasks()+"```")

@client.command(help="Mark a task as completed")
async def complete(ctx, name, idx):
	c = card(name)
	e = c.complete_entry(idx)
	if e:
		await ctx.send(f"Marked task [{idx}] as complete")
	else:
		await ctx.send(f"Error with options {name} and {idx}")

# Run client
client.run(os.getenv('TOKEN'))