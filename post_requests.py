import requests

for i in range(1, 3):
    request_example = {'question_num': i}
    result = requests.post('http://0.0.0.0:5000/api/questions', json=request_example)
    print(result.text)
