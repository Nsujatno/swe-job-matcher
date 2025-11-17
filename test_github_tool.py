from app.agents.tools import get_first_10_github_jobs, scrape_job_posting
# jobs = get_first_10_github_jobs.invoke({})
# print(jobs)

job1 = "https://jobs.ea.com/en_US/careers/JobDetail/Systems-Software-Engineer-Co-op/210903?utm_source=Simplify&ref=Simplify"
job2 = "https://philips.wd3.myworkdayjobs.com/jobs-and-careers/job/Bothell/Intern---Ultrasound-Imaging-Acoustics---Bothell--WA---Summer-2026_567433?utm_source=Simplify&ref=Simplify"

job = scrape_job_posting.invoke(job1)
print(job)