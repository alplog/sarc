from sarc.core.router import Router
from sarc.agents.echo_agent import EchoAgent
from sarc.protocol.message import IntentType

# Ajanı oluştur
echo = EchoAgent()

# Router'a ajanları ver
router = Router([echo])

# Test mesajları
print(router.route("Hey, what's up?"))
print(router.route("Blorp zzz 9000"))
