import os
import json
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import requests
from openai import OpenAI

# Initialize Rich console for better output
console = Console()

class BraveAIAgent:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize API keys
        self.brave_api_key = os.getenv('BRAVE_API_KEY')
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.brave_api_key:
            raise ValueError("Brave API key not found in environment variables")
        
        # Initialize OpenAI client if API key is available
        self.openai_client = OpenAI(api_key=self.openai_api_key) if self.openai_api_key else None
        
        # Set up console
        self.console = Console()

    def web_search(self, query: str, count: int = 10) -> Dict[str, Any]:
        """
        Perform a web search using Brave Search API
        """
        headers = {
            'X-Subscription-Token': self.brave_api_key,
            'Accept': 'application/json',
        }
        
        params = {
            'q': query,
            'count': count
        }
        
        response = requests.get(
            'https://api.search.brave.com/res/v1/web/search',
            headers=headers,
            params=params
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Search failed with status code: {response.status_code}")

    def process_query(self, query: str) -> str:
        """
        Process the user query using OpenAI if available
        """
        if not self.openai_client:
            return query
            
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that improves search queries."},
                    {"role": "user", "content": f"Improve this search query for better results: {query}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            console.print(f"[yellow]Warning: Could not process query with OpenAI. Using original query.[/yellow]")
            return query

    def display_results(self, results: Dict[str, Any]) -> None:
        """
        Display search results in a formatted way
        """
        if 'web' not in results:
            console.print("[red]No results found[/red]")
            return

        for result in results['web']['results']:
            console.print(Panel(
                Markdown(f"# {result['title']}\n\n{result['description']}\n\n[Link]({result['url']})"),
                border_style="blue"
            ))
            console.print()

    def run(self):
        """
        Main loop for the agent
        """
        console.print("[bold blue]Brave AI Search Agent[/bold blue]")
        console.print("Type 'exit' to quit\n")

        while True:
            query = console.input("[bold green]Enter your search query:[/bold green] ")
            
            if query.lower() == 'exit':
                break
                
            try:
                # Process query if OpenAI is available
                processed_query = self.process_query(query)
                if processed_query != query:
                    console.print(f"[cyan]Improved query:[/cyan] {processed_query}\n")
                
                # Perform search
                results = self.web_search(processed_query)
                self.display_results(results)
                
            except Exception as e:
                console.print(f"[red]Error:[/red] {str(e)}")

if __name__ == "__main__":
    try:
        agent = BraveAIAgent()
        agent.run()
    except Exception as e:
        console.print(f"[red]Fatal error:[/red] {str(e)}")