import discord
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import asyncio
import os

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    print("❌ DISCORD_TOKEN이 설정되지 않았습니다.", flush=True)
    exit()

CHANNEL_ID = 1515335921854316664
ROLE_ID = 1515334567446183967

intents = discord.Intents.default()
client = discord.Client(intents=intents)


async def scheduled_message():

    await client.wait_until_ready()

    print("✅ 스케줄러 시작", flush=True)

    # 채널 가져오기
    channel = client.get_channel(CHANNEL_ID)

    if channel is None:

        try:

            channel = await client.fetch_channel(
                CHANNEL_ID
            )

        except Exception as e:

            print(
                f"❌ 채널을 찾지 못함: {e}",
                flush=True
            )

            return

    # 현재 한국 시간
    now = datetime.now(
        ZoneInfo("Asia/Seoul")
    )

    # 오늘 오후 5시
    first_time = now.replace(
        hour=17,
        minute=0,
        second=0,
        microsecond=0
    )

    # 이미 5시가 지났으면 내일 5시부터 시작
    if now >= first_time:

        first_time += timedelta(days=1)

    wait_seconds = (
        first_time - now
    ).total_seconds()

    print("=" * 50, flush=True)

    print(
        f"현재 시각(KST): {now}",
        flush=True
    )

    print(
        f"첫 전송 예정(KST): {first_time}",
        flush=True
    )

    print(
        f"첫 메시지까지 {wait_seconds:.0f}초 대기",
        flush=True
    )

    print("=" * 50, flush=True)

    # 오후 5시까지 대기
    await asyncio.sleep(
        wait_seconds
    )

    # 이후 20시간마다 반복
    while not client.is_closed():

        try:

            await channel.send(
                f"# 블랙마켓이 시작되었습니다 <@&{ROLE_ID}>"
            )

            send_time = datetime.now(
                ZoneInfo("Asia/Seoul")
            )

            print(
                f"✅ 메시지 전송 완료 ({send_time})",
                flush=True
            )

        except Exception as e:

            print(
                f"❌ 메시지 전송 실패: {e}",
                flush=True
            )

        print(
            "다음 메시지까지 20시간 대기",
            flush=True
        )

        await asyncio.sleep(
            20 * 60 * 60
        )


@client.event
async def on_ready():

    print("=" * 50, flush=True)

    print(
        "로그인 완료",
        flush=True
    )

    print(
        f"봇 이름 : {client.user}",
        flush=True
    )

    print(
        f"봇 ID : {client.user.id}",
        flush=True
    )

    # 🔽 스트리밍 상태 설정
    activity = discord.Streaming(
        name="📢 노틸을 위해서 열심히 일하기!",
        url="https://www.twitch.tv/nautlidauntiscute"
    )

    await client.change_presence(
        status=discord.Status.online,
        activity=activity
    )

    print(
        "🟣 스트리밍 상태 적용 완료",
        flush=True
    )

    print("=" * 50, flush=True)

    # 중복 실행 방지
    if not hasattr(
        client,
        "scheduler_started"
    ):

        client.scheduler_started = True

        print(
            "✅ scheduled_message 시작",
            flush=True
        )

        asyncio.create_task(
            scheduled_message()
        )


client.run(TOKEN)
