# import httpx
# from app.config import get_settings

# settings = get_settings()

# class OumiAgent:
#     """
#     AI Agent using Oumi framework with Together AI LLM
#     Handles incident analysis and root cause detection
#     """
    
#     def __init__(self):
#         self.api_key = settings.TOGETHER_API_KEY
#         self.model = settings.OUMI_MODEL
#         self.base_url = "https://api.together.xyz/v1"
    
#     async def analyze_incident(self, context: dict) -> dict:
#         """
#         Analyze incident and provide root cause + resolution steps
#         """
#         prompt = self._build_analysis_prompt(context)
        
#         response = await self._call_llm(prompt)
        
#         # Parse LLM response into structured format
#         analysis = self._parse_analysis_response(response)
        
#         return analysis
    
#     def _build_analysis_prompt(self, context: dict) -> str:
#         """Build detailed prompt for incident analysis"""
#         return f"""You are a DevOps expert analyzing a production incident.

# Incident Details:
# - Title: {context.get('title')}
# - Service: {context.get('service')}
# - Error Type: {context.get('error_type')}
# - Description: {context.get('description')}

# Stack Trace:
# {context.get('stack_trace', 'Not available')}

# Metadata:
# {context.get('metadata', {})}

# Please provide:
# 1. Root Cause Analysis (what caused this incident)
# 2. Impact Assessment (severity and affected systems)
# 3. Resolution Steps (actionable steps to fix this)
# 4. Prevention Recommendations (how to prevent this in future)

# Format your response as JSON with keys: root_cause, impact, resolution_steps (array), prevention_steps (array)"""
    
#     async def _call_llm(self, prompt: str) -> str:
#         """Call Together AI API with Oumi model"""
#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 f"{self.base_url}/chat/completions",
#                 headers={
#                     "Authorization": f"Bearer {self.api_key}",
#                     "Content-Type": "application/json"
#                 },
#                 json={
#                     "model": self.model,
#                     "messages": [
#                         {
#                             "role": "system",
#                             "content": "You are an expert DevOps incident response agent. Provide clear, actionable analysis."
#                         },
#                         {
#                             "role": "user",
#                             "content": prompt
#                         }
#                     ],
#                     "temperature": 0.3,
#                     "max_tokens": 1000
#                 },
#                 timeout=30.0
#             )
            
#             result = response.json()
#             return result["choices"][0]["message"]["content"]
    
#     def _parse_analysis_response(self, response: str) -> dict:
#         """Parse LLM response into structured format"""
#         import json
#         import re
        
#         try:
#             # Try to extract JSON from response
#             json_match = re.search(r'\{.*\}', response, re.DOTALL)
#             if json_match:
#                 return json.loads(json_match.group())
#         except:
#             pass
        
#         # Fallback: structured parsing
#         return {
#             "root_cause": response[:500],
#             "impact": "Analysis in progress",
#             "resolution_steps": ["Review logs", "Apply fix", "Monitor"],
#             "prevention_steps": ["Add monitoring", "Improve error handling"]
#         }
    
#     async def suggest_code_fix(self, incident_context: dict, code_snippet: str) -> str:
#         """Suggest code fixes using AI"""
#         prompt = f"""Given this incident:
# {incident_context.get('description')}

# And this code snippet:

import httpx
import json
from typing import Optional, Dict, Any
from app.config import get_settings

settings = get_settings()

class OumiAgent:
    """
    AI Agent using Oumi framework with Together AI LLM
    Handles incident analysis and root cause detection
    """
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        
        if self.provider == "together":
            self.api_key = settings.TOGETHER_API_KEY
            self.base_url = "https://api.together.xyz/v1"
            self.model = "meta-llama/Llama-3.2-70B-Instruct-Turbo"
        else:  # groq
            self.api_key = settings.GROQ_API_KEY
            self.base_url = "https://api.groq.com/openai/v1"
            self.model = "llama-3.1-70b-versatile"
    
    async def analyze_incident(self, context: dict) -> dict:
        """
        Analyze incident and provide root cause + resolution steps
        """
        prompt = self._build_analysis_prompt(context)
        
        try:
            response = await self._call_llm(prompt)
            analysis = self._parse_analysis_response(response)
            return analysis
        except Exception as e:
            print(f"Error in AI analysis: {str(e)}")
            return {
                "root_cause": "Analysis failed - manual investigation required",
                "impact": "Unknown",
                "resolution_steps": ["Review logs manually", "Contact on-call engineer"],
                "prevention_steps": ["Add monitoring"],
                "error": str(e)
            }
    
    def _build_analysis_prompt(self, context: dict) -> str:
        """Build detailed prompt for incident analysis"""
        # Escape any special characters in the input
        title = context.get('title', 'Unknown').replace('"', '\\"')
        service = context.get('service', 'unknown').replace('"', '\\"')
        error_type = context.get('error_type', 'unknown').replace('"', '\\"')
        description = context.get('description', '').replace('"', '\\"')
        stack_trace = context.get('stack_trace', 'Not available')[:1000]  # Limit length
        
        prompt1 = f"""You are a DevOps expert analyzing a production incident.

Incident Details:
- Title: {title}
- Service: {service}
- Error Type: {error_type}
- Description: {description}

Stack Trace:
{stack_trace}

Metadata:
{json.dumps(context.get('metadata', {}), indent=2)}

Please provide a detailed analysis in JSON format with the following structure:
{{
    "root_cause": "Clear explanation of what caused this incident",
    "impact": "Description of severity and affected systems",
    "resolution_steps": ["Step 1", "Step 2", "Step 3"],
    "prevention_steps": ["Prevention measure 1", "Prevention measure 2"],
    "confidence": "high/medium/low"
}}

Be specific and actionable. Focus on technical root causes, not symptoms."""
        
        # In _build_analysis_prompt method, around line 60
        prompt = f"""You are a DevOps expert analyzing a production incident.

        INCIDENT DETAILS:
        - Title: {title}
        - Service: {service}
        - Error Type: {error_type}
        - Description: {description}

        STACK TRACE:
        {stack_trace}

        METADATA:
        {json.dumps(context.get('metadata', {}), indent=2)}  # This stays as 'metadata' since it's the key name in the dict
        """

        return prompt
    
    async def _call_llm(self, prompt: str, max_retries: int = 3) -> str:
        """Call Together AI API with Oumi model and retry logic"""
        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        f"{self.base_url}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {self.api_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": self.model,
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "You are an expert DevOps incident response agent. Provide clear, actionable analysis in valid JSON format only."
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            "temperature": 0.3,
                            "max_tokens": 1500,
                            "top_p": 0.9,
                            "response_format": {"type": "json_object"}  # Force JSON response
                        }
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    if "choices" in result and len(result["choices"]) > 0:
                        return result["choices"][0]["message"]["content"]
                    else:
                        raise ValueError("Invalid LLM response structure")
                        
            except httpx.TimeoutException:
                print(f"Timeout on attempt {attempt + 1}/{max_retries}")
                if attempt == max_retries - 1:
                    raise
            except httpx.HTTPStatusError as e:
                print(f"HTTP error on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt == max_retries - 1:
                    raise
            except Exception as e:
                print(f"Unexpected error on attempt {attempt + 1}/{max_retries}: {e}")
                if attempt == max_retries - 1:
                    raise
        
        raise Exception("Failed to get LLM response after retries")
    
    def _parse_analysis_response(self, response: str) -> dict:
        """Parse LLM response into structured format with validation"""
        try:
            # Try to parse JSON directly
            data = json.loads(response)
            
            # Validate required fields
            required_fields = ["root_cause", "resolution_steps"]
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Ensure resolution_steps is a list
            if not isinstance(data.get("resolution_steps"), list):
                data["resolution_steps"] = [str(data.get("resolution_steps", "Review manually"))]
            
            # Ensure prevention_steps is a list
            if "prevention_steps" not in data or not isinstance(data["prevention_steps"], list):
                data["prevention_steps"] = ["Add monitoring", "Improve error handling"]
            
            # Add confidence if missing
            if "confidence" not in data:
                data["confidence"] = "medium"
            
            # Add impact if missing
            if "impact" not in data:
                data["impact"] = "Service degradation detected"
            
            return data
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            print(f"Response was: {response[:500]}")
            
            # Fallback: try to extract useful information
            return self._extract_fallback_analysis(response)
    
    def _extract_fallback_analysis(self, response: str) -> dict:
        """Extract analysis from non-JSON response"""
        import re
        
        # Try to find JSON object in the response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except:
                pass
        
        # Ultimate fallback
        return {
            "root_cause": response[:500] if response else "Analysis incomplete",
            "impact": "Requires manual investigation",
            "resolution_steps": [
                "Review application logs",
                "Check service dependencies",
                "Verify configuration changes",
                "Monitor system metrics"
            ],
            "prevention_steps": [
                "Add automated monitoring",
                "Implement better error handling",
                "Add alerting thresholds"
            ],
            "confidence": "low",
            "raw_response": response[:1000]
        }
    
    async def suggest_code_fix(
        self, 
        incident_context: Dict[str, Any], 
        code_snippet: Optional[str] = None,
        file_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Suggest code fixes using AI
        
        Args:
            incident_context: Details about the incident
            code_snippet: The problematic code (if available)
            file_path: Path to the file (for context)
            
        Returns:
            Dict with suggested fix, explanation, and diff
        """
        if not code_snippet:
            return {
                "success": False,
                "error": "No code snippet provided",
                "suggestion": "Please provide code snippet for analysis"
            }
        
        # Build comprehensive prompt
        prompt = self._build_code_fix_prompt(
            incident_context, 
            code_snippet, 
            file_path
        )
        
        try:
            response = await self._call_llm(prompt)
            fix_data = json.loads(response)
            
            return {
                "success": True,
                "suggested_fix": fix_data.get("fixed_code", ""),
                "explanation": fix_data.get("explanation", ""),
                "changes": fix_data.get("changes", []),
                "confidence": fix_data.get("confidence", "medium"),
                "testing_notes": fix_data.get("testing_notes", [])
            }
            
        except Exception as e:
            print(f"Error generating code fix: {e}")
            return {
                "success": False,
                "error": str(e),
                "suggestion": "Manual code review required"
            }
    
    def _build_code_fix_prompt(
        self, 
        incident_context: Dict[str, Any],
        code_snippet: str,
        file_path: Optional[str]
    ) -> str:
        """Build detailed prompt for code fix suggestion"""
        
        # Sanitize inputs
        description = incident_context.get('description', 'Unknown error')[:500]
        error_type = incident_context.get('error_type', 'unknown')
        stack_trace = incident_context.get('stack_trace', '')[:1000]
        
        prompt = f"""You are a senior software engineer reviewing code that caused a production incident.

    **Incident Information:**
    - Error Type: {error_type}
    - Description: {description}
    - File: {file_path or 'Unknown'}

    **Stack Trace:**
    {stack_trace}

    **Problematic Code:**
    ```python
    {code_snippet}
    ```

    Please provide:
    1. Fixed version of the code
    2. Explanation of what was wrong
    3. List of specific changes made
    4. Testing recommendations

    Respond in JSON format:
    {{
        "fixed_code": "complete fixed code here",
        "explanation": "detailed explanation of the root cause",
        "changes": ["change1", "change2"],
        "confidence": "high/medium/low",
        "testing_notes": ["test1", "test2"]
    }}"""
        
        return prompt
        
    async def check_similar_incidents(
        self, 
        error_pattern: str, 
        knowledge_base: list
    ) -> Optional[Dict[str, Any]]:
        """
        Check if similar incident exists in knowledge base
        Uses AI to find semantic similarity
        
        Args:
            error_pattern: Current error description
            knowledge_base: List of past incidents
            
        Returns:
            Most similar incident if found, None otherwise
        """
        if not knowledge_base:
            return None
        
        # Create embeddings and find similarity
        from app.services.embedding_service import EmbeddingService
        
        embedding_service = EmbeddingService()
        similar = await embedding_service.find_similar_incidents(
            error_pattern, 
            knowledge_base, 
            top_k=1
        )
        
        if similar and len(similar) > 0:
            # Use AI to verify if it's actually similar enough
            verification_prompt = f"""Compare these two incidents and determine if they are similar enough to reuse the solution.

Incident 1 (Current):
{error_pattern}

Incident 2 (Past):
{similar[0].get('error_pattern', '')}

Past Solution:
{similar[0].get('solution', '')}

Respond in JSON:
{{
    "is_similar": true/false,
    "confidence": "high/medium/low",
    "reasoning": "Why they are or are not similar",
    "applicable": true/false
}}"""
            
            try:
                response = await self._call_llm(verification_prompt)
                verification = json.loads(response)
                
                if verification.get("is_similar") and verification.get("applicable"):
                    return {
                        "similar_incident": similar[0],
                        "confidence": verification.get("confidence"),
                        "reasoning": verification.get("reasoning")
                    }
            except Exception as e:
                print(f"Error in similarity verification: {e}")
        
        return None

    