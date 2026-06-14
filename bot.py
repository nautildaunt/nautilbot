import discord
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio
import os
import random

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    print("❌ DISCORD_TOKEN이 설정되지 않았습니다.", flush=True)
    exit()

CHANNEL_ID = 1515335921854316664
ROLE_ID = 1515334567446183967

# 봇 인스턴스 번호
BOT_INSTANCE = random.randint(1000, 9999)

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def scheduled_message():

    await client.wait_until_ready()

    print("✅ 스케줄러 시작", flush=True)
    print(f"BOT_INSTANCE = {BOT_INSTANCE}", flush=True)

    channel = client.get_channel(CHANNEL_ID)

    if channel is None:
        channel = await client.fetch_channel(CHANNEL_ID)

    now = datetime.now(ZoneInfo("Asia/Seoul"))

    # 테스트용 : 1분 후
    target = now + timedelta(minutes=1)

    wait_seconds = (target - now).total_seconds()

    print("=" * 50, flush=True)
    print(f"현재 시각(KST): {now}", flush=True)
    print(f"테스트 전송 예정(KST): {target}", flush=True)
    print(f"{wait_seconds:.0f}초 대기", flush=True)
    print("=" * 50, flush=True)

    await asyncio.sleep(wait_seconds)

    await channel.send(
        f"# 테스트 메시지입니다! [{BOT_INSTANCE}] <@&{ROLE_ID}>"
    )

    print(
        f"✅ 테스트 메시지 전송 완료 [{BOT_INSTANCE}]",
        flush=True
    )


@client.event
async def on_ready():

    print("=" * 50, flush=True)
    print("로그인 완료", flush=True)
    print(f"봇 이름 : {client.user}", flush=True)
    print(f"봇 ID : {client.user.id}", flush=True)
    print(f"BOT_INSTANCE : {BOT_INSTANCE}", flush=True)
    print("=" * 50, flush=True)

    client.loop.create_task(
        scheduled_message()
    )


client.run(TOKEN)
