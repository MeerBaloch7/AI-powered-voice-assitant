import pytest

from NLPM import NaturalLanguageProcessingModule
from conversation_context import ConversationContext


@pytest.fixture
def nlpm():
    return NaturalLanguageProcessingModule()


@pytest.fixture
def context():
    return ConversationContext()


@pytest.fixture
def context_with_timer():
    ctx = ConversationContext()
    ctx.add_turn("set timer for 5 minutes", "set_timer", True, {"duration": 300})
    return ctx
