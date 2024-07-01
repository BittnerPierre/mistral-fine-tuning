# MISTRAL FINE-TUNING HACKATHON PROJECT

## Project Goals
Goals of the project is to create a pipeline that produce fine-tuned models that are able to edit and revised youtube video scripts that ensure a consistent personnal tone & structure and content.

## Project code structure
Source code of the pipeline is in src/video_script:
- Step_1_-_extract_video_details.py
- Step_2_-_synthesize_video_script.py
- Step_3_-_critic_video_script.py
- Step_4_-_enforce_specific_style.py
- Step_5_-_measure_progress.py
- Step_6_-_final_enhancement_test.py
- Step_7_-_critic_enhanced_video_script.py

Each steps use file produced by previsous one.

Prompt and evaluation framework can be found in: 
- src/video_script/video_prompt.py

![The project pipeline](/Diapositive1.jpeg "Project Pipeline")

Project use poetry for managing dependencies.

Produced files are in src/video_script/data/results.
- generated_video_conversation.jsonl is file used for training model. We have trained a mistral-small-latest model.

Training dataset is around 1000 videos on GenAI. Generation of original video script is part of the pipeline.

Notebook for model training, unitary test and generate video script of the video is located in:
- src/mistral_finetune_api_video.ipynb

Final Fine-tuned model is "ft:mistral-small-latest:c056c2e4:20240628:f732bd21"
It is based on mistral-small-latest.

To display the result of benchmark :
- src/video_script/step_8_-_statistics.py

``` step_8_-_statistics.py
/Users/pierrebittner/Library/Caches/pypoetry/virtualenvs/mistral-fine-tuning-HF3LZeAg-py3.10/bin/python /Users/pierrebittner/Documents/GitHub/mistral-fine-tuning/src/video_script/step_8_-_statistics.py 
------ Initial statistics
Initial / Average: 6.26024, Tone: 7.19397, Structure and content: 5.33728
------ Mistral Small Fine Tuned statistics
Mistral Small Fine Tuned  / Average: 6.51767, Tone: 7.33264, Structure and content: 5.73493
------ Mistral Small statistics
Mistral Small / Average: 6.64936, Tone: 7.44861, Structure and content: 5.86296
------ Mistral Large statistics
Mistral Large / Average: 6.92848, Tone: 7.68582, Structure and content: 6.23627

Process finished with exit code 0
```

``` Step_5a_-_print_score.py 
/Users/pierrebittner/Library/Caches/pypoetry/virtualenvs/mistral-fine-tuning-HF3LZeAg-py3.10/bin/python /Users/pierrebittner/Documents/GitHub/mistral-fine-tuning/src/video_script/Step_5a_-_print_score.py 
------
Initial Average Overall Score: 6.26024
Enhanced Average Overall Score: 7.18103
------
Average Overall Improvement: 0.9208
Average Tone Improvement: 0.76401
Average Structure and Content Improvement: 1.16595
------
Statistics excluding negative overall improvements:
Initial Average Overall Score: 5.97207
Enhanced Average Overall Score: 7.35505
------
Average Overall Improvement: 1.38298
Average Tone Improvement: 1.1117
Average Structure and Content Improvement: 1.68085
------
Statistics excluding postive overall improvements:
Initial Average Overall Score: 7.49148
Enhanced Average Overall Score: 6.4375
------
Average Overall Improvement: -1.05398
Average Tone Improvement: -0.72159
Average Structure and Content Improvement: -1.03409

Process finished with exit code 0
```

 ![The project benchmakr](/Diapositive3.jpeg "Project Benchmark")
