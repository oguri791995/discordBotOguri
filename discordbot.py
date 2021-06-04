# インストールした discord.py を読み込む
import discord

# 自分のBotのアクセストークンに置き換えてください
TOKEN = 'XXXXXXXXX'

#  メンション通知をするテキストチャンネルIDを指定
notice_channel_id = 778266062776303616
reboot_notice_channel_id = 782193600591167488

intents = discord.Intents.default()
intents.members = True
notice_trigger = True

# 接続に必要なオブジェクトを生成
client = discord.Client(intents=intents)
notice_channel = None


# 起動時に動作する処理
@client.event
async def on_ready():
    reboot_notice_channel = client.get_channel(reboot_notice_channel_id)
    global notice_channel
    notice_channel = client.get_channel(notice_channel_id)
    # 起動したらターミナルにログイン通知が表示される
    # print('ログインしました')
    #  @everyoneまでたどった
    # await notice_channel.send(client.get_guild(client.guilds[0].id).roles[0])  # @everyoneメンション
    await reboot_notice_channel.send("再起動しました。")


# 発言時に実行されるイベントハンドラを定義
@client.event
async def on_message(message):
    global notice_channel_id, notice_trigger

    if message.content == "!set":
        notice_trigger = True
        await message.channel.send("このテキストチャンネルに通知設定をしました。\nチャットをすると毎回メンションが届きます。")
    elif message.content == "!unset":
        notice_trigger = False
        await message.channel.send("通知設定を解除しました。")

    if notice_trigger:
        await other_than_the_author(message)


# 本人以外を取得(BOT以外)
async def other_than_the_author(author):
    members = author.guild.members

    # 対象がbotなら無視
    if author.author.bot:
        return

    #  ボット以外でかつ発言者以外のメンバーを取得
    for member in members:
        if not member.bot and author.author.id != member.id:
            await notice_channel.send(member.mention)


# ボイスチャンネルに変化(入退出など)に対するイベントハンドラ
@client.event
async def on_voice_state_update(member, beforeState, afterState):
    if not notice_trigger:
        return

    members = member.guild.members

    if beforeState.channel is None:  # VCへの入室時
        if member.bot:
            return

        for user in members:
            if not user.bot and member.id != user.id:
                await notice_channel.send(user.mention)


# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
