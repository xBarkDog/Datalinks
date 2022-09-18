import discord
import os
import recipies



from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True


client = commands.Bot(command_prefix='^', intents=intents)


articles = ["servo","mechlimb","stone","ice","lamp","copper","iron","drivebox","jade","transformer","arcolantium","brick","silicon","gold","instrument","levitator","hydrogenerator","carbonfiber","uranium","antenna","plastic","flint","gear","diamond","eridanium","seat","aluminium","sail","rubber","cleats","spotlight","turbofan","cooler","anchor","delaywire","titanium","crudewing","amethyst","glass","wing","herbicide","leaves","organicmatter","neodymium","thruster","gravdevice","steeringseat","lightningrod","psibutton","gyro","dynamite","refinery","dimensionaldoor","forcefield","missile","television","magnesium","sand","asphalt","gunpowder","ashes","touchtrigger","zapwire","ruby","explosives","remoteseat","quartz","solarpanel","speaker","powercell","container","inverter","heater","wire","sign","switch","light","generator","signalwire","tintedglass","polysilicon","balloon","truss","firework","faucet","exoticmatter","photonshard","glowtube","cannon","treads","motor","propeller","converter","pipe","lift","enricheduranium","signalswitch","empbomb","coat","polyestercoat","engine","inertiatrigger","gammadrive","warhead","reactor","spawnpoint","rocket","camera","spacesuit","protalium","protoncell","airshield","factory","ore","modem","basecenter","seeker","hyperdrive","prospector","steamengine","lirvanite","energybomb","timemachine","pod","biowall","clock","ballasttank","keyboard","cloakingdevice","alkalinecell","commlink","bogie","radiationsuit","sulfur","activedefense","aethergate","combolock","lab","powerplant","teleporter","goo","hull","ionrocket","iondrive","lasertargeter","actuator","node","valve","memorychip","monitor","scanner","mainspring","heatcylinder","searchlight","computer","energyshield","accelerator","energycannon","abantium","armor","rotor","beamcannon","lexan","zaktralia","firewood","probabilityfield","foam","flamethrower","launcher","sensor","graphicscard","cloth","ceramic","ramjet","dish","button","singularitybomb","radar","gel","plant","inductor","firebox","geigercounter","gun","book","track","bend","market","warpgate","automaton","parachutepack","seed","bank","filler","charcoal","wood","interceptor","windmill","bilgepump","crudehull","seaalloy","catapult","biolab","cotton","selfdestruct","derrick","controller","plutonium","deuteriumcap","lcd","radio","horse","crate","flubber","belt","foundation","concrete","scubasuit","pulsedrive","brake","speedwalk","trampoline","paybox","y","turboshaft","sword","musket","scattergun","pistol","torch","fuelcan","hammer","wrench","viper","lasersword","stinger","pitchfork","blinkdisplacer","plasmapistol","saving","templates","bot","automaton","storms","seed","biolab","programming","energycannon","substances", "cmos", "relics"]
substance = ["ammo", "coal", "water", "oil", "acid" "nitroglycerin", "nitrogen", "liquidnitrogen", "protaloxide", "protaliumoxide", "toxin", "gas", "steam"]
listedArticles = { "programming":5, "biolab":2 }

listMessages = {}

@client.event
async def on_ready():
  print("Initialized")


@client.command()
async def dl(ctx, arg):
  article = arg
  if article.lower() in substance:
    article = "substances"
  if article.lower() in articles:
    articleEmbed = discord.Embed(title = article.capitalize()) 
    articleEmbed.set_image(url="https://pipe.miroware.io/5e97bfd35d5b6e0703983341/HelpMenuImages/" + article.lower() + ".png")
    if article.lower() in recipies.list:
      articleEmbed.description = str(recipies.list[article.lower()]) + " Credits"
    msg = await ctx.send(embed=articleEmbed)
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

@client.command()
async def list(ctx):
  result = ""
  for entry in articles:
    result = result + entry.capitalize() + ", " 
  listEmbed = discord.Embed(title="Part List", description=result[:-2])
  await ctx.send(embed=listEmbed)
  

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
  
ReplicationDevice = ["DeviceofReplication", "ReplicationDevice", "Device of Replication", "Replication Device"] 
@client.command() 
async def relic(ctx, arg): 
  relic = arg 
  if relic in ReplicationDevice: 
    relicEmbed=discord.Embed(title="Device of Replication", description="Duplicates 50 lower value parts when signaled", color=0x0000c8)
    relicEmbed.set_thumbnail(url="https://media.discordapp.net/attachments/1020146938638778429/1020780156895379497/DeviceOfReplication.PNG")
    relicEmbed.add_field(name="PG", value="Power Generation: 18/tick", inline=True) 
    relicEmbed.add_field(name="MV", value="Max Value: Unknown", inline=True)
    await ctx.send(embed=relicEmbed)





client.run("MTAxODk1MTEyOTYzNzMzNTA1MA.GpHP2L.IaiA_NHvaSTTn__jNIx3Q6RUnuw8WD69D3J48Q")