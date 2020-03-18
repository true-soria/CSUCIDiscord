import discord
import asyncio
import datetime

TOKEN = 'Njg5NTQwODM0NjEzNTI2NjEw.XnEq0g.I1t9uY8NgfXZ6VqK0JkS-50SioY'
client = discord.Client()

# Room IDs
WELCOME_ID = 689600552921071668
ROLE_SELECT_ID = 689607881716400248
ANNOUNCEMENTS_ID = 689891177289482298

# Preset messages
role_message = '__**This is a made up rule**__\n' \
          'please reply to my emojis.\n' \
          'they will unlock new channels\n\n' \
          ':test_tube:  for Chemistry,  :desktop:  for Comp Sci,\n' \
          ':infinity:  for Math,  :rocket:  for Physics,\n' \
          ':x:  to clear your selections\n'

# Command Strings
welcome_key = '$accept'

# Emoji Unicodes
testtube_emoji = "\U0001F9EA"
computer_emoji = "\U0001F5A5"
infinity_emoji = "\U0000267E"
rocket_emoji = "\U0001F680"
x_emoji = "\U0000274C"


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_reaction_add(reaction, member):
    if (member == client.user
            or reaction.message.channel != client.get_channel(ROLE_SELECT_ID)
            or reaction.message.author != client.user):
        return

    await asyncio.sleep(3)
    if reaction.emoji == testtube_emoji:
        role = discord.utils.get(member.guild.roles, name='Chemistry')
        await reaction.remove(member)
    elif reaction.emoji == computer_emoji:
        role = discord.utils.get(member.guild.roles, name='CompSci')
        await reaction.remove(member)
    elif reaction.emoji == infinity_emoji:
        role = discord.utils.get(member.guild.roles, name='Math')
        await reaction.remove(member)
    elif reaction.emoji == rocket_emoji:
        role = discord.utils.get(member.guild.roles, name='Physics')
        await reaction.remove(member)
    elif reaction.emoji == x_emoji:
        role_names = ['Chemistry', 'CompSci', 'Math', 'Physics']
        roles = {discord.utils.get(member.guild.roles, name=x) for x in role_names}
        for x in roles:
            await member.remove_roles(x)
        role = None
        await reaction.remove(member)
    else:
        role = None
        await reaction.remove(member)

    def is_not_me(m):
        return m.author != client.user
    await reaction.message.channel.purge(limit=1000, check=is_not_me)

    if role is not None:
        await member.add_roles(role)


@client.event
async def on_message(message):
    welcome = client.get_channel(WELCOME_ID)
    if message.author == client.user:
        return

    if message.channel == welcome:
        await welcome_desk(message)
    else:  # For messages from any other chat
        await dadum_check(message)


async def welcome_desk(message):
    if welcome_key in message.content:
        role = discord.utils.get(message.author.guild.roles, name='member')
    else:
        await message.delete()
        await message.channel.send('Nope. Try again.', delete_after=3)
        role = None

    if role is not None:
        await message.author.add_roles(role)
        await message.delete()


async def background_task():
    await client.wait_until_ready()
    # Discord serverHQ adjustment
    next_update = datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=8)))
    next_update = next_update.replace(minute=0, second=0, microsecond=0)
    role_select = client.get_channel(ROLE_SELECT_ID)
    while not client.is_closed():
        next_update += datetime.timedelta(minutes=30)
        await role_select.purge(limit=1000)
        role_post = await role_select.send(role_message)
        await role_post.add_reaction(testtube_emoji)
        await role_post.add_reaction(computer_emoji)
        await role_post.add_reaction(infinity_emoji)
        await role_post.add_reaction(rocket_emoji)
        await role_post.add_reaction(x_emoji)
        # wait
        await discord.utils.sleep_until(next_update)


async def dadum_check(message):
    if 'Adam' in message.content:
        await message.channel.send('*Dadam  ' + "\U0001F60E")


client.loop.create_task(background_task())
client.run(TOKEN)
