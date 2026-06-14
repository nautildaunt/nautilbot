import discord
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio
import os

# =========================
# 환경 변수
# =========================

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    print("❌ DISCORD_TOKEN이 설정되지 않았습니다.")
    exit()

CHANNEL_ID = 1515335921854316664
ROLE_ID = 1515334567446183967

# =========================
# Discord 설정
# =========================

intents = discord.Intents.default()

client = discord.Client(intents=intents)


# =========================
# 자동 전송 함수
# =========================

async def scheduled_message():

    await client.wait_until_ready()

    print("✅ 스케줄러 시작")

    while not client.is_closed():

        # 채널 가져오기
        channel = client.get_channel(CHANNEL_ID)

        if channel is None:
            try:
                channel = await client.fetch_channel(CHANNEL_ID)
            except Exception as e:
                print(f"❌ 채널을 찾지 못함: {e}")
                await asyncio.sleep(60)
                continue

        # 현재 한국 시간
        now = datetime.now(ZoneInfo("Asia/Seoul"))

        # 오늘 오후 5시
        target = now.replace(
            hour=17,
            minute=0,
            second=0,
            microsecond=0
        )

        # 이미 지났으면 내일 오후 5시
        if now >= target:
            target += timedelta(days=1)

        wait_seconds = (target - now).total_seconds()

        print("=" * 50)
        print(f"현재 시각(KST): {now}")
        print(f"다음 전송 예정(KST): {target}")
        print(f"{wait_seconds:.0f}초 대기")
        print("=" * 50)

        await asyncio.sleep(wait_seconds)

        try:

            await channel.send(
                f"# 블랙마켓이 시작되었습니다 <@&1515334567446183967> "
            )

            send_time = datetime.now(
                ZoneInfo("Asia/Seoul")
            )

            print(
                f"✅ 메시지 전송 완료 ({send_time})"
            )

        except Exception as e:

            print(
                f"❌ 메시지 전송 실패: {e}"
            )

            await asyncio.sleep(60)


# =========================
# 봇 실행 이벤트
# =========================

@client.event
async def on_ready():

    print("=" * 50)
    print(f"로그인 완료")
    print(f"봇 이름 : {client.user}")
    print(f"봇 ID : {client.user.id}")
    print("=" * 50)

    if not hasattr(client, "scheduler_started"):

        client.scheduler_started = True

        client.loop.create_task(
            scheduled_message()
        )


# =========================
# 실행
# =========================

client.run(TOKEN)
