import json
from datetime import datetime
import uuid

def transform(input_json: dict) -> dict:
    timestamp = datetime.now().isoformat()
    submission_id = str(uuid.uuid4())

    questions = []
    for q in range(1, 6):
        question_key = f'question_{q}'
        question_text = input_json[question_key]
        answers = []
        correct_answer_key = f'correct_answer{q}'
        correct_answer = input_json[correct_answer_key]
        for a in range(1, 5):
            answer_key = f'question_{q}_answer_{a}'
            answer_text = input_json[answer_key]
            answers.append(answer_text)

        question = {
            'student_name': input_json['student_name'],
            'timestamp': timestamp,
            # assemble question in the output format
            'question': question_text,
            'uuid': submission_id,
            'answers': answers,
            'correct answer': correct_answer
            
        }
        questions.append(question)      
    return questions


if __name__ == '__main__':
    with open(r'data\test_submission.json') as f:
       input_json = json.load(f)
    output_json = transform(input_json)
    with open(r'data\transformed_submission.json', 'w') as f:
        json.dump(output_json, f, indent=4)