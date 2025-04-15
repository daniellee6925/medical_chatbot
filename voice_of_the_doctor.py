# Step1a: Setup Text to Speech–TTS–model with gTTS
from gtts import gTTS
from pydub import AudioSegment
import platform
import subprocess
import os
import elevenlabs
from elevenlabs import ElevenLabs, save

ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")
input_text = "Testing Audio one two three"


def text_to_speech_with_gtts_old(input_text, output_filepath):
    language = "en"

    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)


# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")


# --------------------------------------------------------------------------
def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2",
    )
    elevenlabs.save(audio, output_filepath)


# text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3")


# --------------------------------------------------------------------------
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    mp3_filepath = (
        output_filepath
        if output_filepath.endswith(".mp3")
        else output_filepath + ".mp3"
    )
    wav_filepath = output_filepath.replace(".mp3", ".wav")

    # Generate MP3
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(mp3_filepath)

    # Convert to WAV using pydub
    sound = AudioSegment.from_mp3(mp3_filepath)
    sound.export(wav_filepath, format="wav")

    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(["afplay", wav_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(
                [
                    "powershell",
                    "-c",
                    f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();',
                ]
            )
        elif os_name == "Linux":  # Linux
            subprocess.run(["aplay", wav_filepath])  # or 'ffplay', 'mpg123'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# --------------------------------------------------------------------------
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

    mp3_filepath = (
        output_filepath
        if output_filepath.endswith(".mp3")
        else output_filepath + ".mp3"
    )
    wav_filepath = output_filepath.replace(".mp3", ".wav")

    # Generate MP3
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2",
    )
    save(audio, mp3_filepath)

    # Convert MP3 to WAV
    sound = AudioSegment.from_mp3(mp3_filepath)
    sound.export(wav_filepath, format="wav")

    # Play the WAV file
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(["afplay", wav_filepath])
        elif os_name == "Windows":  # Windows
            subprocess.run(
                [
                    "powershell",
                    "-c",
                    f'(New-Object Media.SoundPlayer "{wav_filepath}").PlaySync();',
                ]
            )
        elif os_name == "Linux":  # Linux
            subprocess.run(["aplay", wav_filepath])  # or 'ffplay', 'mpg123'
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# --------------------------------------------------------------------------
# test
"""
text_to_speech_with_gtts(
    input_text=input_text, output_filepath="gtts_testing_autoplay.mp3"
)

text_to_speech_with_elevenlabs(
    input_text, output_filepath="elevenlabs_testing_autoplay.mp3"
)
"""
