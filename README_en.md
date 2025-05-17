[中文](README.md) | English

# Golden Form Random Fill Script (Multiple Choice/Rating Scale Only)

## Project Description

This script is used to automate filling out and submitting Golden Form online questionnaires (mini-program). It randomly selects answers for single-choice and multiple-choice questions, and randomly fills in rating scale questions.

## Important Notes

*   This script is intended for learning and research purposes only. Please do not use it for malicious purposes or violate any website's terms of service. The user assumes all consequences resulting from the use of this script.
*   Packet Capturing is required to obtain the questionnaire's structure data (`QUESTIONS_TEMPLATE_JSON`), questionnaire ID (`WID`), and the submission URL and Headers.
*   Currently, the script only supports processing single-choice (`single`), multiple-choice (`multiple`) and rating scale (`rating`) questions. Other question types (such as fill-in-the-blank, image upload, etc.) cannot be filled correctly.

## Usage Instructions

Capture the POST request to `https://cmapi.molingtech.net/app8/submit-wj/` and obtain the `WID` value. Fill this value into the `WID` variable in the script. Also, obtain the value of the `questions` field from the request body for configuring `QUESTIONS_TEMPLATE_JSON`.

## Configuring QUESTIONS_TEMPLATE_JSON

*   Find the value of the `questions` field in the captured request body. Copy and save its structure. Then, go to the questionnaire page and copy all questions and options. A simple method is to send the captured value, the questions and options from the page, and this repository's code to an AI, asking it to convert it into the format adapted for this script.
*   This JSON string represents the structure of the questionnaire questions and the state of your answers when manually filling it out. You need to copy the entire JSON string of the `questions` field obtained from packet capturing (including the square brackets `[]`) and paste it into the `QUESTIONS_TEMPLATE_JSON` variable in the script. Please ensure the entire string is enclosed in triple quotes `"""..."""` or single/double quotes `''...''` or `""...""`.
*   The script will read this template and then randomly modify the `selfChoice` (single/multiple choice) or `fillText` (rating scale) fields within it to generate random answers.
*   Do not break the JSON structure.

## Disclaimer

This project is for technical exchange and learning purposes only. Please abide by relevant laws, regulations, and website service agreements, and do not use this script for any illegal or immoral purposes. All consequences arising from the use of this script are borne by the user, and the author assumes no responsibility.
