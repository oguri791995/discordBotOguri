# インストールした discord.py を読み込む
import discord

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'XXXXXXXXX'
notice_channel_id = None

intents = discord.Intents.default()
intents.members = True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)
users = client


# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしました')


# 発言時に実行されるイベントハンドラを定義
@client.event
async def on_message(message):
    global notice_channel_id

    if message.content == "!set":
        notice_channel_id = message.channel.id
        await message.channel.send("このテキストチャンネルに通知設定をしました。\nチャットをすると毎回メンションが届きます。")
    elif message.content == "!unset":
        notice_channel_id = None
        await message.channel.send("通知設定を解除しました。")

    channel_ids = []
    for channel in message.guild.text_channels:
        channel_ids.append(channel.id)

    # if notice_channel_id not in channel_ids:
    if notice_channel_id is None or notice_channel_id not in channel_ids:
        # print("return")
        return

    await other_than_the_author(message)


# 本人以外を取得(BOT以外)
async def other_than_the_author(author):
    members = author.guild.members
    notice_channel = client.get_channel(notice_channel_id)
    # print(notice_channel_id)

    if author.author.bot:
        return

    for member in members:
        if not member.bot and author.author.id != member.id:
            await notice_channel.send(member.mention)


# ボイスチャンネルに変化(入退出など)に対するイベントハンドラ
@client.event
async def on_voice_state_update(member, beforeState, afterState):
    channel_ids = []
    for channel in member.guild.text_channels:
        channel_ids.append(channel.id)

    if notice_channel_id is None or notice_channel_id not in channel_ids:
        return

    members = member.guild.members
    notice_channel = client.get_channel(notice_channel_id)

    if beforeState.channel is None:  # VCへの入室時
        if member.bot:
            return

        for user in members:
            if not user.bot and member.id != user.id:
                await notice_channel.send(user.mention)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
