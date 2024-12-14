from fastapi import APIRouter, HTTPException
from fast_api.langgraph_api.agent import runnable
import logging
from fast_api.langgraph_api.utilities import build_report


router = APIRouter()

@router.get("/get-langraph-response/")
def get_response(input_query: str, index_name: str):
    try:
        # Generate the file stream and metadata
        input = input_query
        chat_history = []
        
        print(f"Calling {index_name}")        
        out = runnable.invoke({
                 "input": input,
                "chat_history": chat_history,
                "index_name": index_name,
        })

        if "research_steps" in out["intermediate_steps"][-1].tool_input:
            return build_report(
            output=out["intermediate_steps"][-1].tool_input
        )
        else:
            return out['intermediate_steps'][-1].log
    
    except Exception as e:
        logging.error("Exception:", e)
        raise HTTPException(status_code=500, detail=f"Error fetching response from Langgraph: {str(e)}")