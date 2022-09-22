#imports
import discord
import os
import recipies
import json
import asyncio
import sys
import time
import settings
import random
import importlib



from discord.ext import commands, tasks

#intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True


client = commands.Bot(command_prefix=settings.PREFIX, intents=intents)

#list of datalink articles
articles = ["servo","mechlimb","stone","ice","lamp","copper","iron","drivebox","jade","transformer","arcolantium","brick","silicon","gold","instrument","levitator","hydrogenerator","carbonfiber","uranium","antenna","plastic","flint","gear","diamond","eridanium","seat","aluminium","sail","rubber","cleats","spotlight","turbofan","cooler","anchor","delaywire","titanium","crudewing","amethyst","glass","wing","herbicide","leaves","organicmatter","neodymium","thruster","gravdevice","steeringseat","lightningrod","psibutton","gyro","dynamite","refinery","dimensionaldoor","forcefield","missile","television","magnesium","sand","asphalt","gunpowder","ashes","touchtrigger","zapwire","ruby","explosives","remoteseat","quartz","solarpanel","speaker","powercell","container","inverter","heater","wire","sign","switch","light","generator","signalwire","tintedglass","polysilicon","balloon","truss","firework","faucet","exoticmatter","photonshard","glowtube","cannon","treads","motor","propeller","converter","pipe","lift","enricheduranium","signalswitch","empbomb","coat","polyestercoat","engine","inertiatrigger","gammadrive","warhead","reactor","spawnpoint","rocket","camera","spacesuit","protalium","protoncell","airshield","factory","ore","modem","basecenter","seeker","hyperdrive","prospector","steamengine","lirvanite","energybomb","timemachine","pod","biowall","clock","ballasttank","keyboard","cloakingdevice","alkalinecell","commlink","bogie","radiationsuit","sulfur","activedefense","aethergate","combolock","lab","powerplant","teleporter","goo","hull","ionrocket","iondrive","lasertargeter","actuator","node","valve","memorychip","monitor","scanner","mainspring","heatcylinder","searchlight","computer","energyshield","accelerator","energycannon","abantium","armor","rotor","beamcannon","lexan","zaktralia","firewood","probabilityfield","foam","flamethrower","launcher","sensor","graphicscard","cloth","ceramic","ramjet","dish","button","singularitybomb","radar","gel","plant","inductor","firebox","geigercounter","gun","book","track","bend","market","warpgate","automaton","parachutepack","seed","bank","filler","charcoal","wood","interceptor","windmill","bilgepump","crudehull","seaalloy","catapult","biolab","cotton","selfdestruct","derrick","controller","plutonium","deuteriumcap","lcd","radio","horse","crate","flubber","belt","foundation","concrete","scubasuit","pulsedrive","brake","speedwalk","trampoline","paybox","y","turboshaft","sword","musket","scattergun","pistol","torch","fuelcan","hammer","wrench","viper","lasersword","stinger","pitchfork","blinkdisplacer","plasmapistol","saving","templates","bot","automaton","storms","seed","biolab","programming","energycannon","substances", "cmos", "relics"]
#aliases for substance page
substance = ["ammo", "coal", "water", "oil", "acid" "nitroglycerin", "nitrogen", "liquidnitrogen", "protaloxide", "protaliumoxide", "toxin", "gas", "steam"]
#aliases for template page
templates = ["WedgeTemplate", "BallTemplate", "WheelTemplate", "BladeTemplate", "DoorTemplate", "CornerTemplate", "Wedge Template", "Ball Template", "Wheel Template", "Blade Template", "Door Template", "CornerTemplate"]
#articles with multiple pages due to length
listedArticles = { "programming":5, "biolab":2 }

listMessages = {}

@client.event
async def on_ready():
  print("Initialized")

#standard datalink info command
@client.command()
async def dl(ctx, arg):
  article = arg
  if article.lower() in substance:
    article = "substances"
  if article.lower() in templates:
    article = "templates"
  if article.lower() in articles:
    articleEmbed = discord.Embed(title = article.capitalize()) 
    articleEmbed.set_image(url="https://pipe.miroware.io/5e97bfd35d5b6e0703983341/HelpMenuImages/" + article.lower() + ".png")
    print('dl command successfully executed')
#list amount of credits if in recipies.py
    if article.lower() in recipies.list:
      articleEmbed.description = str(recipies.list[article.lower()]) + " Credits"
    msg = await ctx.send(embed=articleEmbed)
#reactions for long articles with multiple pages
    if (article.lower()[:-1] in listedArticles) or (article.lower() in listedArticles):
      await msg.add_reaction("⬅️")
      await msg.add_reaction("➡️")
      if article[-1:].isnumeric():
        listMessages[msg] = [int(article[-1:]), article.lower()[:-1]]
      else:
        listMessages[msg] = [1, article.lower()]
  else:
    await ctx.send("Article not found. If you're having trouble finding something, remember that classes of parts only have one article (for example, all templates are in the Templates article, and all liquids/gases are in the Substances article.) Contact murpyh#3984 if you think something may be missing from the database.")


    

#@client.event
#async def on_command_error(ctx, error):
#  await ctx.send("An error occured while running the command. Did #you forget a required argument?")

#lists all parts
@client.command()
async def list(ctx):
  result = ""
  for entry in articles:
    result = result + entry.capitalize() + ", " 
  listEmbed = discord.Embed(title="Part List", description=result[:-2])
  await ctx.send(embed=listEmbed)
  print('list command successfully executed')
  

@client.event
async def on_reaction_add(reaction, user):
  msg = reaction.message
  
  if msg in listMessages:
    if msg.author != user:
      cap = listedArticles[listMessages[msg][1]]
      if reaction.emoji == "⬅️":
        listMessages[msg][0] = listMessages[msg][0]  - 1
        if listMessages[msg][0] < 1:
          listMessages[msg][0] = 1
      elif reaction.emoji == "➡️":
        listMessages[msg][0]  = listMessages[msg][0]  + 1
        if listMessages[msg][0] > cap:
           listMessages[msg][0] = cap
      embed = discord.Embed()
      if listMessages[msg][0] == 1:
        image = "https://pipe.miroware.io/5e97bfd35d5b6e0703983341/HelpMenuImages/" + listMessages[msg][1] + ".png"
      else:
        image = "https://pipe.miroware.io/5e97bfd35d5b6e0703983341/HelpMenuImages/" + listMessages[msg][1] + str(listMessages[msg][0]) + ".png"
      articleEmbed = discord.Embed(title=listMessages[msg][1].capitalize())
      if listMessages[msg][1].lower() in recipies.list:
        articleEmbed.description = str(recipies.list[listMessages[msg][1].lower()]) + " Credits"
      articleEmbed.set_image(url=image)
      await msg.edit(embed=articleEmbed)
      await reaction.remove(user)
  
#relic name lists
ReplicationDevice = ["deviceofreplication", "replicationdevice"] 
TeleportAxis = ["axisofrelativity", "axisrelativity", "relativityaxis"]
TelepathyBeacon = ["telepathybeacon", "beaconoftelepathy", "globalmessagebeacon", "/mbeacon"]
VengeanceBlade = ["bladeofvengeance", "vengeanceblade"]
WealthCauldron = ["wealthcauldron", "cauldronofwealth"]
InfChalice = ["infinitychalice", "gobletofplenty", "plentychalice", "gobletofinfinity"]
SerenityShield = ["serenityorb", "orbofserenity", "serenityshield", "orbshield"]
#actual relic command
@client.command() 
async def relic(ctx, *args): 
  relic = ''.join(args)
  print (relic)
  if relic.lower() in ReplicationDevice: 
    relicEmbed=discord.Embed(title="Device of Replication", description="Duplicates 50 lower value parts when signaled", color=0x0000c8)
    relicEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/1020146938638778429/1020780156895379497/DeviceOfReplication.PNG")
    relicEmbed.add_field(name="PG", value="Power Generation: 18/tick", inline=True) 
    relicEmbed.add_field(name="MV", value="Max Value: Unknown", inline=True)
    await ctx.send(embed=relicEmbed)
    print('relic command for Device of Replication successfully executed')
  if relic.lower() in TeleportAxis: 
    relicEmbed=discord.Embed(title="Axis of Relativity", description="teleports to specified XYZ coordinates when signaled, does not take power, shorter wind up then hyperdrive", color=0x0000c8)
    relicEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/1020146938638778429/1020780156895379497/DeviceOfReplication.PNG")
    await ctx.send(embed=relicEmbed)
    print('relic command for Axis of Relativity successfully executed')
  if relic.lower() in TelepathyBeacon:
    relicEmbed=discord.Embed(title="Beacon of Telepathy", description="/m except for regular mortals such as us (can be used by multiple people, perhaps if unlocked?) so displays global message when message sent near it.", color=0x0000c8)
    #relicEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/1020146938638778429/1020780156895379497/DeviceOfReplication.PNG")
    await ctx.send(embed=relicEmbed)  
    print('relic command for Beacon of Telepathy successfully executed')
  if relic.lower() in VengeanceBlade:
    relicEmbed=discord.Embed(title="Blade of Vengeance", description="keks anything it touches except if locked by rogue", color=0x0000c8)
    #relicEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/1020146938638778429/1020780156895379497/DeviceOfReplication.PNG")
    await ctx.send(embed=relicEmbed)  
    print('relic command for Blade of Vengeance successfully executed')
  if relic.lower() in WealthCauldron:
    relicEmbed=discord.Embed(title="Cauldron of Wealth", description="gives credits", color=0x0000c8)
    relicEmbed.add_field(name="CR/s", value="Credit Generation: 2/second", inline=True) 
    #relicEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/1020146938638778429/1020780156895379497/DeviceOfReplication.PNG")
    await ctx.send(embed=relicEmbed)  
    print('relic command for Cauldron of Wealth successfully executed')
  if relic.lower() in InfChalice:
    relicEmbed=discord.Embed(title="Goblet of Plenty", description="containers and powercells never run out when attached unless your using it unrealistically fast", color=0x0000c8)
    #relicEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/1020146938638778429/1020780156895379497/DeviceOfReplication.PNG")
    await ctx.send(embed=relicEmbed)  
    print('relic command for Goblet of Plenty successfully executed')
  if relic.lower() in SerenityShield:
    relicEmbed=discord.Embed(title="Orb of Serenity", description="spawns an immovable shield (possibly terrain) that is made out of arcolantium textured parts and transparent part", color=0x0000c8)
    #relicEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/1020146938638778429/1020780156895379497/DeviceOfReplication.PNG")
    await ctx.send(embed=relicEmbed)  
    print('relic command for Ore of Serenity successfully executed')



#server list command
@client.command()
@commands.is_owner()
async def servers(ctx):
    activeservers = client.guilds    
    for guild in activeservers:
      await ctx.send(guild.name)
      print('server list command successfully executed for')
      print(guild.name)


#useless status thing
statuslist = ["VOTE WAR", "if you vote cold war in the next minute, devan will tell us his deepest secret and fears", "this is how we played tetris back in the days before new fangled electricity", "/s cj", "Walking Simulator", "bill nye the scibust guy", "the prefix is ^"]
#status set command
@client.command()
@commands.is_owner()
async def status(ctx, *args):
  statarg = ' '.join(args)
  await client.change_presence(activity=discord.Game(statarg))
  await ctx.send(statarg)
  print(statarg)
  print('status command successfully executed')

#list of statuses i might use
@client.command()
@commands.is_owner()
async def statlist(ctx):
  result = ""
  for entry in statuslist:
    result = result + entry.capitalize() + " | " 
  statEmbed = discord.Embed(title="Status List", description=result[:-2])
  await ctx.send(embed=statEmbed)
  print('list of statuses command successfully executed')

#status list for mobile (for easier copying)
@client.command()
@commands.is_owner()
async def statmobile(ctx):
  result = ""
  for mobentry in statuslist:
    await ctx.send(mobentry)



@client.listen()
async def on_ready():
    task_loop.start() # important to start the loop

@tasks.loop(seconds=180)
async def task_loop():
    ... #ever 180 seconds the random status thing is executed (or every 3 minutes)
    CC = random.choice(statuslist)
    await client.change_presence(activity=discord.Game(CC))
    print(CC)
    print("random status task successfully executed")



#update prices if recipies has been updated
@client.command()
@commands.is_owner()
async def updateprice(ctx):
  importlib.reload(recipies)


#update settings
@client.command()
@commands.is_owner()
async def updatesettings(ctx):
  importlib.reload(settings)



@client.command()
@commands.is_owner()
async def speak(ctx, arg):
  sayarg = ' '.join(args)
  await ctx.send(sayarg)




client.run(settings.TOKEN)
