import logging
from gpt import check_batch_status, fetch_batch_details, read_file_contents
from utils import reading_retrieved_results
from constants import model

if __name__ == "__main__":
    
    batch_job = fetch_batch_details() #fetch latest batch job details
    status = check_batch_status(batch_job.id)
    
    if status == 'completed':
        if batch_job.data[0].output_file_id is not None:
            reading_retrieved_results(model, batch_job.data[0])
        elif batch_job.data[0].error_file_id is not None:
            logging.error("Batch job has error file")
            read_file_contents(batch_job.data[0].error_file_id)
    
    elif status == 'failed':
        logging.error("Batch job has failed")
        read_file_contents(batch_job.data[0].error_file_id)
    
    elif status == 'inprogress':
        logging.info("Batch job is in progress")

    else:
        logging.info(f"Batch job is in queue with status {status}")