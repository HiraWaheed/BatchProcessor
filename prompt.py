def build_gpt_prompt(storyname):
    system_prompt = """ You are a helpful story-teller and writer. Your task is to write a creative story based on the storyname given. """
    user_prompt = f""" 
                
    ***Task

    Write an interesting and creative short story based on the story name provided in ***Story Name section.

    ***Story Name
    {storyname}

    ***Instructions

    Step 1: Carefully read the story name in ***Story Name section and write a creative short story based on the story name.
    Step 2: Use a human-like and writer's tone to write a story from the story name.
    Step 3: Provide a ***complete and concise story, of 2 paragraphs with 5 lines in each paragraph.
    Step 4: Use the formatting guidelines provided in the Output Example section below and return answer in JSON object for the summary.
    Step 5: Do not include any portion of the prompt or instructions in your response to avoid penalties.

    ## Output Example:
    # Story Name
    [WRITE STORY NAME HERE]
    # Story 
    ```
    [WRITE STORY HERE]
    ```
    *** Response:
    """
    return system_prompt, user_prompt
