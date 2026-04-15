from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

def run_research_pipeline(topic:str) -> dict:
    
    state = {}
    
    # Search Agent Working
    print("\n"+"="*50)
    print("Step 1 - Search Agent Is Working ...")
    print("="*50)
    
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages" : [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    
    state["search_results"] = search_result['messages'][-1].content 
    
    print("\n Search Result ",state['search_results'])
    
    # Step 2 Reader Agent
    print("\n"+"="*50)
    print("Step 2 - Reader Agent is Scraping Top Resources ...")
    print("="*50)
    
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages" : [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    
    state['scraped_content'] = reader_result['messages'][-1].content
    
    print("\nScraped Content\n", state['scraped_content'])
    
    # Step 3 Writer Agent
    print("\n"+"="*50)
    print("Step 3 - Writer is drafting the report...")
    print("="*50)
    
    research_combined = (
        f"Search Results : \n {state['search_results']}\n\n"
        f"Detailed Scraped Content : \n {state['scraped_content']}"
    )
    
    state['report'] = writer_chain.invoke(
        {
            "topic" : topic,
            "research" : research_combined
        }
    )
    
    print("\n Final Report \n",state['report'])
    
    # Critic Report
    
    print("\n"+"="*50)
    print("Step 4 - Critics are reviewing the report...")
    print("="*50)
    
    
    state["feedback"] = critic_chain.invoke(
        {
            "report":state['report']
        }
    )
    
    print("\n Critic Report\n", state['feedback'])
    
    return state

if __name__ == "__main__" :
    topic = input("\n Enter research topic :")
    run_research_pipeline(topic)