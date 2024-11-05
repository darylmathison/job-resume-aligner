# Job Resume Aligner

It's well known that customizing a resume for a job is good idea.  However, customizing for each job description can take up a lot of time.  This utility aims to help with some of that by harnessing the power of AI.

**Note**: This only creates a first draft of the resume.  In my own experience using it, generative AI has added skills I don't have to the resume.  At the end of the day, a human has to submit the resume and is ultimately responsible.

## Inspiration
[5 AI Projects You Can Build This Weekend (with Python)](https://towardsdatascience.com/5-ai-projects-you-can-build-this-weekend-with-python-c57724e9c461)

## Requirements

* Python 3.12
* An OpenAI account with an API key.  Instructions are at https://platform.openai.com/docs/quickstart

**Usage**:
```
python resume_modifier.py
usage: resume_modifier.py [-h] --resume RESUME --description DESCRIPTION --company COMPANY
resume_modifier.py: error: the following arguments are required: --resume, --description, --company
```
## Arguments
All arguments are required.
### resume
This is the filepath to a markdown version of a resume.

### description
This is the filepath to a text file of the job description.

### company
This is name of the company so the new version can have a unique filename.

## Expected output
The expected output is a markdown file that has the filename of `Daryl_Mathison_{today's date}_{company name}.md`

## Improvements in the Future

* A way to turn the output into something more well known like PDF or docx.  I currently upload the file into Google Docs and edit it from there.
* A better way to strip out what ChatGPT adds to the top and bottom.  The code that does that now is rough at best.