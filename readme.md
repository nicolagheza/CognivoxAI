# COGNIVOX AI

## A Cutting-Edge Telegram Bot Powered by LLaMA 3.1 and LangChain

🚀 Cognivox AI is an innovative, open-source Telegram bot that harnesses the power of LLaMA 3.1, a state-of-the-art language model, to provide users with a conversational AI experience like no other. Built using Python, LangChain, and LangGraph, our bot is designed to be highly scalable, flexible, and customizable.

## Features

💬 Conversational Interface: Engage in natural-sounding conversations with Cognivox AI, powered by LLaMA 3.1's advanced language understanding and generation capabilities.

📚 Knowledge Graph: Our bot leverages LangGraph to construct a vast knowledge graph, providing users with accurate and up-to-date information on a wide range of topics.

🤖 Customizable: With our open-source codebase, developers can easily modify and extend Cognivox AI's functionality to suit their specific needs.

📊 Scalable: Built using LangChain, our bot can handle a high volume of conversations simultaneously, making it perfect for large-scale deployments.

## Requirements

* Python 3.8 or higher
* Check .env.example

## Installation

1. Clone this repository: git clone https://github.com/your-repo/Cognivox-AI.git
2. Install dependencies: pip install -r requirements.txt
3. Configure your environment variables:
 * TELEGRAM_API_KEY: Your Telegram bot token
 * TOGHETER_API_KEY: Your togheter.ai API key
 * LANGCHAIN_API_KEY: Your LangChain API key
 * GROQ_API_KEY: Your Groq API key for Whisper
 * TELEGRAM_CHANNEL_ID: The ID of the Telegram channel where the bot will be deployed (required for bot access)
4. Run the bot: python main.py

**Note:** To obtain the `TELEGRAM_CHANNEL_ID`, follow these steps:

1. Create a new Telegram channel.
2. Add the bot as an administrator to the channel.
3. Go to the channel settings and click on the three dots next to the channel name.
4. Select "Edit" and then click on the " Channel ID" field.
5. Copy the Channel ID and add it to your environment variables.

## Contributing

We welcome contributions from the community! Please submit pull requests or issues to help improve Cognivox AI.

## License

Cognivox AI is released under the [MIT License](https://opensource.org/licenses/MIT).

## Acknowledgments

* Special thanks to Toghter.ai for providing access to the LangChain API.
* Special thanks to Groq for providing access to the GROQ API.

## Community

Join our community to discuss Cognivox AI and stay updated on the latest developments:

* GitHub: [your-repo/Cognivox-AI](https://github.com/your-repo/Cognivox-AI)

We hope you enjoy using Cognivox AI! 🤗
