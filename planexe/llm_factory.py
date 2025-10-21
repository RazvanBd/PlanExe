"""
Create a LLM instances.

PROMPT> python -m planexe.llm_factory
"""
import logging
from dataclasses import dataclass
from planexe.utils.planexe_dotenv import PlanExeDotEnv
from planexe.utils.planexe_config import PlanExeConfig, PlanExeConfigError
from planexe.utils.planexe_llmconfig import PlanExeLLMConfig
from typing import Optional, Any
from llama_index.core.llms.llm import LLM
from llama_index.llms.gemini import Gemini

# This is a special case. It will cycle through the available LLM models, if the first one fails, try the next one.
SPECIAL_AUTO_ID = 'auto'
SPECIAL_AUTO_LABEL = 'Auto'

logger = logging.getLogger(__name__)

__all__ = ["get_llm", "LLMInfo", "get_llm_names_by_priority", "SPECIAL_AUTO_ID", "is_valid_llm_name"]

planexe_llmconfig = PlanExeLLMConfig.load()

@dataclass
class LLMConfigItem:
    id: str
    label: str

@dataclass
class LLMInfo:
    llm_config_items: list[LLMConfigItem]
    error_message_list: list[str]

    @classmethod
    def obtain_info(cls) -> 'LLMInfo':
        """
        Returns a list of available LLM names.
        """

        error_message_list = []

        # Prepare the list of available LLM config items.
        llm_config_items = []

        # This is a special case. It will cycle through the available LLM models, if the first one fails, try the next one.
        llm_config_items.append(LLMConfigItem(id=SPECIAL_AUTO_ID, label=SPECIAL_AUTO_LABEL))

        # The rest are the LLM models specified in the llm_config.json file.
        for config_id, config in planexe_llmconfig.llm_config_dict.items():
            priority = config.get("priority", None)
            if priority:
                label_with_priority = f"{config_id} (prio: {priority})"
            else:
                label_with_priority = config_id

            item = LLMConfigItem(id=config_id, label=label_with_priority)
            llm_config_items.append(item)

        return LLMInfo(
            llm_config_items=llm_config_items, 
            error_message_list=error_message_list,
        )

def get_llm_names_by_priority() -> list[str]:
    """
    Returns a list of LLM names sorted by priority.
    Lowest values comes first.
    Highest values comes last.
    """
    configs = [(name, config) for name, config in planexe_llmconfig.llm_config_dict.items() if config.get("priority") is not None]
    configs.sort(key=lambda x: x[1].get("priority", 0))
    return [name for name, _ in configs]

def is_valid_llm_name(llm_name: str) -> bool:
    """
    Returns True if the LLM name is valid, False otherwise.
    """
    return llm_name in planexe_llmconfig.llm_config_dict

def get_llm(llm_name: Optional[str] = None, **kwargs: Any) -> LLM:
    """
    Returns an LLM instance based on the config.json file or a fallback default.

    :param llm_name: The name/key of the LLM to instantiate.
                     If None, falls back to DEFAULT_LLM in .env (or 'gemini-paid-flash-2.0').
    :param kwargs: Additional keyword arguments to override default model parameters.
    :return: An instance of a LlamaIndex LLM class.
    """
    if not llm_name:
        planexe_dotenv = PlanExeDotEnv.load()
        llm_name = planexe_dotenv.get("DEFAULT_LLM", "gemini-paid-flash-2.0")

    if llm_name == SPECIAL_AUTO_ID:
        logger.error(f"The special {SPECIAL_AUTO_ID!r} is not a LLM model that can be created. Please use a valid LLM name.")
        raise ValueError(f"The special {SPECIAL_AUTO_ID!r} is not a LLM model that can be created. Please use a valid LLM name.")

    if not is_valid_llm_name(llm_name):
        logger.error(f"Cannot create LLM, the llm_name {llm_name!r} is not found in llm_config.json.")
        raise ValueError(f"Cannot create LLM, the llm_name {llm_name!r} is not found in llm_config.json.")

    config = planexe_llmconfig.llm_config_dict[llm_name]
    class_name = config.get("class")
    arguments = config.get("arguments", {})

    # Override with any kwargs passed to get_llm()
    arguments.update(kwargs)

    # Dynamically instantiate the class
    try:
        llm_class = globals()[class_name]  # Get class from global scope
        return llm_class(**arguments)
    except KeyError:
        raise ValueError(f"Invalid LLM class name in config.json: {class_name}")
    except TypeError as e:
        raise ValueError(f"Error instantiating {class_name} with arguments: {e}")

if __name__ == '__main__':
    llm_names = get_llm_names_by_priority()
    print("LLM names by priority:")
    for llm_name in llm_names:
        print(f"- {llm_name}")
    print("\n\nTesting the LLMs:")
    try:
        llm = get_llm(llm_name="gemini-paid-flash-2.0")
        print(f"Successfully loaded LLM: {llm.__class__.__name__}")
        print(llm.complete("Hello, how are you?"))
    except ValueError as e:
        print(f"Error: {e}")
