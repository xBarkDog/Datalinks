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
articles = ["servo","mechlimb","stone","ice","lamp","copper","iron","drivebox","jade","transformer","arcolantium","brick","silicon","gold","instrument","levitator","hydrogenerator","carbonfiber","uranium","antenna","plastic","flint","gear","diamond","eridanium","seat","aluminium","sail","rubber","cleats","spotlight","turbofan","cooler","anchor","delaywire","titanium","crudewing","amethyst","glass","wing","herbicide","leaves","organicmatter","neodymium","thruster","gravdevice","steeringseat","lightningrod","psibutton","gyro","dynamite","refinery","dimensionaldoor","forcefield","missile","television","magnesium","sand","asphalt","gunpowder","ashes","touchtrigger","zapwire","ruby","explosives","remoteseat","quartz","solarpanel","speaker","powercell","container","inverter","heater","wire","sign","switch","light","generator","signalwire","tintedglass","polysilicon","balloon","truss","firework","faucet","exoticmatter","photonshard","glowtube","cannon","treads","motor","propeller","converter","pipe","lift","enricheduranium","signalswitch","empbomb","coat","polyestercoat","engine","inertiatrigger","gammadrive","warhead","reactor","spawnpoint","rocket","camera","spacesuit","protalium","protoncell","airshield","factory","ore","modem","basecenter","seeker","hyperdrive","prospector","steamengine","lirvanite","energybomb","timemachine","pod","biowall","clock","ballasttank","keyboard","cloakingdevice","alkalinecell","commlink","bogie","radiationsuit","sulfur","activedefense","aethergate","combolock","lab","powerplant","teleporter","goo","hull","ionrocket","iondrive","lasertargeter","actuator","node","valve","memorychip","monitor","scanner","mainspring","heatcylinder","searchlight","computer","energyshield","accelerator","energycannon","abantium","armor","rotor","beamcannon","lexan","zaktralia","firewood","probabilityfield","foam","flamethrower","launcher","sensor","graphicscard","cloth","ceramic","ramjet","dish","button","singularitybomb","radar","gel","plant","inductor","firebox","geigercounter","gun","book","track","bend","market","warpgate","automaton","parachutepack","seed","bank","filler","charcoal","wood","interceptor","windmill","bilgepump","crudehull","seaalloy","catapult","biolab","cotton","selfdestruct","derrick","controller","plutonium","deuteriumcap","lcd","radio","horse","crate","flubber","belt","foundation","concrete","scubasuit","pulsedrive","brake","speedwalk","trampoline","paybox","y","turboshaft","sword","musket","scattergun","pistol","torch","fuelcan","hammer","wrench","viper","lasersword","stinger","pitchfork","blinkdisplacer","plasmapistol","saving","templates","bot","storms","seed","biolab","programming","energycannon","substances", "cmos", "relics", "endgame", "handcannon", "machinegun", "ammo", "coal", "water", "oil", "acid", "nitroglycerin", "nitrogen", "liquidnitrogen", "protaloxide", "protaliumoxide", "toxin", "gas", "steam"]
#aliases
templates = ["wedgetemplate", "balltemplate", "wheeltemplate", "bladetemplate", "doortemplate", "cornertemplate", "wedge", "ball", "wheel", "blade", "door", "corner"]

sportball = ["sportsball", "volleyball", "basketball", "baseball", "dodgeball", "bowlingball", "sandbag"]

botspawn = ["jolemspawner", "jolemspawn", "botspawner", "automatonspawn", "automatonspawner"]
#articles with multiple pages due to length
listedArticles = { "programming":5, "biolab":2 }

listMessages = {}

@client.event
async def on_ready():
  print("Initialized")

#standard datalink info command
@client.command()
async def dl(ctx, arg):
  article = ''.join(arg)

  if article.lower() in templates:
    article = "templates"
  if article.lower() in sportball:
    article = "sportball"
  if article.lower() == "protal":
    article = "protalium"
  if article.lower() in botspawn:
    article = "botspawn"
  
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
statuslist = ["VOTE WAR", "if you vote cold war in the next minute, devan will tell us his deepest secret and fears", "this is how we played tetris back in the days before new fangled electricity", "/s cj", "Walking Simulator", "bill nye the scibust guy", "the prefix is ^", "forget it, enjoy being cavemen loser nubs"]
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

@tasks.loop(seconds=2100)
async def task_loop():
    ... #ever 2100 seconds the random status thing is executed (or every 35 minutes)
    CC = random.choice(statuslist)
    await client.change_presence(activity=discord.Game(CC))
    print(CC)
    print("random status task successfully executed")



#update prices if recipies has been updated
@client.command()
@commands.is_owner()
async def updateprice(ctx):
  importlib.reload(recipies)
  print("updating of prices successfully executed")


#update settings
@client.command()
@commands.is_owner()
async def updatesettings(ctx):
  importlib.reload(settings)
  print("settings update successfully executed")


@client.command()
@commands.is_owner()
async def speak(ctx, say):
  sayarg = ' '.join(say)
  await ctx.send(sayarg)
  print(say)
  print("Speak command successfully executed")



client.run(settings.TOKEN)
