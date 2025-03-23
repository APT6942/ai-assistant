import asyncio

from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import openai, silero
from api import AssistantFnc

load_dotenv()


async def entrypoint(ctx: JobContext):
    initial_ctx = llm.ChatContext().append(
        role="system",
        text=(
            "You are a voice assistant created by LiveKit. Your interface with users will be voice. "
            "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
        ),
    )
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    fnc_ctx = AssistantFnc()

    assitant = VoiceAssistant(
        vad=silero.VAD.load(),   #model to detect when user is speaking 
        stt=openai.STT(),        #openai speech totext
        llm=openai.LLM(),        # which llm we want to use 
        tts=openai.TTS(),       # whcih text to speech to use
        chat_ctx=initial_ctx,   #context of app
        fnc_ctx=fnc_ctx,
    )
    assitant.start(ctx.room)   #connect to a room and start assistant inside the room

    await asyncio.sleep(1)
    await assitant.say("Hey, how can I help you today!", allow_interruptions=True) # allow to inteerupt voice assistant


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
