from app.agents.tools import get_first_10_github_jobs
jobs = get_first_10_github_jobs.invoke({})
print(jobs)