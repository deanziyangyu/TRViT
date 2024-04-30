import openai
import base64
import mimetypes
from pathlib import Path
import requests
import json

# client = openai.OpenAI(
#     base_url="http://localhost:8080/v1", # "http://<Your api-server IP>:port"
#     api_key = "sk-no-key-required"
# )

def image_to_base64(image_path):
    # Guess the MIME type of the image
    mime_type, _ = mimetypes.guess_type(image_path)

    if not mime_type or not mime_type.startswith('image'):
        raise ValueError("The file type is not recognized as an image")
    
    # Read the image binary data
    with open(image_path, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    
    return encoded_string

stage_1_b64 = image_to_base64("./store/NE_ID5_Es2_7_s=0/0005.png")
stage_2_b64 = image_to_base64("./store/NE_ID5_Es2_7_s=0/0055.png")
stage_3_b64 = image_to_base64("./store/NE_ID5_Es2_7_s=0/0085.png")


with open("./struc_data/exec_descs/exec_1_desc.json") as f:
	exe_1_desc_json = json.dumps(json.load(f))

with open("./struc_data/exec_descs/exec_2_desc.json") as f:
	exe_2_desc_json = json.dumps(json.load(f))

with open("./struc_data/eval_format.json") as f:
	eval_format_json = json.dumps(json.load(f))

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

score = 2

json_data = {
    "stream":False,
    "n_predict":1024,
    "temperature":0.5,
    "stop":[
        "</s>",
        "Llama:",
        "User:"
    ],
    "repeat_last_n":256,
    "repeat_penalty":1.18,
    "top_k":40,
    "top_p":0.95,
    "min_p":0.05,
    "tfs_z":1,
    "typical_p":1,
    "presence_penalty":0,
    "frequency_penalty":0,
    "mirostat":0,
    "mirostat_tau":5,
    "mirostat_eta":0.1,
    "grammar":"",
    "n_probs":0,
    "min_keep":0,
	"image_data": [
		{
			"data": stage_1_b64,
			"id": 12
		},
        {
			"data": stage_2_b64,
			"id": 13
		},		
        {
			"data": stage_3_b64,
			"id": 14
		}
	],
    "cache_prompt":True,
    "api_key":"",
    "slot_id":0,
    "prompt": f"You are an AI assistant that give movement feedback to patient doing rehabilitation exercises \
		by analyzing skeleton graphs captured by a camera system with the help of the result from a custom model. You can provide a step-by-step reasoning before providing your answer, \
		or responds with `I don't know the answer` if you are unsure.\nUSER:{user_intro+background_text}.\nASSISTANT:Please assign me with a task.\nUSER:{task_rep_desc}.\nASSISTANT:I am ready for the inputs.\nUSER:The following input is in the order of 1. exercise description json 2. Three skeleton Graphs 3. output json. \
				The actual evaluation score from the model is {score}.\
                \n {exe_2_desc_json}. \
                \n[img-12] Here is the first stage. \
                \n[img-13] Here is the second stage. \
                \n[img-14] Here is the third stage. \
                \n Here is the Evaluation Format: {eval_format_json}. Remember, provide your answers in json only.\
                \nASSISTANT:"
}

url = 'http://localhost:8080/completion'
headers = {'Content-Type': 'application/json'}
response = requests.post(url=url,headers=headers, data=json.dumps(json_data))
print(response.content)
