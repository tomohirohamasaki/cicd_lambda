import os
import json
from chalice import Chalice
from my_package.math import newton_sqrt
from my_package.repository import save_result, retrieve_result_for

app = Chalice(app_name='sqrt-app')
BATCH_SIZE = 5
input_queue_name = os.getenv('INPUT_QUEUE_NAME')


@app.on_sqs_message(queue=input_queue_name, batch_size=BATCH_SIZE)
def sqrt(event):
    for record in event:
        record_body = json.loads(record.body)
        number = record_body['number']
        result_from_db = retrieve_result_for(number)
        if result_from_db:
            print(f'Result found in DB: sqrt({number})={result_from_db}')
        else:
            result = newton_sqrt(number)
            save_result(number, result)
            print(f'Result saved to DB: sqrt({number})={result}')
