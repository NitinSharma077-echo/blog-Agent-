from agents import get_rag_agent,get_research_agent,get_report_agent


def run_research_pipeline(topic:str):
    """Run the Research Pipeline"""
    state={}
    search_agent=get_rag_agent()
    report_agent=get_report_agent()

    search_agent.invoke({
        "message":[("user",f"Research this topic: {topic}")]
    })

    state['web_content'] = search_agent.invoke({
        "message":[("user",f"Research this topic: {topic}")]
    })['messages'][-1].content

    report_content=report_agent.invoke({
        "message":[("user",f"Write a report on this topic: {topic}")]
    })['messages'][-1].content

    state['final_report']=report_content
    reader_result=reader_agent.invoke({
        "message":[("user",f"Summarize this report: {report_content}")]
    })['messages'][-1].content
    state['final_report']=reader_result

    research_combined=(
        f"Search result: {state['web_content']}"
        f"\n\nReport result: {state['final_report']}"

    )
    state['final_report']=writer_chain.invoke({
        "topic":topic,
        "research":research_combined
    })['messages'][-1].content

    return state


if __name__ == "__main__":
    topic = input("Enter the topic you want to research: ")
    result = run_research_pipeline(topic)
    print("\n" + "="*50)
    print(f"Research Report for: {topic}")
    print("="*50 + "\n")
    print(result['final_report'])