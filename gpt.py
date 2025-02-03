
import json
import logging
import os
from prompt import build_gpt_prompt
from openai import OpenAI
from dotenv import load_dotenv

from utils import writing_batch_results
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


def check_batch_status(id):
    """
    Checks the status of a batch job.
    Args:
        id: the ID of the batch job to check
    """
    logging.info("Checking batch status")
    batch_job = client.batches.retrieve(id)
    print(f"Status for {batch_job} is {batch_job.status}")
    return batch_job.status


def retrieve_batch_results(model, batch_job):
    """
    Retrieves the results of a batch job.
    Args:
        model: the model used for the batch job
        batch_job: the batch job to retrieve results from
    """
    try:
        logging.info("Retrieving batch results")
        if batch_job.output_file_id is None:
            logging.error("Batch job has no output file")
            return None
        
        result_file_id = batch_job.output_file_id
        result = client.files.content(result_file_id).content
        result_file_name = writing_batch_results(model, result)
        # Loading data from saved file
        results = []
        with open(result_file_name, 'r') as file:
            for line in file:
                # Parsing the JSON string into a dict and appending to the list of results
                json_object = json.loads(line.strip())
                results.append(json_object)

        return results
    except Exception as e:
        print(f"Error retrieving batch results: {e}")
        return None



def fetch_batch_details():
    """
    Fetches details of the most recent batch job.
    """
    return client.batches.list(limit=1)


def read_file_contents(file_id):
    """
    Reads the contents of a file.
    Args:
        file_id: the ID of the file to read    
    """
    file_response = client.files.content(file_id)
    print(file_response.text)



