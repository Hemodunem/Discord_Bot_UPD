import discord
from discord import utils, Intents

from bot_db import activity_new
from token_storage import token

POST_ID = 817054917415796776

CHANNEL_TO_SPREAD_ID = 817050403484336132

ROLES = {
    '1️⃣': 817056742697336882,
    '2️⃣': 817057140535590942,
    '3️⃣': 817057299558039582,
    '4': 830359760393601044
}

BLACK_LIST = [
    'привет',
    'пока',
    'каркас',
    'чижи'
]

client = discord.Client(intents=Intents.all())


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # role = message.guild.get_role(820240223506006058)
    # await role.delete()

    member = message.author
    split_content = message.content.split()
    guild = member.guild
    if any(word.lower() in BLACK_LIST for word in split_content):
        await guild.kick(member, reason=None)
        await message.delete(delay=None)
        await message.channel.send(f'{member.display_name} забанен')
    if activity_new(member.id, len(split_content)):
        role = guild.get_role(ROLES['4'])
        await member.add_roles(role)


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == POST_ID:
        channel = client.get_channel(payload.channel_id)  # получаем объект канала
        message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения

        member = payload.member  # получаем объект пользователя который поставил реакцию
        guild = message.guild

        try:
            emoji = str(payload.emoji)  # эмоджи который выбрал юзер
            role_id = ROLES[emoji]  # объект выбранной роли (если есть)
            role = utils.get(guild.roles, id=role_id)
            await member.add_roles(role)
            print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))

        except KeyError:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))


@client.event
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(payload.channel_id)  # получаем объект канала
    message = await channel.fetch_message(payload.message_id)  # получаем объект сообщения
    guild = message.guild
    member = utils.get(guild.members, id=payload.user_id)
    emoji = str(payload.emoji)  # эмоджи который выбрал юзер
    try:
        role = utils.get(message.guild.roles, id=ROLES[emoji])  # объект выбранной роли (если есть)

        await member.remove_roles(role)
        print('[SUCCESS] Role {1.name} has been removed for user {0.display_name}'.format(member, role))

    except KeyError:
        print('[ERROR] KeyError, no role found for ' + emoji)
    except Exception as e:
        print(repr(e))


@client.event
async def on_voice_state_update(member, before, after):
    await move_user_to_his_channel(member, before, after)
    await remove_user_channel_if_needed(member, before, after)


async def move_user_to_his_channel(member, before, after):
    if after.channel is None:
        return
    if after.channel.id != CHANNEL_TO_SPREAD_ID:
        return

    category = utils.get(member.guild.categories, id=830351078087983105)

    channel = await member.guild.create_voice_channel(name=str(member)[0:-5] + "'s channel", category=category)
    await member.move_to(channel)


async def remove_user_channel_if_needed(member, before, after):
    if before.channel is None:
        return

    if before.channel.category_id != 830351078087983105:
        return

    if len(before.channel.members) < 1:
        await before.channel.delete()


def give_role4(member_id):
    member = (member_id)
    member.add_roles('4')


# RUN

client.run(token)
