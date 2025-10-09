from langchain_openai import ChatOpenAI
from typing import List
from utils.config import getConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import yaml

class LLMConfig:
    config = getConfig()
    API_KEY = config.get_api_key()
    BASE_URL = config.get_base_url()

    def __init__(self, model: str = "meta-llama/llama-4-maverick:free"):
        self.llm = ChatOpenAI(api_key=self.API_KEY,
                                base_url=self.BASE_URL,
                                temperature=0.5,
                                model=model)

    def get_system_prompt(self, agent_type: str) -> str:
        try:
            with open("./llm/prompts.yaml", "r") as f:
                data = yaml.safe_load(f)
                system_prompt = data["prompts"].get(agent_type, data["prompts"]["base"])
            return system_prompt
        except Exception as e:
            print(f"Error getting system prompt for {agent_type}: {e} ")
            
    def summarise_image(self, image: List) -> List[str]:
        try:
            system_prompt = self.get_system_prompt("imageagent")
            messages = [
                (
                    "system", system_prompt
                ),
                (   "human",
                    [
                        {"type": "text", "text": "Describe and summarise the text contents in the image below."},
                        {"type": "image_url", "image_url": {"url": "data:image/png;base64,{input}"}}
                    ]
                )
            ]
            prompt = ChatPromptTemplate.from_messages(messages)
            chain = prompt | self.llm | StrOutputParser()
            response = chain.invoke({"input":image})
            return response
        except Exception as e:
            print(f"Error in summarise_image: {e}")
            return []
    
    def summarise_function(self, input: List) -> List[str]:
        try:
            system_prompt = self.get_system_prompt("tableagent")
            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{input}")
            ])
                        
            chain = prompt | self.llm | StrOutputParser()
            response = chain.invoke({"input":input})
            return response
        except Exception as e:
            print(f"Error in summarise_function: {e}")
            return []

if __name__ == "__main__":
    llm_config = LLMConfig()
