import json
import logging

from gpt import retrieve_batch_results


def write_tasks_to_json(tasks, output_file):
    """
    Write a list of tasks to a JSONL file.
    Args:
        tasks: list of task dictionaries
        output_file: path to output file
    """
    try:
        logging.info("Writing tasks to JSONL file")
        with open(output_file, 'w') as file:
            for obj in tasks:
                file.write(json.dumps(obj) + '\n')
    except Exception as e:
        logging.error(f"Error writing tasks to JSONL file: {e}")


def writing_batch_results(model, result):
    """
    Write the batch results to a file.
    Args:
        model: the model used for the batch job
        result: the result to write
    """
    try:
        logging.info("Writing batch results")
        result_file_name = f"batch_outputs_Gpt/{model}_batch_results.jsonl"

        with open(result_file_name, 'wb') as file:
            file.write(result)

        return result_file_name
    except Exception as e:
        logging.error(f"Error writing batch results: {e}")
        return None
    


def reading_retrieved_results(model, batch_job):
    """
    Read the retrieved results from a batch job.
    Args:
        model: the model used for the batch job
        batch_job: the batch job to read results from
    """
    try:
        results = retrieve_batch_results(model, batch_job)
        if results is None:
            logging.info("No results to read")
            return None
        
        for res in results[:5]:
            task_id = res['custom_id']
            index = task_id.split('-')[-1] # Getting index from task id
            result = res['response']['body']['choices'][0]['message']['content']
            logging.info(f"\n\nRESULT CONTENT for {index}: {result}")
            logging.info("\n\n----------------------------\n\n")
    except Exception as e:
        print(f"Error reading retrieved results: {e}")  
