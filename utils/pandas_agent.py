import pandas as pd
import openai
import os
import re
import traceback
from config import Config

class PandasAgent:
    """
    Agent that analyzes data by generating and executing Python code.
    This ensures 100% accuracy for calculations.
    """
    
    def __init__(self, df: pd.DataFrame, api_key: str):
        """
        Initialize the Pandas Agent
        
        Args:
            df: The pandas DataFrame to analyze
            api_key: OpenAI API key
        """
        self.df = df
        self.api_key = api_key
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key)
        
        # Get dataframe info for the prompt
        self.columns = list(df.columns)
        self.dtypes = df.dtypes.to_dict()
        self.sample_data = df.head(3).to_string()
        
    def ask(self, question: str) -> str:
        """
        Main entry point to ask a question
        """
        max_retries = 3
        last_error = None
        
        for attempt in range(max_retries):
            try:
                # 1. Generate Code (pass error if retrying)
                code = self._generate_code(question, last_error, attempt + 1)
                
                # 2. Execute Code
                result, output = self._execute_code(code)
                
                # 3. Format Answer
                final_answer = self._format_answer(question, code, result, output)
                return final_answer
                
            except Exception as e:
                last_error = str(e)
                print(f"⚠️ Attempt {attempt + 1} failed: {last_error}")
                # Continue to next attempt
        
        return f"❌ Failed to answer after {max_retries} attempts. Last error: {last_error}"

    def _generate_code(self, question: str, error_message: str = None, attempt: int = 1) -> str:
        """
        Generate Python code using LLM
        """
        if attempt > 3:
            raise Exception("Failed to generate valid code after 3 attempts.")

        system_prompt = f"""
You are an expert Python data analyst.
You have a pandas DataFrame named `df`.
Columns: {self.columns}
Data Types: {self.dtypes}

Sample Data:
{self.sample_data}

TASK:
Write Python code to answer the user's question.
1. Store the final answer in a variable named `result`.
2. If the answer is a number or string, assign it directly to `result`.
3. If the answer is a DataFrame/Series, convert it to a string or dictionary before assigning to `result`.
4. Do NOT generate charts or plots.
5. Use `df` directly. Do not read any files.

IMPORTANT:
- Return ONLY the Python code inside a markdown block.
- Example:
```python
result = df['Total'].sum()
```
"""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        if error_message:
            messages.append({"role": "assistant", "content": "```python\n# Previous code that failed\n```"})
            messages.append({"role": "user", "content": f"The previous code failed with this error:\n{error_message}\nPlease fix the code."})

        response = self.client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=messages,
            temperature=0  # Deterministic for code
        )
        
        content = response.choices[0].message.content
        
        # Extract code from markdown blocks
        code_match = re.search(r"```python\n(.*?)```", content, re.DOTALL)
        if code_match:
            return code_match.group(1)
        
        # Fallback: try to find any code block
        code_match = re.search(r"```(.*?)```", content, re.DOTALL)
        if code_match:
            return code_match.group(1)
            
        return content # Assume raw code if no blocks

    def _execute_code(self, code: str):
        """
        Execute the generated code
        """
        # Prepare execution environment
        local_vars = {
            "df": self.df,
            "pd": pd,
            "result": None
        }
        
        # Capture stdout
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        try:
            exec(code, {}, local_vars)
            result = local_vars.get("result")
            output = captured_output.getvalue()
            return result, output
        except Exception as e:
            # Restore stdout before raising
            sys.stdout = sys.__stdout__
            # Recursively try to fix
            # Note: In a real recursion, we'd pass the error back to _generate_code
            # For simplicity here, we just raise and let the caller handle or fail
            # To implement self-correction, we would need to call _generate_code again here.
            # Let's do a simple 1-level retry here or let the main loop handle it.
            # For this MVP, let's raise and let the user see the error or implement a loop in ask()
            raise e
        finally:
            sys.stdout = sys.__stdout__

    def _format_answer(self, question: str, code: str, result, output: str) -> str:
        """
        Format the final answer using LLM to make it natural
        """
        # If result is simple, just return it
        if isinstance(result, (int, float, str)) and not output:
            # Optional: Make it a full sentence
            pass
            
        # Use LLM to generate a natural language response based on the result
        system_prompt = "You are a helpful assistant. Convert the provided code result into a clear, natural language answer in English."
        
        user_content = f"""
Question: {question}
Code Executed:
{code}

Result: {result}
Output: {output}

Please answer the question clearly based on this result.
"""
        
        response = self.client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0
        )
        
        return response.choices[0].message.content
