from sarc.core.router import Router
from sarc.agents.echo_agent import EchoAgent
from sarc.agents.task_agent import TaskAgent

# Agent'ları oluştur
echo = EchoAgent()
tasker = TaskAgent()

# Router'a kaydet
router = Router([echo, tasker])

# Test mesajları
print(router.route("Hey there!"))
print(router.route("Please summarize this document."))
print(router.route("Do something cool."))
