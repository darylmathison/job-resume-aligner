import openai
import os
import argparse
import sys
from dogpile.cache.region import make_region
import datetime
import os.path


def create_region():
    cache_dir = os.path.join(os.environ.get("HOME"), ".resume_cache")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    return make_region().configure(
        "dogpile.cache.dbm",
        arguments={"filename": os.path.join(cache_dir, "cachefile.dbm")},
        expiration_time=datetime.timedelta(days=1),
    )


region = create_region()

openai.api_key = os.getenv("OPENAI_API_KEY")

# prompt (assuming md_resume and job_description have been defined)
prompt = """
I have a resume formatted in Markdown and a job description. \
Please adapt my resume to better align with the job requirements while \
maintaining a professional tone. Tailor my skills, experiences, and \
achievements to highlight the most relevant points for the position. \
Ensure that my resume still reflects my unique qualifications and strengths \
but emphasizes the skills and experiences that match the job description.

### Here is my resume in Markdown:
{md_resume}

### Here is the job description:
{job_description}

Please modify the resume to:
- Use keywords and phrases from the job description.
- Adjust the bullet points under each role to emphasize relevant skills and achievements.
- Make sure my experiences are presented in a way that matches the required qualifications.
- Maintain clarity, conciseness, and professionalism throughout.

Return the updated resume in Markdown format.

"""


@region.cache_on_arguments()
def modify_resume(md_resume, job_description):
    query = prompt.format(md_resume=md_resume, job_description=job_description)
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": query},
        ],
        temperature=0.25,
    )
    return response.choices[0].message.content


def extract_resume(response_from_openai):
    resume = []
    in_resume = False
    if "markdown" in response_from_openai:
        for line in response_from_openai.split("\n"):
            if line.startswith("```markdown"):
                in_resume = True
            elif line.startswith("```"):
                in_resume = False
            elif in_resume:
                resume.append(line)
        return "\n".join(resume)
    else:
        return response_from_openai


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--resume", help="Path to the resume file", type=str, required=True
    )
    parser.add_argument(
        "--description",
        help="Path to the job description file",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--company", help="Name of the company", type=str, required=True
    )

    args = parser.parse_args(sys.argv[1:])

    with open(args.resume, "r", encoding="utf-8") as resume_file, open(
        args.description, "r"
    ) as description_file, open(
        f"Daryl_Mathison_{datetime.date.today()}_{args.company}.md",
        "w",
        encoding="utf-8",
    ) as new_md_resume_file:
        md_resume = resume_file.read()
        job_description = description_file.read()

        openai_response = modify_resume(md_resume, job_description)
        modified_resume = extract_resume(openai_response)
        new_md_resume_file.write(modified_resume)


if __name__ == "__main__":
    main()
