from app.agents.tools import create_job_agent

agent = create_job_agent()

# Test the complete workflow
query = """
I need help finding internships that match my background. 
Please analyze the top jobs and explain which ones are the best fit for me.
My resume_id is 79e8ee7d-bcfe-4ce7-9526-d62de005b66e
The job posting I am looking at is this url: https://alsacstjude.wd1.myworkdayjobs.com/careersalsacstjude/job/Memphis-TN/Summer-2026-Intern---AI-Software-Engineer--Memphis--TN-_R0010291?utm_source=Simplify&ref=Simplify
"""

print("=== Job Recommendation Agent ===\n")

for event in agent.stream({"messages": [("user", query)]}, stream_mode="values"):
    if "messages" in event:
        last_msg = event["messages"][-1]
        
        # Show tool calls
        if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
            for tool_call in last_msg.tool_calls:
                print(f"🔧 Using tool: {tool_call['name']}")
        
        # Show responses
        elif hasattr(last_msg, 'content') and last_msg.content:
            print(f"\n{last_msg.content}\n")
