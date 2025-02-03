import json


def write_tasks_to_json(tasks, output_file):
    """
    Write a list of tasks to a JSONL file.
    Args:
        tasks: list of task dictionaries
        output_file: path to output file
    """
    with open(output_file, 'w') as file:
        for obj in tasks:
            file.write(json.dumps(obj) + '\n')
