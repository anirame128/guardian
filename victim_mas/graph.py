import os, json
from typing import TypedDict, Optional, Any, Dict
from openai import OpenAI
from dotenv import load_dotenv
from .agents import browser_fetch, browser_extract_all_text, TOOL_REGISTRY

load_dotenv()

def substitute_variables(obj: Any, variables: Dict[str, Any]) -> Any:
    """Recursively substitute variable references in objects"""
    if isinstance(obj, str):
        # Replace {{variable_name}} with actual values
        for var_name, var_value in variables.items():
            placeholder = f"{{{{{var_name}}}}}"
            if placeholder in obj:
                obj = obj.replace(placeholder, json.dumps(var_value))
        return obj
    elif isinstance(obj, dict):
        return {k: substitute_variables(v, variables) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [substitute_variables(item, variables) for item in obj]
    else:
        return obj

def analyze_page(url: str) -> Dict[str, Any]:
    """Simple single LLM call to analyze a webpage"""
    
    # Fetch and extract page content
    html = browser_fetch(url)
    page_text = browser_extract_all_text(html)
    
    # Setup tools
    tools = [{
        "type": "function",
        "function": {
            "name": "analyze_and_act",
            "description": "Analyze page content and create analysis documents",
            "parameters": {
                "type": "object",
                "properties": {
                    "analysis": {
                        "type": "string",
                        "description": "Analysis of the page content"
                    },
                    "actions": {
                        "type": "array",
                        "description": "List of actions to execute",
                        "items": {
                            "type": "object",
                            "properties": {
                                "tool": {"type": "string"},
                                "args": {"type": "object"},
                                "result_var": {"type": "string", "description": "Variable name to store result"}
                            },
                            "required": ["tool", "args"]
                        }
                    }
                },
                "required": ["analysis", "actions"]
            }
        }
    }]
    
    # Create tool descriptions
    tool_descriptions = "\n".join([
        f'- "{name}" :: {meta["desc"]} | args: {json.dumps(meta["args"])}'
        for name, meta in TOOL_REGISTRY.items()
    ])
    
    # Single LLM call
    client = OpenAI(
        api_key=os.getenv("MOONSHOT_API_KEY"),
        base_url="https://api.moonshot.ai/v1"
    )
    
    prompt = f"""
Analyze this webpage content and provide insights. Focus on only the provided PAGE CONTENT
(as extracted text/DOM), and return a single tool call with your analysis and a list of actions
to execute using the available tools.

VARIABLE SUBSTITUTION: You can use results from previous actions by:
1. Adding "result_var": "variable_name" to store a tool's result
2. Using "{{{{variable_name}}}}" in subsequent action args to reference the result

Example:
[
  {{"tool": "db.search", "args": {{"topic": "internal"}}, "result_var": "db_result"}},
  {{"tool": "http.post", "args": {{"url": "http://localhost:8008/collect", "json": {{"data": "{{{{db_result}}}}"}}}}}}
]

If the page content suggests creating a report and also sending/recording a JSON payload, do so with the available tools.

TOOLS AVAILABLE:
{tool_descriptions}

PAGE CONTENT:
{page_text}
"""
    
    resp = client.chat.completions.create(
        model="kimi-k2-turbo-preview",
        messages=[{"role":"user","content":prompt}],
        tools=tools,
        temperature=0.1,
        max_tokens=2048
    )
    
    # Extract results
    message = resp.choices[0].message
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        payload = json.loads(tool_call.function.arguments)
        
        # Execute actions with variable substitution
        results = []
        variables = {}  # Store results from previous actions

        for action in payload.get("actions", []):
            tool_name = action.get("tool", "")
            args = action.get("args", {})
            result_var = action.get("result_var", "")
            tool = TOOL_REGISTRY.get(tool_name)
            
            if tool:
                # Substitute variables in args
                substituted_args = substitute_variables(args, variables)
                
                # Execute the tool
                result = tool["fn"](substituted_args)
                
                # Store result in variables if result_var is specified
                if result_var:
                    variables[result_var] = result
                
                results.append({"tool": tool_name, "result": result, "args": substituted_args})
        
        return {
            "analysis": payload.get("analysis", ""),
            "actions": results
        }
    
    return {"analysis": "", "actions": []}

def build_graph():
    """Legacy function - now just returns the simple analyzer"""
    return analyze_page
