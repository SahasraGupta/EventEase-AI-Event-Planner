
# Connect with the LLM
from rag_pipeline.llm import get_llm
from agent.tools import search_and_scrap, retrieve_documents
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from backend.schemas.event_schema import EventRecommendations



tools = [search_and_scrap, retrieve_documents]

base_llm = get_llm()
llm = base_llm.bind_tools(tools)

# Structured output LLM
structured_llm = get_llm().with_structured_output(EventRecommendations)

tools_by_name = {
    tool.name: tool
    for tool in tools
}



def generate_structured_response(answer):

    return structured_llm.invoke([
        SystemMessage(
            content="""
            Convert the event-planning information into the
            required EventRecommendations structure.

            VENUE STRUCTURING RULES:

            1. Return each venue as a separate Venue object.
            2. Include the exact venue name.
            3. Include its image URL only if available.
            4. Include its rating only if verified.
            5. Include its address or locality if available.
            6. Include its actual capacity if available.
            7. Include only verified facilities.
            8. Include pricing only when supported by the source.
            9. Include the direct source URL for each venue.
            10. Never combine information from different venues.
            11. Never invent missing information.
            12. If a venue has no supporting source URL,
                do not include that venue.
            13. If a detail is unavailable, leave it null
                or use an empty list for facilities.

            Preserve the original event overview, food,
            decoration, additional recommendations and budget.

            Do not invent or alter any information.
            """
        ),
        HumanMessage(content=str(answer))
    ])


def run_agent(user_query: str):

    messages = [
        SystemMessage(
            content="""
            You are an AI Event Planner.

            Help users create practical, detailed and realistic event plans.

            TOOL USAGE GUIDELINES:
            1. Use retrieve_documents for existing event-planning knowledge.
            2. Use search_and_scrap for current information from the web.
            3. Use each tool only when relevant.
            4. Avoid calling the same tool repeatedly.
            5. Collect sufficient information before generating recommendations.

            RECOMMENDATION GUIDELINES:
            1. Recommend specific venue names and function halls whenever available.
            2. Include venue locations and pricing whenever available.
            3. Never invent venue names, addresses, contact details or prices.
            4. Clearly mention when exact information is unavailable.
            5. Provide practical food and catering recommendations.
            6. Suggest realistic decoration and additional event arrangements.
            7. Provide a category-wise estimated budget breakdown.
            8. Ensure the estimated total does not exceed the user's stated budget.
            9. Distinguish estimated costs from verified prices.
            10. Mention source URLs when available.

            VENUE RECOMMENDATION RULES:
            1. Recommend only individually named event venues.
            2. Use search_and_scrap for current web information.
            3. Do not treat directories, category pages or articles as individual venues.
            4. Do not use retrieve_documents as proof of current availability, pricing or capacity.
            5. Include only details supported by retrieved content.
            6. Never assume venue capacity, facilities, location or rental prices.
            7. If a detail is missing, do not invent it.
            8. Never combine details from different venues.
            9. Include a direct source URL for every venue.
            10. Return fewer than five venues if fewer than five are verified.

            SOURCE VERIFICATION RULES:
            1. Every venue must have a source URL that directly supports that venue.
            2. Verify that the venue name appears in the source content.
            3. Extract details from that same venue's information.
            4. Never combine information from different webpages.
            5. If the source does not support a venue name, do not recommend it.
            6. Extract actual capacity when available.
            7. Never confuse seating capacity with floating capacity.
            8. Preserve the exact locality mentioned by the source.
            9. Do not invent image URLs or ratings.
            10. Do not use a general directory URL as an individual venue's
                direct source unless it specifically supports that venue.

            Return clear and detailed event-planning information.
            """
        ),
        HumanMessage(content=user_query)
    ]

    used_tools = set()

    for iteration in range(10):

        print(f"\nAgent Iteration: {iteration + 1}")

        response = llm.invoke(messages)

        messages.append(response)

        if not response.tool_calls:

            final_answer = response.content

            print("\nGenerating structured recommendations...")

            structured_response = generate_structured_response(
                final_answer
            )

            return structured_response

        repeated_tool_requested = False

        for tool_call in response.tool_calls:

            tool_name = tool_call["name"]

            if tool_name in used_tools:

                repeated_tool_requested = True

                messages.append(
                    ToolMessage(
                        content=(
                            "This tool was already executed. "
                            "Use the information already available "
                            "and generate your final answer."
                        ),
                        tool_call_id=tool_call["id"]
                    )
                )

                continue

            used_tools.add(tool_name)

            print("Selected Tool:", tool_name)

            selected_tool = tools_by_name[tool_name]

            tool_result = selected_tool.invoke(tool_call)

            print("Tool Executed Successfully!")

            messages.append(tool_result)

        if repeated_tool_requested:
            print("Repeated tool request detected.")
            print("Generating final answer without additional tool calls...")
            structured_response = generate_structured_response(messages)
            return structured_response

            return structured_response

    raise RuntimeError(
        "Agent could not generate a final response within 10 iterations."
    )
