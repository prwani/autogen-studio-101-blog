import requests
import json
import os
import time
import logging
from typing import Dict, Any, Optional, Union, List
from urllib.parse import urljoin
import backoff  # You may need to install this package: pip install backoff

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("autogen-client")

class AutoGenClient:
    """
    Client for interacting with AutoGen Studio API.
    """
    def __init__(
        self, 
        base_url: str = "http://127.0.0.1:8084",
        api_key: Optional[str] = None,
        timeout: int = 30
    ):
        """
        Initialize the AutoGen client.
        
        Args:
            base_url: The base URL of the AutoGen Studio API server
            api_key: Optional API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.timeout = timeout
        
    def _get_headers(self) -> Dict[str, str]:
        """
        Get the headers for API requests.
        
        Returns:
            A dictionary of HTTP headers
        """
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        """
        Make an HTTP request to the API.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (relative to base_url)
            params: URL parameters for GET requests
            
        Returns:
            Response object
        """
        url = urljoin(self.base_url, endpoint)
        headers = self._get_headers()
        
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            timeout=self.timeout
        )
        
        # Raise an exception for 4XX and 5XX status codes
        response.raise_for_status()
        
        return response
    
    def call_predict_api(
        self,
        task: str,
        input_data: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Call the /predict/{task} REST API endpoint.
        
        Args:
            task: The prediction task identifier
            input_data: The input data for the prediction
            
        Returns:
            The prediction result as a dictionary
        """
        endpoint = f"/predict/{task}"
        input_data = input_data or {}
        
        try:
            response = self._make_request("GET", endpoint, params=input_data)
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


# Example usage
if __name__ == "__main__":
    # Create the client
    client = AutoGenClient(base_url="http://127.0.0.1:8084")
    
    # Try a prediction task
    print("\nTrying a prediction task...")
    predict_result = client.call_predict_api(
        task="Write a function to find the sum of all even numbers in a list.",
        input_data={}
    )
    print(json.dumps(predict_result, indent=2))