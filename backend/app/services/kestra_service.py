import httpx
from typing import Dict, Any
from app.config import get_settings

settings = get_settings()

class KestraService:
    """
    Service to interact with Kestra for workflow orchestration
    Handles incident resolution workflows
    """
    
    def __init__(self):
        self.base_url = settings.KESTRA_URL
        self.api_key = settings.KESTRA_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def trigger_workflow(self, workflow_id: str, inputs: Dict[str, Any]) -> Dict:
        """
        Trigger a Kestra workflow for incident resolution
        
        Args:
            workflow_id: The workflow to execute (e.g., 'incident-resolution')
            inputs: Input parameters for the workflow
        
        Returns:
            Execution result with status and outputs
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/v1/executions/{workflow_id}",
                    headers=self.headers,
                    json={"inputs": inputs},
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    execution_data = response.json()
                    
                    # Poll for execution completion
                    execution_id = execution_data.get("id")
                    result = await self._wait_for_execution(execution_id)
                    
                    return result
                else:
                    return {
                        "success": False,
                        "error": f"Failed to trigger workflow: {response.text}"
                    }
                    
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
    
    async def _wait_for_execution(self, execution_id: str, max_wait: int = 300) -> Dict:
        """Poll Kestra for execution completion"""
        import asyncio
        
        async with httpx.AsyncClient() as client:
            for _ in range(max_wait // 5):  # Poll every 5 seconds
                response = await client.get(
                    f"{self.base_url}/api/v1/executions/{execution_id}",
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    execution = response.json()
                    state = execution.get("state", {}).get("current")
                    
                    if state == "SUCCESS":
                        return {
                            "success": True,
                            "execution_id": execution_id,
                            "outputs": execution.get("outputs", {}),
                            "duration": execution.get("state", {}).get("duration")
                        }
                    elif state in ["FAILED", "KILLED"]:
                        return {
                            "success": False,
                            "execution_id": execution_id,
                            "error": execution.get("state", {}).get("histories", [])
                        }
                
                await asyncio.sleep(5)
        
        return {
            "success": False,
            "error": "Execution timeout"
        }
    
    async def create_workflow(self, workflow_definition: Dict) -> Dict:
        """Create a new workflow in Kestra"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/flows",
                headers=self.headers,
                json=workflow_definition
            )
            
            return response.json()
    
    async def list_executions(self, workflow_id: str, limit: int = 10) -> list:
        """Get recent executions of a workflow"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/api/v1/executions",
                headers=self.headers,
                params={
                    "flowId": workflow_id,
                    "size": limit
                }
            )
            
            if response.status_code == 200:
                return response.json().get("results", [])
            return []
