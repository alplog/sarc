from sarc.core.router import Router
from sarc.agents.echo_agent import EchoAgent
from sarc.agents.task_agent import TaskAgent
from sarc.protocol.message import SAOResponse

def format_response(response: SAOResponse) -> str:
    """Converts SAOResponse to user-friendly format"""
    if response.success:
        result = f"✅ {response.data}"
        if response.processing_time:
            result += f" (⏱️ {response.processing_time:.3f}s)"
        return result
    else:
        error_msg = f"❌ {response.error_message}"
        if response.agent_id:
            error_msg += f" [Agent: {response.agent_id}]"
        if response.error_type:
            error_msg += f" [Type: {response.error_type.value}]"
        return error_msg

echo = EchoAgent()
tasker = TaskAgent()

# Create router with threshold
router = Router([echo, tasker], score_threshold=0)

if __name__ == "__main__":
    print("=== SARC CLI STARTED (with Error Handling) ===")
    print("Type your message below. Type 'exit' or 'quit' to stop.")
    print("Try: 'hello', 'create a report', '', 'invalid command'\n")

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Exiting SARC CLI. Bye!")
                break

            response = router.route(user_input)
            
            # Format and print SAOResponse
            formatted_response = format_response(response)
            print(formatted_response)
            
            # Debug information (optional)
            if not response.success:
                print(f"🔍 Debug: Agent={response.agent_id}, ErrorType={response.error_type}")
                
        except KeyboardInterrupt:
            print("\n\nExiting SARC CLI. Bye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {str(e)}")
