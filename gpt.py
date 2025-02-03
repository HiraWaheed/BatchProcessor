
import logging
import os
from prompt import build_gpt_prompt
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)



def create_task(model, df, start_index=0):
    """
    Process a CSV file and return list of tasks.
    Args:
        df: pandas DataFrame containing task data
        start_index: starting index for task IDs to ensure uniqueness across files
    Returns:
        list of task dictionaries
    """
    logging.info("Creating tasks")
    tasks = []
    
    for index, row in df.iterrows():
        story = row['story']

        system_prompt, user_prompt = build_gpt_prompt(story)
        
        task = {
            "custom_id": f"task-{start_index + index}",
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": {
                "model": model, #model like gpt-4o, gpt-4o-turbo
                "temperature": 0.1,
                "response_format": {  #include this to get the response in JSON format
                    "type": "json_object"
                },
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
            }
        }
        
        tasks.append(task)
    
    return tasks



def upload_batch_file(file_name):
    """
    Uploads a batch file to the OpenAI API.
    Args:
        file_name: name of the file to upload
    """
    logging.info("Uploading batch file")
    batch_file = client.files.create(
    file=open(file_name, "rb"),
    purpose="batch"
    )
    return batch_file


def create_batch_job(batch_file):
    """
    Creates a batch job using the uploaded batch file.
    Args:
        batch_file: the uploaded batch file
    """
    logging.info("Creating batch job")
    batch_job = client.batches.create(
        input_file_id=batch_file.id,
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    return batch_job

