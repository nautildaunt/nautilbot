import discord
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = 1515335921854316664

intents = discord.Intents.default()
client = discord.Client(intents=intents)

async def scheduled_message():
await client.wait_until_ready()

```
channel = client.get_channel(CHANNEL_ID)

if channel is None:
    print("채널을 찾을 수 없습니다.")
    return

# 한국 시간(KST)
now = datetime.now(ZoneInfo("Asia/Seoul"))

# 첫 전송 시각: 오늘 17시
first_time = now.replace(
    hour=17,
    minute=0,
    second=0,
    microsecond=0
)

# 이미 17시가 지났다면 내일 17시부터 시작
if now > first_time:
    first_time += timedelta(days=1)

wait_seconds = (first_time - now).total_seconds()

print(f"첫 메시지까지 {wait_seconds:.0f}초 대기")
print(f"현재 시각(KST): {now}")
print(f"첫 전송 예정(KST): {first_time}")

await asyncio.sleep(wait_seconds)

while not client.is_closed():
    await channel.send(
        "# 블랙마켓이 시작되었습니다 <@&1515334567446183967> "
    )

    current_time = datetime.now(ZoneInfo("Asia/Seoul"))
    print(f"메시지 전송 완료 ({current_time})")

    # 20시간 대기
    await asyncio.sleep(20 * 60 * 60)
```

@client.event
async def on_ready():
print(f"로그인 완료: {client.user}")
print("스케줄러 시작")

```
client.loop.create_task(scheduled_message())
```

client.run(TOKEN)
