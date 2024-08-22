from langchain_core.callbacks import FileCallbackHandler, BaseCallbackHandler
from typing import Any, Dict, Optional
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.utils.input import print_text

class LogsCallbackHandler(FileCallbackHandler):
    """Callback Handler that returns logs."""

    def __init__(
        self, color: Optional[str] = None
    ) -> None:
        """Initialize callback handler."""
        self.color = color
        self.log = ""

    def __del__(self) -> None:
        """Destructor to cleanup when done."""
        

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> Any:
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])
        log_entry = f"\033[1m> Entering new {class_name} chain...\033[0m\n"
        self.log += log_entry

    def on_text(self, text: str, color: Optional[str] = None, end: str = "", **kwargs: Any) -> Any:
        log_entry = f"Text: ---{text}---\n"
        self.log += f"{text}\n"

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        log_entry = "\033[1m> Finished chain.\033[0m\n"
        self.log += log_entry

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action."""
        log_entry = print_text(action.log, color=color or self.color)
        self.log += log_entry

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        if observation_prefix is not None:
            log_entry = print_text(f"\n{observation_prefix}")

            self.log += log_entry
        log_entry = print_text(output, color=color or self.color)
        self.log += log_entry
        if llm_prefix is not None:
            log_entry = print_text(f"\n{llm_prefix}")

            self.log += log_entry

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        log_entry = print_text(finish.log, color=color or self.color, end="\n")
        self.log += log_entry


# it works with any type of model
# pass this callback in config arg of chain.invoke()
class TokenCounter(BaseCallbackHandler):
    """Callback Handler that returns total tokens."""

    def __init__(self, llm):
        self.llm = llm
        self.input_tokens = 0
        self.output_tokens = 0
        self.total_tokens = 0

    def on_llm_start(self, serialized, prompts, **kwargs):
        for p in prompts:
            self.input_tokens += self.llm.get_num_tokens(p)
        self.total_tokens += self.input_tokens

    def on_llm_end(self, response, **kwargs):
        results = response.flatten()
        for r in results:
            self.output_tokens = self.llm.get_num_tokens(r.generations[0][0].text)
        self.total_tokens += self.output_tokens