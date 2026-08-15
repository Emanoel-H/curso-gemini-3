from langchain_google_genai import ChatGoogleGenerativeAI
from my_models import GEMINI_FLASH
from my_keys import GEMINI_API_KEY
from langchain import hub
from langchain.agents import create_react_agent, Tool
from image_analysis_tool import ImageAnalysisTool
from explaining_tool import ExplainingTool

class OrchestratorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            api_key= GEMINI_API_KEY,
            model= GEMINI_FLASH
        )

        image_analysis_tool = ImageAnalysisTool()
        explaining_tool = ExplainingTool()

        self.tools = [
            Tool(
                name= image_analysis_tool.name,
                func = image_analysis_tool.run,
                description= image_analysis_tool.description,
                return_direct = image_analysis_tool.return_direct
            ),
            Tool(
                name=explaining_tool.name,
                func=explaining_tool.run,
                description=explaining_tool.description,
                return_direct=explaining_tool.return_direct
            )
        ]

        prompt = hub.pull("hwchase17/react")
        self.agent = create_react_agent(self.llm, self.tools, prompt)