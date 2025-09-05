from sarc.core.router import Router
from sarc.agents.echo_agent import EchoAgent
from sarc.agents.task_agent import TaskAgent

echo = EchoAgent()
tasker = TaskAgent()

router = Router([echo, tasker])

if __name__ == "__main__":
    print("=== SARC CLI STARTED ===")
    print("Type your message below. Type 'exit' or 'quit' to stop.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Exiting SARC CLI. Bye!")
            break

        response = router.route(user_input)

        if response:
            print(response)
        else:
            print("⚠️ No response from agents.")
