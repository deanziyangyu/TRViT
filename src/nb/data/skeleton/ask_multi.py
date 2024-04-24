from openai import OpenAI
import base64
import mimetypes
from pathlib import Path
import json

with open("./struc_data/exec_descs/exec_1_desc.json") as f:
	exe_1_desc_json = json.dumps(json.load(f))

with open("./struc_data/exec_descs/exec_2_desc.json") as f:
	exe_2_desc_json = json.dumps(json.load(f))

with open("./struc_data/eval_format.json") as f:
	eval_format = json.dumps(json.load(f))

with open("./struc_data/feedback_format.json") as f:
	feedback_format_json = json.dumps(json.load(f))

user_intro = "I am a rehabilitation clinician and I need your help giving me structrual information regarding the skeleton graph. \
    Let me give you some background info on the skeleton."
user_intro_2 = "I am a rehabilitation clinician and I need your help giving me and the patient appropirate feedbacks. \
    Another assistant has done analyzing the skeleton graph and has left you a structual evaluation."

with open("./struc_data/backgrounds_skeletons.txt") as f:
	background_text = f.read()

with open("./struc_data/backgrounds_skeletons_additional.txt") as f:
	additional_info = f.read()


with open("./struc_data/task_descs/rep_desc.txt") as f:
	task_rep_desc = f.read()


with open("./struc_data/task_descs/rep_feedback.txt") as f:
	task_rep_feedback = f.read()


eval_desc = ""

feedback_results = ""


def image_to_base64(image_path):
    # Guess the MIME type of the image
    mime_type, _ = mimetypes.guess_type(image_path)

    if not mime_type or not mime_type.startswith('image'):
        raise ValueError("The file type is not recognized as an image")
    
    # Read the image binary data
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Format the result with the appropriate prefix
    image_base64 = f"data:{mime_type};base64,{encoded_string}"
    
    return image_base64


# SujectCat_ID#_ExerciseEs#_rep#_score=#/frame#.png
stage_1_b64 = image_to_base64("./store/NE_ID5_Es2_7_s=0/0005.png")
stage_2_b64 = image_to_base64("./store/NE_ID5_Es2_7_s=0/0055.png")
stage_3_b64 = image_to_base64("./store/NE_ID5_Es2_7_s=0/0085.png")

use_oai_llm = False

if use_oai_llm:
	key = '' # add your Open AI Key Here
	client = OpenAI(
		api_key=key,
	)
else:
	key = 'sk-xxx'
	client = OpenAI(
		base_url='http://192.168.181.108:8080/v1',
		api_key=key,
	)

task = 1
score = 2

if task == 0:
	response = client.chat.completions.create(
	model="gpt-4",
	messages=[
		{"role": "system", "content": "You are an AI assistant that give movement feedback to patient doing rehabilitation exercises \
		by turning structured data provided by another assistant into verbal suggestions. You can provide a step-by-step reasoning before providing your answer, \
		or responds with `I don't know the answer` if you are unsure."},
		{
		"role": "user",
		"content": [
			{"type": "text", "text": user_intro_2},
		],
		},
		{
		"role": "assistant",
		"content": "Please assign me with a task."
		},
		{
		"role": "user",
		"content": [
			{"type": "text", "text": task_rep_feedback},
		],
		},
		{
		"role": "assistant",
		"content": "I am ready for the inputs."
		},
		{
		"role": "user",
		"content": [
			{
				"type": "text", "text": "The following input is in the order of 1. exercise description json 2. evalutaion description json 3. output json `feedback_format`.",
			},
			{
				"type": "text", "text": exe_2_desc_json, 
			},
			{
				"type": "text", "text": eval_desc, 
			},
			{
				"type": "text", "text": feedback_format_json,
			},
		],
		}
	],
	response_format={"type": "json_object"},
	max_tokens=512,
	)

elif task == 1:

	response = client.chat.completions.create(
	model="gpt-4-turbo-2024-04-09",
	messages=[
		{"role": "system", "content": "You are an AI assistant that give movement feedback to patient doing rehabilitation exercises \
		by analyzing skeleton graphs captured by a camera system with the help of the result from a custom model. You can provide a step-by-step reasoning before providing your answer, \
		or responds with `I don't know the answer` if you are unsure."},
		{
		"role": "user",
		"content": [
			{"type": "text", "text": user_intro+background_text},
		],
		},
		{
		"role": "assistant",
		"content": "Please assign me with a task."
		},
		{
		"role": "user",
		"content": [
			{"type": "text", "text": task_rep_desc},
		],
		},
		{
		"role": "assistant",
		"content": "I am ready for the inputs."
		},
		{
		"role": "user",
		"content": [
			{
				"type": "text", "text": f"The following input is in the order of 1. exercise description json 2. Three skeleton Graphs 3. output json. \
				The actual evaluation score from the model is {score}.",
			},
			{
				"type": "text", "text": exe_2_desc_json,
			},
			{
			"type": "image_url",
			"image_url": {
				"url": stage_1_b64,
			},
			},
			{
			"type": "image_url",
			"image_url": {
				"url": stage_2_b64,
			},
			},
			{
			"type": "image_url",
			"image_url": {
				"url": stage_3_b64,
			},
			},
			{
				"type": "text", "text": eval_format,
			},
		],
		}
	],
	temperature=0.5,
	#   response_format={"type": "json_object"},
	max_tokens=1024,
)

if __name__ == '__main__':
    print(response.usage)
    print(response.choices[0].message.content)
    print(response.choices[0].finish_reason, response.choices[0].index)
    # print(response['choices'][0]['message']['content'])
