

## Text To Speech (TTS) With Gradio Plugin 


## Install TTS

```bash
pip install TTS
```

If you plan to code or train models, clone TTS and install it locally.

```bash
git clone https://github.com/saba99/TTS-MultiLingual
pip install -e .[all,dev,notebooks]  # Select the relevant extras
```

If you are on Ubuntu (Debian), you can also run following commands for installation.

```bash
$ make system-deps  # intended to be used on Ubuntu (Debian). Let us know if you have a different OS.
$ make install
```

## Synthesizing speech by TTS

### 🐍 Python API

```python
from TTS.api import TTS

# Running a multi-speaker and multi-lingual model

# List available TTS models and choose the first one
model_name = TTS.list_models()[0]
# Init TTS
tts = TTS(model_name)
# Run TTS
# Since this model is multi-speaker and multi-lingual, we must set the target speaker and the language
# Text to speech with a numpy output
wav = tts.tts("This is a test! This is also a test!!", speaker=tts.speakers[0], language=tts.languages[0])
# Text to speech to a file
tts.tts_to_file(text="Hello world!", speaker=tts.speakers[0], language=tts.languages[0], file_path="output.wav")

# Running a single speaker model

# Init TTS with the target model name
tts = TTS(model_name="tts_models/de/thorsten/tacotron2-DDC", progress_bar=False, gpu=False)
# Run TTS
tts.tts_to_file(text="Ich bin eine Testnachricht.", file_path=OUTPUT_PATH)

# Example voice cloning with YourTTS in English, French and Portuguese:
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts", progress_bar=False, gpu=True)
tts.tts_to_file("This is voice cloning.", speaker_wav="my/cloning/audio.wav", language="en", file_path="output.wav")
tts.tts_to_file("C'est le clonage de la voix.", speaker_wav="my/cloning/audio.wav", language="fr-fr", file_path="output.wav")
tts.tts_to_file("Isso é clonagem de voz.", speaker_wav="my/cloning/audio.wav", language="pt-br", file_path="output.wav")


# Example voice conversion converting speaker of the `source_wav` to the speaker of the `target_wav`

tts = TTS(model_name="voice_conversion_models/multilingual/vctk/freevc24", progress_bar=False, gpu=True)
tts.voice_conversion_to_file(source_wav="my/source.wav", target_wav="my/target.wav", file_path="output.wav")

# Example voice cloning by a single speaker TTS model combining with the voice conversion model. This way, you can
# clone voices by using any model in TTS.

tts = TTS("tts_models/de/thorsten/tacotron2-DDC")
tts.tts_with_vc_to_file(
    "Wie sage ich auf Italienisch, dass ich dich liebe?",
    speaker_wav="target/speaker.wav",
    file_path="ouptut.wav"
)

# Example text to speech using [Coqui Studio](https://coqui.ai) models. You can use all of your available speakers in the studio.
# [Coqui Studio](https://coqui.ai) API token is required. You can get it from the [account page](https://coqui.ai/account).
# You should set the `COQUI_STUDIO_TOKEN` environment variable to use the API token.

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

## Output Audio

<table class="center">
<tr>
  <td style="text-align:center;"><b>Short Example</b></td>
  <td style="text-align:center;"><b>Short Example</b></td>
   <td style="text-align:center;"><b>Short Example</b></td>
</tr>
  
<tr>
 <td>


https://user-images.githubusercontent.com/33378412/235578067-2f87fa05-a3ad-4387-ab02-c44acd5506fd.mp4


</td>
  <td>
  

https://user-images.githubusercontent.com/33378412/235578084-01157592-f9f5-4cac-b198-0d3fe14460ed.mp4


  </td>
  <td>

https://user-images.githubusercontent.com/33378412/235578127-2dba010a-18a1-4206-a2b5-aef120118046.mp4


</td>
</tr>

<tr>
  <td width=25% style="text-align:center;color:gray;">rainbow is a meteorological phenomenon that is caused by reflection, refraction and dispersion of light</td>
  <td width=25% style="text-align:center;">The driver learned his lesson. He will never drive in the wind again</td>
  <td width=25% style="text-align:center;"> The people outside are bending over. The wind makes it hard to walk</td>
</tr>

<tr>
  <td style="text-align:center;"><b>Long Example</b></td>
  <td style="text-align:center;"><b>Long Example</b></td>
   <td style="text-align:center;"><b>Long Example</b></td>
</tr>
<tr>
  <td>

https://user-images.githubusercontent.com/33378412/235578423-ada6252f-513b-4acf-bad6-6e6de3ed205b.mp4


  </td>
  <td>


https://user-images.githubusercontent.com/33378412/235578512-05197fb7-f313-4e7c-b5ca-c1239243252c.mp4



  </td>
  <td>


https://user-images.githubusercontent.com/33378412/235578601-60e59794-4ffc-4ac9-8b28-5e31463d6d85.mp4


  </td>              
 
</tr>


<tr>
  <td width=25% style="text-align:center;color:gray;">The tree was full of red apples. 
The farmer was riding his brown horse. He stopped under the tree. He reached out and picked an apple off a branch. 
He bit into the raw apple. He enjoyed the apple. His horse turned its head to look at him. The farmer picked another apple off the tree. He gave it to the horse. The horse ate the raw apple. The horse enjoyed the apple. The farmer put a dozen apples into a bag. He rode the horse back home. He put the horse in the barn. He walked into his house. The cat rubbed up against his leg. He gave the cat a bowl of warm milk.
/td>
  <td width=25% style="text-align:center;">The black cat jumped up onto the chair. It looked down at the white dog.
 The dog was chewing on a bone. The cat jumped onto the dog. The dog kept chewing the bone. 
The cat played with the dog’s tail. The dog kept chewing the bone. The cat jumped back onto the chair.
 It started licking its paws. The dog stood up. It looked at the cat. It licked the cat’s fur.
 The cat licked the dog’s nose. The dog went back to its bone. A boy ran through the room. He was wearing a yellow shirt. He almost ran into the chair. The cat jumped off the chair. The cat jumped onto the sofa.
</td>
  <td width=25% style="text-align:center;">The farmer drives a tractor. The tractor digs up the ground. He plants yellow corn in the ground.
 He plants the yellow corn in the spring. The corn grows in the summer. The rain helps the corn grow. 
If there is no rain, the corn dies. If there is a lot of rain, there is a lot of corn. He harvests the yellow corn in late summer.
 He sells the corn at his vegetable stand. He sells one ear for 25 cents. He sells four ears for $1.
 He sells all his corn in just one month. The neighbors love his corn. The corn is fresh. It is bright yellow. It is tasty.
 It is delicious. The birds love his corn, too. They don’t pay for it. They eat it while it is in the field
</td>
 </tr>
 
 <tr>
  <td style="text-align:center;"><b>Multilingual Support  : English</b></td>
  <td style="text-align:center;"><b>Multilingual Support  : French</b></td>
   <td style="text-align:center;"><b>Multilingual Support : Dutch</b></td>
</tr>

<tr>
  <td>


https://user-images.githubusercontent.com/33378412/235579386-368bddcc-4cb1-42bb-b6fb-241a71273c30.mp4


  </td>
  <td>
  

https://user-images.githubusercontent.com/33378412/235579023-359decbf-d27d-4c69-a5e6-0fe749ea15a8.mp4


  </td>              
  <td>
  
https://user-images.githubusercontent.com/33378412/235579052-5cbe64e3-c171-4c99-8667-44b325d2ba2d.mp4


  </td>
</tr>
<tr>
  <td width=25% style="text-align:center;color:gray;">Dark clouds were in the sky. The sun went down. The weather got cold. The wind started to blow.
 Leaves blew off the trees. Paper flew through the air. People buttoned their jackets. 
The rain started to fall. At first, it was quiet. Then it got louder</td>
  <td width=25% style="text-align:center;">Un arcoíris o arco iris es un fenómeno óptico y meteorológico que consiste en la aparición en el cielo de un arco de luz multicolor</td>
  <td width=25% style="text-align:center;"Een regenboog is een gekleurde cirkelboog die aan de hemel waargenomen kan worden als de, laagstaande</td>

 
</tr>


</table>



### Command line `tts`
#### Single Speaker Models

- List provided models:

    ```
    $ tts --list_models
    ```
- Get model info (for both tts_models and vocoder_models):

       ```
       $ tts --model_info_by_name tts_models/tr/common-voice/glow-tts
        ```
        ```
        $ tts --model_info_by_name vocoder_models/en/ljspeech/hifigan_v2
        ```
    
       
- Run TTS with default models:

  For example:

    ```
    $ tts --text "Text for TTS" --model_name "tts_models/en/ljspeech/glow-tts" --out_path output/path/speech.wav
    ```

#### Multi-speaker Models


- Run your own multi-speaker TTS model:

    ```
    $ tts --text "Text for TTS" --out_path output/path/speech.wav --model_path path/to/model.pth --config_path path/to/config.json --speakers_file_path path/to/speaker.json --speaker_idx <speaker_id>
    ```


## Directory Structure
```
|- notebooks/       (Jupyter Notebooks for model evaluation, parameter selection and data analysis.)
|- utils/           (common utilities.)
|- TTS
    |- bin/             (folder for all the executables.)
      |- train*.py                  (train your target model.)
      |- ...
    |- tts/             (text to speech models)
        |- layers/          (model layer definitions)
        |- models/          (model definitions)
        |- utils/           (model specific utilities.)
    |- speaker_encoder/ (Speaker Encoder models.)
        |- (same)
    |- vocoder/         (Vocoder models.)
        |- (same)
```
