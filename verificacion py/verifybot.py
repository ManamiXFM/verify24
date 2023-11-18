import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.reactions = True
intents.messages = True  # Agrega el intento de mensajes

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')

@bot.command(name='verificar', pass_context=True)
async def verificar(ctx):
    # Obtén el objeto Member del autor del mensaje
    member = ctx.guild.get_member(ctx.author.id)
    
    if member and member.guild_permissions.administrator:
        mensaje_verificacion = await ctx.send('Reaccionen a este mensaje con 🍓 para verificarse.')
        await mensaje_verificacion.add_reaction('🍓')
        await mensaje_verificacion.add_reaction('🍎')  # Puedes agregar más emojis si lo deseas
        await ctx.send('Canal de verificación configurado. Los usuarios pueden reaccionar al mensaje para verificarse.')

@bot.event
async def on_raw_reaction_add(payload):
    print('Evento de reacción detectado')  # Mensaje de depuración
    print(payload)  # Muestra la información completa del payload

    fresa_emoji_name = "🍓"
    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    if payload.emoji.name == fresa_emoji_name and payload.user_id != bot.user.id:
        guild = bot.get_guild(payload.guild_id)
        
        # Utiliza fetch_member en lugar de get_member
        member = await guild.fetch_member(payload.user_id)
        
        role_id = 1173555812719931392  # Reemplaza con la ID del rol
        role = discord.utils.get(guild.roles, id=role_id)

        if role:
            await member.add_roles(role)
            await member.send('¡Bienvenido! Ahora estás verificado.')
            print(f'Usuario {member.display_name} verificado con el rol {role.name}')

# Inicia el bot con tu token
bot.run('MTE3NTM3MzcyODM2NDg5NjMxNg.GxjoUw.fK3faGQlFJtmySGjieHSuMTi0xAtWu_FysZcyM')
