(synthesizing_speech)=
# Synthesizing Speech

First, you need to install TTS. We recommend using PyPi. You need to call the command below:

```bash
$ pip install TTS
```

After the installation, 2 terminal commands are available.

1. TTS Command Line Interface (CLI). - `tts`
2. Local Demo Server. - `tts-server`
3. In 🐍Python. - `from TTS.api import TTS`

## On the Commandline - `tts`
![cli.gif](https://github.com/coqui-ai/TTS/raw/main/images/tts_cli.gif)

After the installation, 🐸TTS provides a CLI interface for synthesizing speech using pre-trained models. You can either use your own model or the release models under 🐸TTS.

Listing released 🐸TTS models.

```bash
tts --list_models
```

Run a TTS model, from the release models list, with its default vocoder. (Simply copy and paste the full model names from the list as arguments for the command below.)

```bash
tts --text "Text for TTS" \
    --model_name "<type>/<language>/<dataset>/<model_name>" \
    --out_path folder/to/save/output.wav
```

Run a tts and a vocoder model from the released model list. Note that not every vocoder is compatible with every TTS model.

```bash
tts --text "Text for TTS" \
    --model_name "tts_models/<language>/<dataset>/<model_name>" \
    --vocoder_name "vocoder_models/<language>/<dataset>/<model_name>" \
    --out_path folder/to/save/output.wav
```

Run your own TTS model (Using Griffin-Lim Vocoder)

```bash
tts --text "Text for TTS" \
    --model_path path/to/model.pth \
    --config_path path/to/config.json \
    --out_path folder/to/save/output.wav
```

Run your own TTS and Vocoder models

```bash
tts --text "Text for TTS" \
    --config_path path/to/config.json \
    --model_path path/to/model.pth \
    --out_path folder/to/save/output.wav \
    --vocoder_path path/to/vocoder.pth \
    --vocoder_config_path path/to/vocoder_config.json
```

Run a multi-speaker TTS model from the released models list.

```bash
tts --model_name "tts_models/<language>/<dataset>/<model_name>"  --list_speaker_idxs  # list the possible speaker IDs.
tts --text "Text for TTS." --out_path output/path/speech.wav --model_name "tts_models/<language>/<dataset>/<model_name>"  --speaker_idx "<speaker_id>"
```

Run a released voice conversion model

```bash
tts --model_name "voice_conversion/<language>/<dataset>/<model_name>"
    --source_wav "my/source/speaker/audio.wav"
    --target_wav "my/target/speaker/audio.wav"
    --out_path folder/to/save/output.wav
```

**Note:** You can use ```./TTS/bin/synthesize.py``` if you prefer running ```tts``` from the TTS project folder.

## On the Demo Server - `tts-server`

 <!-- <img src="https://raw.githubusercontent.com/coqui-ai/TTS/main/images/demo_server.gif" height="56"/> -->
![server.gif](https://github.com/coqui-ai/TTS/raw/main/images/demo_server.gif)

You can boot up a demo 🐸TTS server to run an inference with your models. Note that the server is not optimized for performance
but gives you an easy way to interact with the models.

The demo server provides pretty much the same interface as the CLI command.

```bash
tts-server -h # see the help
tts-server --list_models  # list the available models.
```

Run a TTS model, from the release models list, with its default vocoder.
If the model you choose is a multi-speaker TTS model, you can select different speakers on the Web interface and synthesize
speech.

```bash
tts-server --model_name "<type>/<language>/<dataset>/<model_name>"
```

Run a TTS and a vocoder model from the released model list. Note that not every vocoder is compatible with every TTS model.

```bash
tts-server --model_name "<type>/<language>/<dataset>/<model_name>" \
           --vocoder_name "<type>/<language>/<dataset>/<model_name>"
```

## Python 🐸TTS API

You can run a multi-speaker and multi-lingual model in Python as

```python
from TTS.api import TTS

# List available 🐸TTS models and choose the first one
model_name = TTS.list_models()[0]
# Init TTS
tts = TTS(model_name)
# Run TTS
# ❗ Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
# Text to speech with a numpy output
wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])
# Text to speech to a file
tts.tts_to_file(text="Hello world!", speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")
```

Here is an example for a single speaker model.

```python
# Init TTS with the target model name
tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False, gpu=False)
# Run TTS
tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path=OUTPUT_PATH)
```

Example voice cloning with YourTTS in English, French and Portuguese:

```python
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=True)
tts.tts_to_file("This is voice cloning.", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
tts.tts_to_file("C'est le clonage de la voix.", speaker_wav="my/cloning/audio.wav", language="fr", file_path="output.wav")
tts.tts_to_file("Isso é clonagem de voz.", speaker_wav="my/cloning/audio.wav", language="pt", file_path="output.wav")
```

Example voice conversion converting speaker of the `source_wav` to the speaker of the `target_wav`

```python
tts = TTS(model_name="voice_conversion_models/multilingual/vctk/freevc24", progress_bar=False, gpu=True)
tts.voice_conversion_to_file(source_wav="my/source.wav", target_wav="my/target.wav", file_path="output.wav")
```

Example voice cloning by a single speaker TTS model combining with the voice conversion model. This way, you can
clone voices by using any model in 🐸TTS.

```python
tts = TTS("tts_models/de/thorsten/tacotron2-DDC")
tts.tts_with_vc_to_file(
    "Wie sage ich auf Italienisch, dass ich dich liebe?",
    speaker_wav="target/speaker.wav",
    file_path="ouptut.wav"
)

Example text to speech using [🐸Coqui Studio](https://coqui.ai) models. You can use all of your available speakers in the studio.
[🐸Coqui Studio](https://coqui.ai) API token is required. You can get it from the [account page](https://coqui.ai/account).
You should set the `COQUI_STUDIO_TOKEN` environment variable to use the API token.

```python
# If you have a valid API token set you will see the studio speakers as separate models in the list.
# The name format is coqui_studio/en/<studio_speaker_name>/coqui_studio
models = TTS().list_models()
# Init TTS with the target studio speaker
tts = TTS(model_name="coqui_studio/en/Torcull Diarmuid/coqui_studio", progress_bar=False, gpu=False)
# Run TTS
tts.tts_to_file(text="This is a test.", file_path=OUTPUT_PATH)
# Run TTS with emotion and speed control
tts.tts_to_file(text="This is a test.", file_path=OUTPUT_PATH, emotion="Happy", speed=1.5)
```

If you just need 🐸 Coqui Studio speakers, you can use `CS_API`. It is a wrapper around the 🐸 Coqui Studio API.

```python
from TTS.api import CS_API

# Init 🐸 Coqui Studio API
# you can either set the API token as an environment variable `COQUI_STUDIO_TOKEN` or pass it as an argument.
api = CS_API(api_token=<token>)
api.speakers
api.emotions
api.list_speakers()
api.list_voices()
wav, sample_rate = api.tts(text="This is a test.", speaker=api.speakers[0].name, emotion="Happy", speed=1.5)
```