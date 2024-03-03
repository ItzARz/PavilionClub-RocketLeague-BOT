from discord.ext.commands.core import bot_has_permissions
import requests
from PIL import Image, ImageFont, ImageDraw
import discord
from discord.ext import commands

rangos = [
    "Unranked",
    "Bronze I",
    "Bronze II",
    "Bronze III",
    "Silver I",
    "Silver II",
    "Silver III",
    "Gold I",
    "Gold II",
    "Gold III",
    "Platinum I",
    "Platinum II",
    "Platinum III",
    "Diamond I",
    "Diamond II",
    "Diamond III",
    "Champion I",
    "Champion II",
    "Champion III",
    "Grand Champion I",
    "Grand Champion II",
    "Grand Champion III",
    "Supersonic Legend",
]

imagen_rango = [
    "unranked.png",
    "br1.png",
    "br2.png",
    "br3.png",
    "silver1.png",
    "silver2.png",
    "silver3.png",
    "g1.png",
    "g2.png",
    "g3.png",
    "p1.png",
    "p2.png",
    "p3.png",
    "d1.png",
    "d2.png",
    "d3.png",
    "c1.png",
    "c2.png",
    "c3.png",
    "gc1.png",
    "gc2.png",
    "gc3.png",
    "ssl.png",
]

output_path = "output/rank_image.jpg"
base_image_path = "assets/base/BASE.jpg"

#TYPOs
font_path = "assets/font/Amuro-CB.ttf"
font_nickname = ImageFont.truetype(font_path, 35)
font_rango = ImageFont.truetype(font_path, 23)
font_division = ImageFont.truetype(font_path, 20)
font_mmr = ImageFont.truetype(font_path, 68)

# EMOJIS
hot_emoji = Image.open("assets/EMOJIS/hot.jpg")
paz_emoji = Image.open("assets/EMOJIS/paz.jpg")
skull_emoji = Image.open("assets/EMOJIS/calavera.jpg")

# EMOJIS
hot_emoji = Image.open("assets/EMOJIS/hot.jpg")
paz_emoji = Image.open("assets/EMOJIS/paz.jpg")
skull_emoji = Image.open("assets/EMOJIS/calavera.jpg")

def api_fetch(nickname):
  url = "https://rocket-league1.p.rapidapi.com/ranks/{}".format(nickname)

  headers = {
      "User-Agent": "RapidAPI Playground",
      "Accept-Encoding": "identity",
      "X-RapidAPI-Key": "{API_KEY}", #YOUR RAPIDAPI KEY HERE
      "X-RapidAPI-Host": "rocket-league1.p.rapidapi.com",
  }
  response = requests.get(url, headers=headers)
  data = response.json()
  return data


def detectarDivision(numero):
    divisiones = {
        1: "DIVISION I",
        2: "DIVISION II",
        3: "DIVISION III",
        4: "DIVISION IV"
    }
    return divisiones.get(numero, "N/A")

def create_image(data, nickname):
    img = Image.open(base_image_path)
    draw = ImageDraw.Draw(img)

    def draw_streak(position, streak):
      if streak > 0:
        draw.text(position, f"+{streak}", fill=(22, 139, 33), font=font_rango)
      else:
        draw.text(position, f"{streak}", fill=(204, 0, 0), font=font_rango)

    # LOGICA PARA TOMAR LA IMAGEN CORRECTA DE ACUERDO AL RANGO
    rango = data["ranks"][0]["rank"]
    if rango in rangos:
        indice = rangos.index(rango)
        ruta_imagen = "assets/ranks/{}".format(imagen_rango[indice])
        rango_imagen_single = Image.open(ruta_imagen)

    rango2 = data["ranks"][1]["rank"]
    if rango2 in rangos:
        indice = rangos.index(rango2)
        ruta_imagen = "assets/ranks/{}".format(imagen_rango[indice])
        rango_imagen_doubles = Image.open(ruta_imagen)

    rango3 = data["ranks"][2]["rank"]
    if rango3 in rangos:
        indice = rangos.index(rango3)
        ruta_imagen = "assets/ranks/{}".format(imagen_rango[indice])
        rango_imagen_standard = Image.open(ruta_imagen)

    # TEXTO RANGO, DIVISIONES Y MMR
    rango_standard = data["ranks"][2]["rank"].upper()
    division_standard = detectarDivision(data["ranks"][2]["division"])
    mmr_standard = str(data["ranks"][2]["mmr"])

    rango_doubles = data["ranks"][1]["rank"].upper()
    division_doubles = detectarDivision(data["ranks"][1]["division"])
    mmr_doubles = str(data["ranks"][1]["mmr"])

    rango_single = data["ranks"][0]["rank"].upper()
    division_single = detectarDivision(data["ranks"][3]["division"])
    mmr_single = str(data["ranks"][0]["mmr"])

    # DIBUJAMOS EL NICK DEL PLAYER
    draw.text((19.52, 20.37), nickname.upper(), fill=(12, 12, 12), font=font_nickname)

    # ESTOS SON DE STANDARD
    draw.text((20.77, 140), rango_standard, fill=(252, 252, 252), font=font_rango)
    draw.text((20.77, 165), division_standard, fill=(252, 252, 252, 25), font=font_division)
    draw.text((20.77, 175), mmr_standard, fill=(159, 221, 0), font=font_mmr)

    # ESTOS SON LOS TEXTOS DE 2PA2
    draw.text((270, 345), rango_doubles, fill=(252, 252, 252), font=font_rango)
    draw.text((295, 370), division_doubles, fill=(252, 252, 252, 25), font=font_division)
    draw.text((270, 380), mmr_doubles, fill=(159, 221, 0), font=font_mmr)

    # ESTOS SON LOS TEXTOS DE GUABIGUAN
    draw.text((20.77, 550), rango_single, fill=(252, 252, 252), font=font_rango)
    draw.text((20.77, 575), division_single, fill=(252, 252, 252, 25), font=font_division)
    draw.text((20.77, 585), mmr_single, fill=(159, 221, 0), font=font_mmr)

    img.paste(rango_imagen_standard.resize((126, 126)), (247, 136))
    img.paste(rango_imagen_doubles.resize((126, 126)), (40, 335))
    img.paste(rango_imagen_single.resize((126, 126)), (247, 540))

    streak_standard = data["ranks"][2]["streak"]
    streak_doubles = data["ranks"][1]["streak"]
    streak_single = data["ranks"][0]["streak"]

    draw_streak((335, 105), streak_standard)
    draw_streak((55, 310), streak_doubles)
    draw_streak((335, 510), streak_single)

    img.paste(hot_emoji, (160, 110))
    img.paste(paz_emoji, (150, 308))
    img.paste(skull_emoji, (228, 514))
    img.save(output_path, format="JPEG", subsampling=100, quality=100)
    print("Imagen creada exitosamente.")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="pvl-", intents=intents)

# bot.remove_command("help")

@bot.command(name="rank", description="Muestra tu rango de Rocket League de forma dinámica")
async def rank(ctx, *, nickname):
  data = api_fetch(nickname)
  img = create_image(data, nickname)
  await ctx.message.reply(content=f"{ctx.author.mention}", file=discord.File(output_path))
  #await ctx.send(f"[LOG] Nickname: {nickname}")

@bot.event
async def on_ready():
    print(f"Logueado exitosamente como: {bot.user}")
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="como ivan se pajea"
        )
    )

bot.run("{TOKEN}") #DISCORD TOKEN
