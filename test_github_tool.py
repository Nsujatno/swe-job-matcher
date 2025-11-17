from app.agents.tools import get_first_10_github_jobs, scrape_job_posting
# jobs = get_first_10_github_jobs.invoke({})
# print(jobs)

job = scrape_job_posting.invoke("https://jobs.ea.com/en_US/careers/JobDetail/Systems-Software-Engineer-Co-op/210903?utm_source=Simplify&ref=Simplify")
print(job)