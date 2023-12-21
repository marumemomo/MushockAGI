import re

def invoke_llm(llm, task):
    response = llm.invoke(
        f"""
        You are a Professional Python programmer.
        Please change the following code with the following description.
        The changed code should be output using code blocks.
        Be sure to output all code for final export to a file.
        If the code is empty, generate the code.

        Description:
        {task['description']}

        Code:
        {task['code']}
        """)
    # Extracting code block from response
    matches = re.findall(r'```.*\n\s*([\s\S]*?)\n```', response, re.MULTILINE)
    if len(matches) > 0:
        return matches[0]
    else:
        print("No code block found in the response.")
        return response
