import requests
import json
import random
import string
import copy
# Randomly fill Jin Questionnaire (multiple choice questions only)
# version 0.1
# Need to capture packets to get the content to fill in
# Questionnaire ID
WID = "38778"
# Original template of questionnaire questions (in JSON string format) - Example content filled in
QUESTIONS_TEMPLATE_JSON = """
[{"c_nums":[],"fillText":"","qt":"single","mc":0,"title":"您的性别：","fillTexts":"","qid":2203189,"extra":{},"answers":[{"selfChoice":true,"value":"男","indexLetter":"A"},{"selfChoice":false,"value":"女","indexLetter":"B"}]
"""

# URL for submission
url = "https://cmapi.molingtech.net/app8/submit-wj/"

headers = {
    "Host": "cmapi.molingtech.net",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a1b)XWEB/13639",
    "Accept": "/",
    "Referer": "https://servicewechat.com/wx3cd7a9e68b144dbf/46/page-frame.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

# Generate openid
def generate_random_lowercase_string(length):
  lowercase_letters = string.ascii_lowercase
  random_string = ''.join(random.choice(lowercase_letters) for i in range(length))
  return random_string

# Submit the questionnaire
def submit_random_survey_response():
    random_openid = generate_random_lowercase_string(28)

    # Parse the global questions template JSON string
    # Use deepcopy to avoid modifying QUESTIONS_TEMPLATE_JSON
    try:
        questions_list = copy.deepcopy(json.loads(QUESTIONS_TEMPLATE_JSON))
    except json.JSONDecodeError:
        print("Error: Failed to parse QUESTIONS_TEMPLATE_JSON.")
        return None # Return None on failure

    # Iterate through each question and perform random selection/answer generation
    for question in questions_list:
        q_type = question.get("qt") # Get question type
        qid = question.get("qid", "N/A") # Get QID for error messages

        if q_type == "single":
            answers = question.get("answers", []) # Get list of options
            if answers: # Ensure there are options
                # First set selfChoice to False for all options
                for answer in answers:
                    answer["selfChoice"] = False
                # Randomly select one option and set its selfChoice to True
                chosen_answer = random.choice(answers)
                chosen_answer["selfChoice"] = True
            else:
                print(f"Warning: Single choice question QID {qid} has no answers.")

        elif q_type == "multiple":
            answers = question.get("answers", [])
            if answers:
                # First set selfChoice to False for all options
                for answer in answers:
                    answer["selfChoice"] = False
                # Randomly choose the number of options to select (at least 1, at most all options)
                num_options = len(answers)
                if num_options > 0:
                    # Ensure at least one option is selected, unless num_options is 0
                    num_to_select = random.randint(1, num_options)
                    # Randomly select a specified number of unique option indices
                    chosen_indices = random.sample(range(num_options), num_to_select)
                    # Set selfChoice to True for the selected options
                    for i in chosen_indices:
                        answers[i]["selfChoice"] = True
                else:
                    print(f"Warning: Multiple choice question QID {qid} has no answers.")

        elif q_type == "rating":
            r_min = question.get("r_min")
            r_max = question.get("r_max")
            # Check if r_min and r_max exist and are numbers
            if isinstance(r_min, (int, float)) and isinstance(r_max, (int, float)) and r_min <= r_max:
                # Randomly generate an integer between r_min and r_max (inclusive)
                random_rating = random.randint(int(r_min), int(r_max))
                question["fillText"] = str(random_rating)
            else:
                 # If rating data is invalid, print a warning
                 print(f"Warning: Invalid rating data for QID {qid} (min: {r_min}, max: {r_max}). Skipping random rating.")


    # Convert the modified questions list back to a JSON string
    modified_questions_json = json.dumps(questions_list)

    # Construct the final request body data
    data = {
        "openid": random_openid,
        "wid": WID,
        "questions": modified_questions_json,
        "ftype": "wj",
        "appname": "dj",
        "fixqnaid": "0" # Fixed value
    }

    # Send the POST request
    try:
        response = requests.post(url, headers=headers, data=data)
        # Print the response
        print("Submission successful!")
        print("Response status code:", response.status_code)
        print("Response content:", response.text)
        return response # Return the response object
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None # Return None indicating failure

# Example: How to call the function to submit a survey once
if __name__ == "__main__":
    print(f"Submitting survey {WID}...")
    submit_random_survey_response()
