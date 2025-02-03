import logging
import os
import pandas as pd
from constants import model
from gpt import check_batch_status, create_batch_job, create_task, fetch_batch_details, read_file_contents, upload_batch_file
from utils import reading_retrieved_results, write_tasks_to_json

def main(model, inputs_reading_dir, outputs_writing_dir):
    """
    Driver function to create tasks, write them to a JSONL file, upload the file, and create a batch job.
    """
    try:
        all_tasks = []
        current_index = 0

        os.makedirs(outputs_writing_dir, exist_ok=True)

        output_process_json = os.path.join(outputs_writing_dir, f"{model}_summary.jsonl")
        for file_name in os.listdir(inputs_reading_dir):
            if file_name.endswith(".csv"):
                input_process_csv = os.path.join(inputs_reading_dir, file_name)

                try:
                    df = pd.read_csv(input_process_csv)
                    file_tasks = create_task(model, df, start_index=current_index)
                    all_tasks.extend(file_tasks)
                    current_index += len(df)
                except Exception as e:
                    print(f"Error processing {file_name}: {str(e)}")


        write_tasks_to_json(all_tasks, output_process_json)
        batch_file = upload_batch_file(output_process_json)
        batch_job = create_batch_job(batch_file)

        return batch_job
    except Exception as e:
        print(f"Error in main: {str(e)}")
        return None
    

if __name__ == "__main__":
    inputs_reading_dir = "inputs/"
    outputs_writing_dir = "outputs/"
    os.makedirs(inputs_reading_dir, exist_ok=True)
    os.makedirs(outputs_writing_dir, exist_ok=True)
    batch_job = None
    
    batch_job = main(model, inputs_reading_dir, outputs_writing_dir)

    status = check_batch_status(batch_job.id)
    
    
    if status == 'completed':
        batch_job = fetch_batch_details()
        if batch_job.data[0].output_file_id is not None:
            reading_retrieved_results(model, batch_job.data[0])
        elif batch_job.data[0].error_file_id is not None:
            logging.error("Batch job has error file")
            read_file_contents(batch_job.data[0].error_file_id)