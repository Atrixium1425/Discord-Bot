import discord, random, time, praw, datetime, asyncio, pyjokes, googletrans
from discord.ext import commands, tasks
from enum import IntEnum

intents = discord.Intents.default()
intents.members = True

prefix = "!"
client = commands.Bot(command_prefix = prefix, intents = intents)
client.remove_command("help")

f = open("rules.txt", "r")
rules = f.readlines()

filteredWords = ["" '''
    "nigga", "niger", "nigger", "nigel", "niga",
    "n1gga", "n1ger", "n1ger", "n1gel", "n1ga",
    "shit", "sh1t", "shite", "sh1te"''']

white = 0xeeffee

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game("Cum Clicker 1.0.0a"))

    clearer.start()
    
    guild = client.get_guild(850027913461366834)
    owner = client.get_user(guild.owner.id)
    interval = 600 * 6
    reminder.change_interval(seconds = interval)
    reminder.start(member = owner, interval = interval)
    
    print("Virus activated")    #START LOOPS (FRIENDCHECKER, CLEARENTRY, PROCRASTINATION REMINDER) , ON MEMBER JOIN/LEAVE DO MESSAGE THING WITH MENTION AND GAME CHANNEL!!,  rate and choose funcs

@client.event
async def on_member_join(member):
    '''If member is a friend of owner, give them friend  roles
    frole = discord.utils.get(member.guild.roles, name = "Friend")
    owner = client.get_user(guild.owner.id)
    friends =  await member.mutual_friends()
    if owner in friends:
        await member.add_roles(frole)'''
    
    #role = discord.utils.get(member.guild.roles, name = "Baby Sperm")
    #await member.add_roles(role)

@client.event
async def on_member_remove(member):
    guild = client.get_guild(850027913461366834)
    channel = guild.get_channel(850043463604764712)
    embed = discord.Embed(title = "Goodbye!", description = f"Goodbye {member.mention}. Hope you enjoyed your stay with us, if possible please rejoin: https://discord.gg/DgagPvkMWb.", colour = white)   
    await member.send(embed = embed)  

'''@client.command(name = "friendchecker", description = "no")

@commands.has_permissions(manage_roles = True)
@tasks.loop(seconds = 60)
async def friendchecker():
    guild = client.get_guild(850027913461366834)
    members = guild.fetch_members(limit = 1000)
    role = discord.utils.get(member.guild.roles, name = "Friend")
    checker.start(members)
    for member in members:
        if member.is_friend():
            await member.add_roles(role)
'''

@client.command(name = "clearentryway", description = "no")
@commands.has_permissions(manage_messages = True)
async def clearentryway(ctx,enabled : str = "start",cleartime = 300):
    if enabled.lower() == "stop":
        clearer.cancel()
    elif enabled.lower() == "start":
        clearer.change_interval(seconds = float(cleartime))
        clearer.start()

@tasks.loop(seconds = 300)
async def clearer():
    guild = client.get_guild(850027913461366834)
    channel = guild.get_channel(850594150071140403)
    await channel.purge(limit = 1000)

@client.command()
@commands.has_permissions(administrator = True)
async def remind(ctx,member : discord.Member = "", enabled : str = "start", interval = 600):
    if member == "":
        member = client.get_user(ctx.author.id)
    if enabled.lower() == "stop":
        reminder.cancel()
    elif enabled.lower() == "start":
        reminder.change_interval(seconds = float(interval))
        reminder.start(member, interval)
        
@tasks.loop(seconds = 600)
async def reminder(member, interval):
    mbed = discord.Embed(title = f'Reminding you to stop procrastinating every {interval / 60} minutes.', description = 'If you want to deactivate this, enter the command `!remind stop`')
    mbed.set_author(name = 'Procrastination Police')
    await member.send(embed=mbed)

'''@client.command()
async def remind(ctx, enabled = "start", interval = 600):
    member = client.get_user(ctx.author.id)
    if enabled.lower() == "stop":
        reminder.cancel()
    elif enabled.lower() == "start":
        reminder.change_interval(seconds = float(interval))
        reminder.start(member, interval)'''
    
@client.event
async def on_message(msg):
    for word in filteredWords:
        if word in msg.content:
            await msg.delete()

    '''if ":" == msg.content[0] and ":" == msg.content[-1]:
        emojiName = msg.content[1:-1]
        for emoji in msg.guild.emojis:
            if emojiName == emoji.name:
                await msg.channel.send(str(emoji))
                await msg.delete()
                break

    if "cool" in msg.content:
        await msg.add_reaction("<:cool:850142621954736159>")'''

    await client.process_commands(msg)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title = "**Missing Permissions!**", description = f"You dont have the power to do that '-'.", colour = discord.Colour.red())  
        await ctx.send(embed = embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title = "**Missing Required Argument!**", description = f"Please enter all the required arguments.", colour = discord.Colour.red()) 
        await ctx.send(embed = embed)
    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = "**Command Not Found!**", description = f"That command does not exst '-'.", colour = discord.Colour.red())
        await ctx.send(embed = embed)
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(title = "**Bad Argument!**", description = f"Invalid argument '-'.", colour = discord.Colour.red())
        await ctx.send(embed = embed)
    else:
        raise error

@client.command(name = "help", description = "Helps you...?")
async def help(ctx, cmd : str = None):
    if cmd != None:
        for command in client.commands:
            if cmd.lower() == command.name.lower():
                
                paramString = f"{prefix}{command.name.lower()}"
                aliasString = str(command.aliases)[1:-1]
                
                for param in command.clean_params:
                    paramString += f" <{param}> "

                paramString = paramString[:-1]
                
                if len(command.clean_params) == 0:
                    paramString = f"{prefix}{command.name.lower()}"
                    
                embed = discord.Embed(title = f"Help - {command.name}", description = command.description, colour = white)   
                embed.add_field(name = "Syntax", value = paramString, inline = False)
                embed.add_field(name = "Aliases", value = aliasString, inline = False)
                await ctx.message.delete()
                await ctx.send(embed = embed)
    else:           
        embed = discord.Embed(title = "Commands", description = f"Type `{prefix}help <command>` for more help e.g. `!help kick`", colour = white)           

        #for cmd in client.commands:
            #embed.add_field(name = cmd.name.lower(), value = cmd.description, inline = False)
        embed.add_field(name = "Info", value = "`help` `rule` `ping` `info` `server`", inline = False)
        embed.add_field(name = "Server", value = "`giveaway`", inline = False)
        embed.add_field(name = "Moderation", value = "`clear` `mute` `unmute` `kick` `ban` `unban`", inline = False)
        embed.add_field(name = "Fun", value = "`choose` `coin` `cat` `dog` `eightball` `codejoke` `joke` `meme` `poll` `rate` `rps` `cps` emoji fortune throw", inline = False)
        embed.add_field(name = "Search", value = "`subreddit`", inline = False)
        embed.add_field(name = "Misc", value = "`translate` remindme", inline = False)
        await ctx.message.delete()
        await ctx.send(embed = embed)

@client.command(name = "wakeandrape", description = "Used to get the role Baby Boi.")
async def wakeandrape(ctx):
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name = "Baby Boi")
    if not role in member.roles:
        await member.add_roles(role)

        #Welcome
        guild = client.get_guild(850027913461366834)
        welcomechannel = guild.get_channel(850043463604764712)
        rulechannel = guild.get_channel(850029975301914644).mention
        gamechannel = guild.get_channel(850027913461366837).mention
        embed = discord.Embed(title = f"Welcome to the {guild.name} server!", description = f"Welcome {member.mention}. Please read {rulechannel} to get up to speed and if you're just here for Cum Clicker {gamechannel} is your jig.", colour = white)   
        await welcomechannel.send(embed = embed)
    await ctx.message.delete()

@client.command(name = "ping", description = "Used to test bot response time.", aliases = ["p"])
async def ping(ctx):
    embed = discord.Embed(title = "", description = f":information_source:  **|**  Pong! - Time taken: **{str(round(client.latency * 1000))}ms**", colour = white)   
    await ctx.send(embed = embed)

@client.command(name = "rule", description = "no", aliases = ["rules"])
async def rule(ctx,*,number):
    await ctx.send(rules[int(number)-1])

@client.command(name = "clear", description = "Clears messages.", aliases = ["c", "purge", "nuke"])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount = 2):
    if amount == "all":
        amount = 10000
    await ctx.channel.purge(limit = amount)

@client.command(name = "kick", description = "Kick a user and specify a kick message that will show up in kick logs and DM them the message.", aliases = ["k"])
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member,*,reason = "No reason provided"):
    actionschannel= client.get_guild(850027913461366834).get_channel(855770839958159381)
    embed = discord.Embed(title = "Moderation: Kick", description = f"**Moderator:** {client.get_user(ctx.author.id)} ({ctx.author.id})\n**Offender:** {member} ({member.id})\n**Reason:** {reason}", colour = discord.Colour.red())
    embed.set_footer(text = time.strftime("%d/%m/%Y"))
    await member.send(embed = embed)
    await actionschannel.send(embed = embed)
    await member.kick(reason = reason)
    
@client.command(name = "ban", description = "Ban a user and specify a ban message that will show up in any audit/ban logs and DM them the message.", aliases = ["b"])
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member,*,reason = "No reason provided"):
    actionschannel= client.get_guild(850027913461366834).get_channel(855770839958159381)
    embed = discord.Embed(title = "Moderation: Ban", description = f"**Moderator:** {client.get_user(ctx.author.id)} ({ctx.author.id})\n**Offender:** {member} ({member.id})\n**Reason:** {reason}", colour = discord.Colour.red())  
    embed.set_footer(text = time.strftime("%d/%m/%Y"))
    await member.send(embed = embed)
    await actionschannel.send(embed = embed)
    await member.ban(reason = reason)
    
@client.command(name = "unban", description = "Unbans a user from the server.", aliases=["ub"])
@commands.has_permissions(ban_members = True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_disc = member.split("#")

    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator) == (member_name, member_disc):
            await ctx.guild.unban(user)
            await ctx.send(f"{member} has been unbanned!")
            await member.send(f"{member} has been unbanned!")
            return
        
    await ctx.send(f"{member} was not found!")

@client.command(name = "mute", description = "Mutes a user.", aliases=["m"])
@commands.has_permissions(kick_members = True)
async def mute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(850105985770192906)

    await member.add_roles(muted_role)

    await ctx.send(f"{member.mention} has been muted")

@client.command(name = "unmute", description = "Unmutes a user", aliases=["um"])
@commands.has_permissions(kick_members = True)
async def unmute(ctx, member : discord.Member):
    muted_role = ctx.guild.get_role(850105985770192906)

    await member.remove_roles(muted_role)

    await ctx.send(f"{member.mention} has been unmuted")

@client.command(name = "info", description = "Shows info about a user.", aliases=["user", "whois"])
async def info(ctx, member : discord.Member): 
    embed = discord.Embed(title = member.name, description = member.mention, colour = white)   

    embed.add_field(name = "ID", value = member.id, inline = False)
    embed.add_field(name = "Nickname", value = member.display_name, inline = False)
    embed.add_field(name = "Account Created", value = member.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    embed.add_field(name = "Join Date", value = member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)

    roles = [role for role in member.roles]

    embed.add_field(name = f"Roles [{len(roles)}]", value = " ".join([role.mention for role in roles]), inline = False)

    embed.set_thumbnail(url = member.avatar_url)
    embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Requested by {ctx.author.name}")
    
    await ctx.send(embed = embed)

@client.command(name = "serverinfo", description = "Shows info about the current server.", aliases=["server"])
async def serverinfo(ctx): 
    embed = discord.Embed(title = f"{ctx.guild.name}", description = ".", colour = white)   
    roleCount = len(ctx.guild.roles)
    bots = [bot.mention for bot in ctx.guild.members if bot.bot]

    embed.set_thumbnail(url = str(ctx.guild.icon_url))
    
    embed.add_field(name = f"ID: **{ctx.guild.id}**", value = "⠀", inline = False)
    embed.add_field(name = "Verification Level", value = str(ctx.guild.verification_level).capitalize(), inline = False)
    embed.add_field(name = "Region", value =  str(ctx.guild.region).capitalize(), inline = False)
    categories = ctx.guild.categories
    text_channels = 0
    news_channels = 0
    for channel in ctx.guild.text_channels:
        if channel.is_news():
            news_channels += 1
        else:
            text_channels += 1
    embed.add_field(name = f"Channels[{len(categories)+text_channels+news_channels}]",
                    value = f"Category: {len(categories)}\nText: {text_channels}\nNews: {news_channels}",
                    inline = False)
    embed.add_field(name = "Server Owner", value = str(ctx.guild.owner.mention), inline = False)
    embed.add_field(name = "Created On", value = ctx.guild.created_at.strftime("%a, %#d %B %Y, %I:%M %p UTC"), inline = False)
    embed.add_field(name = f"Roles[{len(ctx.guild.roles)}]", value = "⠀", inline = False)

    embed.set_footer(icon_url = str(ctx.author.avatar_url), text = f"Requested by {ctx.author.name}")

    await ctx.send(embed = embed)

reddit = praw.Reddit(client_id = "fFuv-xo1bLxRag",
                     client_secret = "no",
                     username = "AtrixiumAlt",
                     password = "no",
                     user_agent = "MemeBot")

@client.command(name = "subreddit", description = ".", aliases = ["redditpost"])
async def subreddit(ctx, subredditname : str):
    subred = reddit.subreddit(subredditname)
    allSubs = []

    top = subred.top(limit = 50)

    for sub in top:
        allSubs.append(sub)

    randomSub = random.choice(allSubs)
    name = randomSub.title
    url = randomSub.url

    embed = discord.Embed(title = name)
    embed.set_image(url = url)

    await ctx.send(embed = embed)
    
@client.command(name = "meme", description = "( ͡° ͜ʖ ͡°)")
async def meme(ctx):
    subred = reddit.subreddit("memes")
    allSubs = []

    top = subred.top(limit = 50)

    for sub in top:
        allSubs.append(sub)

    randomSub = random.choice(allSubs)
    name = randomSub.title
    url = randomSub.url

    embed = discord.Embed(title = name)
    embed.set_image(url = url)

    await ctx.send(embed = embed)

@client.command(name = "joke", description = "haha", aliases = ["dadjoke"])
async def joke(ctx):
    j = open('jokes.txt', 'r', encoding="utf8")
    jokes = j.readlines()
    embed = discord.Embed(title = "", description = random.choice(jokes), colour = white)
    await ctx.send(embed = embed)

@client.command(name = "codejoke", description = "error: haha", aliases = ["programjoke"])
async def codejoke(ctx):
    embed = discord.Embed(title = "", description = pyjokes.get_joke(), colour = white)
    await ctx.send(embed = embed)

@client.command(name = "cat", description = "Gives you a random cat :3", aliases = ["catto", "kitty", "neko"])
async def cat(ctx):
    subred = reddit.subreddit("cat")
    allSubs = []

    top = subred.top(limit = 50)

    for sub in top:
        allSubs.append(sub)

    randomSub = random.choice(allSubs)
    name = randomSub.title
    url = randomSub.url

    embed = discord.Embed(title = name)
    embed.set_image(url = url)

    await ctx.send(embed = embed)

@client.command(name = "dog", description = "Gives you a random dog :3", aliases = ["doggo", "puppy", "inu"])
async def dog(ctx):
    subred = reddit.subreddit("dog")
    allSubs = []

    top = subred.top(limit = 50)

    for sub in top:
        allSubs.append(sub)

    randomSub = random.choice(allSubs)
    name = randomSub.title
    url = randomSub.url

    embed = discord.Embed(title = name)
    embed.set_image(url = url)

    await ctx.send(embed = embed)

@client.command(name = "emoji", description = "no", aliases=["e"])
async def emoji(ctx):
    await ctx.send(":cool:")

@client.command(name = "poll", description = "no", aliases=["pl"])
async def poll(ctx,*,msg):
    channel = ctx.channel
    try:
        op1, op2 = msg.split("or")
        txt = f"React with ✅ for {op1} or ❎ for {op2}"
    except:
        await channel.send("Correct Syntax: [Choice1] or [Choice2]")
        return

    embed = discord.Embed(title = "Poll", description = txt, colour = white)   
    message_ = await channel.send(embed = embed)
    await message_.add_reaction("✅")
    await message_.add_reaction("❎")
    await ctx.message.delete()
#Fun?
@client.command(name = "eightball", description = "Asks the 8ball a question.", aliases = ["8ball","8b"])
async def eightball(ctx,*,question):
    responses = ("It is Certain.","It is decidedly so.","Without a doubt.","Yes definitely.","You may rely on it.","As I see it, yes.","Most likely.","Outlook good.","Yes.","Signs point to yes.","Reply hazy, try again.","Ask again later.","Better not tell you now.","Cannot predict now.","Concentrate and ask again.","Don't count on it.","My reply is no.","My sources say no.","Outlook not so good.","Very doubtful.")
    embed = discord.Embed(title = ":8ball:8ball", description = random.choice(responses), colour = white)    
    await ctx.send(embed = embed)

@client.command(name = "coin", description = "Flips one or more coins.", aliases = ["coinflip","cointoss"])
async def coin(ctx,*,number = 1):
    choices = ["heads", "tails"]
    if number > 1:
        num1 = random.randint(0,number)
        num2 = number - num1
        embed = discord.Embed(title = "**Coinflip Results**", description = f"**{ctx.author.name} tossed {number} coins**\nAnd got **{num1}** heads and **{num2}** tails!", colour = discord.Colour.gold())    
    else:
        embed = discord.Embed(title = "**Coinflip Results**", description = f"**{ctx.author.name} tossed a coin**\nAnd got **{random.choice(choices)}**!", colour = discord.Colour.gold())    
    await ctx.send(embed = embed) 

@client.command(name = "rps", description = "Play rock paper scissors with birth control", aliases = ["rockpaperscissors"])        
async def rps(ctx,*,playerChoice):
    playerChoice.lower()
        
    wins = {"rock":"scissors", "paper":"rock", "scissors":"paper"}
    defeats = wins[playerChoice]

    cpuChoice = random.choice(["rock", "paper", "scissors"])
    
    if playerChoice == cpuChoice:
        embed = discord.Embed(title = "**Rock Paper Scissors**", description = f"Both players selected **{playerChoice}**.\nIt's a tie!", colour = discord.Colour.orange())       
    elif cpuChoice in defeats:
        embed = discord.Embed(title = "**Rock Paper Scissors**", description = f"**{playerChoice}** beats **{cpuChoice}**!\n{ctx.author.name} wins!", colour = discord.Colour.green())     
    else:
        embed = discord.Embed(title = "**Rock Paper Scissors**", description = f"**{cpuChoice}** beats **{playerChoice}**!\n{ctx.author.name} loses.", colour = discord.Colour.red())    
 
    await ctx.send(embed = embed)

@client.command(name = "cps", description = "Play cock pussy sperm with birth control", aliases = ["cockpussysperm"])        
async def cps(ctx,*,playerChoice):
    playerChoice.lower()
        
    wins = {"cock":"pussy", "pussy":"sperm", "sperm":"cock"}
    defeats = wins[playerChoice]

    cpuChoice = random.choice(["cock", "pussy", "sperm"])
    
    if playerChoice == cpuChoice:
        embed = discord.Embed(title = "**Cock Pussy Sperm**", description = f"Both players selected **{playerChoice}**.\nIt's a tie!", colour = discord.Colour.orange())       
    elif cpuChoice in defeats:
        embed = discord.Embed(title = "**Cock Pussy Sperm**", description = f"**{playerChoice}** beats **{cpuChoice}**!\n{ctx.author.name} wins!", colour = discord.Colour.green())     
    else:
        embed = discord.Embed(title = "**Cock Pussy Sperm**", description = f"**{cpuChoice}** beats **{playerChoice}**!\n{ctx.author.name} loses.", colour = discord.Colour.red())    
 
    await ctx.send(embed = embed)

@client.command(name = "dice", description = "Rolls some dice.", aliases = ["diceroll","rolldice","roll"])        
async def dice(ctx,*,rolls = 1):
    result = []
    total = 0

    if rolls > 10:
        rolls = 10
    
    for i in range(0, rolls):
        randroll = random.randint(1, 6)
        result.append(randroll)
        total += randroll

    if total == (6 - 0) * rolls:
        colour = discord.Colour.green()    
    elif total >= (6 - 1) * rolls:
        colour = discord.Colour.dark_green()
    elif total >= (6 - 2) * rolls:
        colour = discord.Colour.gold()
    elif total >= (6 - 3) * rolls:
        colour = discord.Colour.orange()         
    elif total >= (6 - 4) * rolls:
        colour = discord.Colour.dark_orange()
    elif total >= (6 - 5) * rolls:
        colour = discord.Colour.red()
        
    embed = discord.Embed(title = ":game_die:Rolling dice!", description = f"{result}\nIn the end, the result was: {total}", colour = colour)
        
    await ctx.send(embed = embed)

@client.command(name = "giveaway", description = "awaygive", aliases = [])
@commands.has_permissions(administrator = True)
async def giveaway(ctx):
    await ctx.send("Let's start with this giveaway! Answer these questions: ")

    questions = [["Which channel should it be hosted in?", "Mention the channel"],
                 ["How long should the giveaway last?", "s|m|h|d"],
                 ["What is the prize of the giveaway?", "e.g. Free V-bucks"]]

    answers = {}

    for i, question in enumerate(questions):
        answer = await GetMessage(ctx, question[0], question[1], timeout = 30)

        if not answer:
            await ctx.send("You failed to answer in time, please answer quicker next time!")
            return
        
        answers[i] = answer

    try:
        channelID = int(answers[0][2:-1])
    except:
        await ctx.send(f"You failed to mention a channel properly, Do it like this {ctx.channel.mention} next time!")
        return

    channel = client.get_channel(channelID)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You failed to answer the time with a proper unit. Use (s|m|h|d) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be and integer. Please enter an integer next time!")
        return

    embed = discord.Embed(name = "Giveaway content")
    for key, value in answers.items():
        embed.add_field(name = f"Question: {questions[key][0]}", value = f"Answer: {value}", inline = False)

    m = await ctx.send("Are these all valid?", embed = embed)
    await m.add_reaction("✅")
    await m.add_reaction("❎")

    try:
        reaction, member = await client.wait_for(
            "reaction_add", timeout = 30,
            check=lambda reaction, user : user == ctx.author
            and reaction.message.channel == ctx.channel
            )
        
    except asyncio.TimeoutError:
        await ctx.send("Confirmation failure. Please try again.")
        return

    if str(reaction.emoji) not in ["✅","❎"] or str(reaction.emoji) == "❎":
        await ctx.send("Cancelling giveaway!")
        return
    
    prize = answers[2]

    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]} seconds!")
        
    gembed = discord.Embed(title = "Giveaway", description = f"Prize: **{prize}**", colour = white)
    gembed.add_field(name = "Hosted by:", value = ctx.author.mention)
    gembed.set_footer(text = f"Ends in {answers[1]} from this message!")

    msg = await channel.send(embed = gembed)
    await channel.send("@here")

    await msg.add_reaction("🎉")

    await asyncio.sleep(time)

    newMsg = await channel.fetch_message(msg.id)

    users = await newMsg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations {winner.mention}! You won **{prize}**.\n\nTo claim your prize, DM {ctx.guild.owner.mention} within 24 hours of this messsage.")
'''
@client.command(name = "reroll", description = ".", aliases = [])
@commands.has_permissions(administrator = True)
async def reroll(ctx, channel : discord.TextChannel, id_ : int):
    try:
        newMsg = await channel.fetch_message(id_)
    except:
        await ctx.send("The id was entered incorrectly.")
        return
    
    users = await newMsg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)

    await channel.send(f"Congratulations {winner.mention}! You won **{prize}**.\n\nTo claim your prize, DM {ctx.guild.owner} within 24 hours of this messsage.")
'''
def convert(time):
    pos = ["s","m","h","d"]

    timeDict = {"s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return - 2

    return val * timeDict[unit]

async def GetMessage(ctx, contentOne="Default Message", contentTwo="\uFEFF", timeout=30):
    """
    This function sends an embed containing the params and then waits for a message to return
    Params:
     - bot (commands.Bot object) :
     - ctx (context object) : Used for sending msgs n stuff
     - Optional Params:
        - contentOne (string) : Embed title
        - contentTwo (string) : Embed description
        - timeout (int) : Timeout for wait_for
    Returns:
     - msg.content (string) : If a message is detected, the content will be returned
    or
     - False (bool) : If a timeout occurs
    """
    embed = discord.Embed(title=f"{contentOne}", description=f"{contentTwo}")
    sent = await ctx.send(embed=embed)
    try:
        msg = await client.wait_for("message", timeout=timeout,
            check=lambda message: message.author == ctx.author
            and message.channel == ctx.channel,
        )
        if msg:
            return msg.content
    except asyncio.TimeoutError:
        return False

@client.command(name = "choose", description = "Makes a choice for you.", aliases = ["choice"])
async def choose(ctx,choice1,*,choice2):
    embed = discord.Embed(title = "", description = f":thinking: {ctx.author.name}, I pick {random.choice([choice1, choice2])}", colour = white)  
    await ctx.send(embed = embed)

@client.command(name = "rate", description = "Rates a person randomly.", aliases = ["ratewaifu", "ratehusbando"])
async def rate(ctx,person):
    num = random.randint(0,10)
               
    if person == "birthcontrol" or person == "BirthControl" or person == "myself" or person == "Myself":
        embed = discord.Embed(title = "", description = f":thumbsup: I'd give **myself** a **10/10**.", colour = white)
    elif person == "johncena" or person == "JohnCena":
        embed = discord.Embed(title = "", description = f":thumbsup: I'd give **John Cena** a **11/10**.", colour = white)
    elif person == "yourmom" or person == "YourMom":
        embed = discord.Embed(title = "", description = f":thumbsup: I'd give **Your Mom** a **10/10**.", colour = white)
    else:
        if num >= 8:        
            embed = discord.Embed(title = "", description = f":thumbsup: I'd give **{person}** a **{num}/10**.", colour = white)      
        else:
            embed = discord.Embed(title = "", description = f":thinking: I'd give **{person}** a **{num}/10**.", colour = white)
            
    await ctx.send(embed = embed)

@client.command(name = "fortune", description = "Gets a random fortune.", aliases = [])
async def fortune(ctx):
    pass

@client.command(name = "throw", description = "Throw things at your friends!.", aliases = [])
async def throw(ctx):
    pass

@client.command(name = "translate", description = "Translate stuffs.", aliases = [])
async def translate(ctx, lang_to, *args):
    """Translates the given text to the language `lang_to`.
    The language translated from is automatically detected."""
    lang_to = lang_to.lower()
    text = ' '.join(args)
    translator = googletrans.Translator()
    text_translated = translator.translate(text, dest=lang_to).text
    await ctx.send(text_translated)

client.run("")
