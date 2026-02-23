"""
🧬 MOLECULAR AI SERVER 💀

Runs the background_agent.py as an API service with agent tools.
This is the ACTUAL 31-component molecular AI, not just a prompt.

Features:
- Full cognitive architecture (Brain, Memory, all 31 components)
- File editing tools (read, write, replace, search)
- Code execution tools (run commands, analyze errors)
- Chat interface
- Agent mode (autonomous task execution)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
from pathlib import Path
import json
import subprocess
import traceback

# Already in Theory folder - add parent to path for imports
theory_path = Path(__file__).parent  # We're IN Theory folder now
sys.path.insert(0, str(theory_path))

from background_agent import MolecularAgent

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Global agent instance
molecular_agent = None
workspace_path = Path.cwd().parent  # Default to parent directory (not Theory folder itself)

# Tool implementations (like what I have access to)
class AgentTools:
    """Tools the molecular AI can use to interact with files and execute code."""
    
    @staticmethod
    def read_file(file_path: str, start_line: int = 1, end_line: int = None):
        """Read file contents."""
        try:
            full_path = workspace_path / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if end_line is None:
                end_line = len(lines)
            
            content = ''.join(lines[start_line-1:end_line])
            return {
                'success': True,
                'content': content,
                'lines': f"{start_line}-{end_line}",
                'total_lines': len(lines)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def write_file(file_path: str, content: str):
        """Write content to file."""
        try:
            full_path = workspace_path / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                'success': True,
                'message': f'File written: {file_path}',
                'bytes': len(content)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def replace_in_file(file_path: str, old_string: str, new_string: str):
        """Replace string in file."""
        try:
            full_path = workspace_path / file_path
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if old_string not in content:
                return {
                    'success': False,
                    'error': 'Old string not found in file'
                }
            
            new_content = content.replace(old_string, new_string, 1)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            return {
                'success': True,
                'message': f'Replaced in {file_path}',
                'changes': len(new_string) - len(old_string)
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def list_files(directory: str = "."):
        """List files in directory."""
        try:
            full_path = workspace_path / directory
            items = []
            
            for item in full_path.iterdir():
                items.append({
                    'name': item.name,
                    'type': 'directory' if item.is_dir() else 'file',
                    'size': item.stat().st_size if item.is_file() else None
                })
            
            return {'success': True, 'items': items}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def search_files(query: str, file_pattern: str = "**/*.py"):
        """Search for text in files."""
        try:
            results = []
            for file_path in workspace_path.glob(file_pattern):
                if file_path.is_file():
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query.lower() in content.lower():
                                # Find line numbers
                                lines = content.split('\n')
                                matches = []
                                for i, line in enumerate(lines, 1):
                                    if query.lower() in line.lower():
                                        matches.append({
                                            'line': i,
                                            'content': line.strip()
                                        })
                                
                                results.append({
                                    'file': str(file_path.relative_to(workspace_path)),
                                    'matches': matches
                                })
                    except:
                        continue
            
            return {'success': True, 'results': results, 'count': len(results)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def run_command(command: str, timeout: int = 30):
        """Execute shell command."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=workspace_path
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'exit_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {'success': False, 'error': f'Command timed out after {timeout}s'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    @staticmethod
    def get_errors(file_path: str = None):
        """Get syntax/lint errors (simulated - would use real linters)."""
        # Placeholder - would integrate with pylint, mypy, etc.
        return {
            'success': True,
            'errors': [],
            'message': 'Error checking not yet implemented'
        }


def execute_tool(tool_name: str, params: dict):
    """Execute a tool with given parameters."""
    tools = AgentTools()
    
    if not hasattr(tools, tool_name):
        return {'success': False, 'error': f'Unknown tool: {tool_name}'}
    
    tool_func = getattr(tools, tool_name)
    return tool_func(**params)


def make_json_serializable(obj, seen=None):
    """Convert non-serializable objects to JSON-safe format."""
    from types import MappingProxyType
    
    if seen is None:
        seen = set()
    
    # Handle basic JSON types
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    
    # Prevent infinite recursion on circular references
    obj_id = id(obj)
    if obj_id in seen:
        return f"<circular reference to {type(obj).__name__}>"
    seen.add(obj_id)
    
    try:
        if isinstance(obj, dict):
            return {k: make_json_serializable(v, seen) for k, v in obj.items()}
        elif isinstance(obj, MappingProxyType):
            return {k: make_json_serializable(v, seen) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [make_json_serializable(item, seen) for item in obj]
        elif hasattr(obj, '__class__') and hasattr(obj.__class__, '__name__'):
            # For enums and other special types
            if obj.__class__.__name__ in ['ViolationSeverity', 'OutputType']:
                return str(obj) if hasattr(obj, 'value') else obj.__class__.__name__
        
        # Try to convert objects with __dict__
        if hasattr(obj, '__dict__'):
            return make_json_serializable(obj.__dict__, seen)
        
        # Fallback: convert to string
        return str(obj)
    finally:
        seen.discard(obj_id)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'molecular_ratio': molecular_agent.brain.state.molecular_ratio() if molecular_agent else 0,
        'decisions': molecular_agent.brain.state.total_decisions if molecular_agent else 0
    })


@app.route('/chat', methods=['POST'])
def chat():
    """
    Chat endpoint - send message, get response.
    
    Now uses knowledge retrieval + molecular predictions!
    
    Body:
    {
        "message": "user message",
        "use_tools": true/false
    }
    """
    try:
        data = request.json
        message = data.get('message', '')
        use_tools = data.get('use_tools', False)
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Process through molecular chat pipeline (includes retrieval + prediction)
        result = molecular_agent.process_chat(message)
        
        # Extract the reply
        reply = result.get('response', 'No response generated')
        
        # Add retrieval info if sources found
        if result.get('retrieved_sources'):
            sources = result['retrieved_sources']
            if len(sources) <= 3:
                reply += f"\n\n💡 Retrieved from: {', '.join(sources)}"
        
        # Make result JSON-serializable before returning
        safe_result = make_json_serializable(result.get('full_result', result))
        
        # Return in format expected by Simple Web UI
        return jsonify({
            'reply': reply, 
            'full_result': safe_result,
            'molecular': result.get('molecular', False),
            'confidence': result.get('confidence', 0)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/execute_tool', methods=['POST'])
def execute_tool_endpoint():
    """
    Direct tool execution endpoint.
    
    Body:
    {
        "tool": "read_file",
        "params": {"file_path": "test.py"}
    }
    """
    try:
        data = request.json
        tool_name = data.get('tool')
        params = data.get('params', {})
        
        result = execute_tool(tool_name, params)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/agent_mode', methods=['POST'])
def agent_mode():
    """
    Agent mode - autonomous task execution.
    
    Body:
    {
        "task": "Create a Python script that...",
        "max_iterations": 10
    }
    """
    try:
        data = request.json
        task = data.get('task', '')
        max_iterations = data.get('max_iterations', 10)
        
        if not task:
            return jsonify({'error': 'No task provided'}), 400
        
        # Agent loop
        iterations = []
        current_task = task
        
        for i in range(max_iterations):
            # Process through molecular agent
            result = molecular_agent.process_prompt(current_task)
            
            iteration_data = {
                'iteration': i + 1,
                'thought': result.get('response', ''),
                'tools_used': []
            }
            
            # Check if agent wants to use tools
            if result.get('needs_tool_execution'):
                tool_calls = result.get('tool_calls', [])
                
                for tool_call in tool_calls:
                    tool_name = tool_call.get('tool')
                    params = tool_call.get('params', {})
                    tool_result = execute_tool(tool_name, params)
                    
                    iteration_data['tools_used'].append({
                        'tool': tool_name,
                        'params': params,
                        'result': tool_result
                    })
            
            iterations.append(iteration_data)
            
            # Check if task complete
            if result.get('task_complete', False):
                break
            
            # Update task based on results
            current_task = result.get('next_action', '')
            if not current_task:
                break
        
        return jsonify({
            'success': True,
            'iterations': iterations,
            'total_iterations': len(iterations)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500


@app.route('/stats', methods=['GET'])
def stats():
    """Get molecular AI statistics."""
    try:
        memory_data = molecular_agent.memory.data
        
        return jsonify({
            'molecular_ratio': molecular_agent.brain.state.molecular_ratio(),
            'total_decisions': molecular_agent.brain.state.total_decisions,
            'memory_items': len(memory_data.get('memory', [])),
            'wisdom_items': len(molecular_agent.wisdom.wisdom_items),
            'mistakes': len(molecular_agent.mistakes.mistakes),
            'habits': len(molecular_agent.habits.habits),
            'active_goals': len(molecular_agent.goals.get_active_goals())
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/set_workspace', methods=['POST'])
def set_workspace():
    """Set workspace directory."""
    global workspace_path
    
    try:
        data = request.json
        new_path = data.get('path', '')
        
        if not new_path:
            return jsonify({'error': 'No path provided'}), 400
        
        new_path = Path(new_path).resolve()
        
        if not new_path.exists():
            return jsonify({'error': 'Path does not exist'}), 400
        
        workspace_path = new_path
        
        return jsonify({
            'success': True,
            'workspace': str(workspace_path)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================================
# OPENAI-COMPATIBLE ENDPOINTS (for Open WebUI integration)
# ============================================================================

@app.route('/v1/models', methods=['GET'])
def list_models():
    """List available models (OpenAI-compatible endpoint)."""
    return jsonify({
        'object': 'list',
        'data': [
            {
                'id': 'molecular-ai-31',
                'object': 'model',
                'created': 1709337600,
                'owned_by': 'molecular-ai',
                'permission': [],
                'root': 'molecular-ai-31',
                'parent': None,
            }
        ]
    })


@app.route('/v1/chat/completions', methods=['POST'])
def openai_chat_completions():
    """OpenAI-compatible chat completions endpoint."""
    try:
        data = request.json
        messages = data.get('messages', [])
        stream = data.get('stream', False)
        
        # Extract the last user message
        user_message = ''
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                user_message = msg.get('content', '')
                break
        
        if not user_message:
            return jsonify({'error': 'No user message found'}), 400
        
        # Use molecular AI to generate response
        global molecular_agent
        if molecular_agent is None:
            return jsonify({'error': 'Molecular AI not initialized'}), 500
        
        # Decide whether to use tools (default to yes for Open WebUI)
        use_tools = data.get('use_tools', True)
        
        # Process with molecular AI
        if use_tools:
            # Check if this looks like a task request
            task_keywords = ['create', 'make', 'write', 'edit', 'search', 'find', 'list', 'run', 'execute', 'agent']
            is_task = any(keyword in user_message.lower() for keyword in task_keywords)
            
            if is_task:
                # Use agent mode for tasks
                result = molecular_agent.autonomous_mode(user_message, max_iterations=5)
                reply = result.get('final_response', 'Task completed.')
            else:
                # Regular chat with tools available
                reply = molecular_agent.think(user_message)
        else:
            # Chat without tools
            reply = molecular_agent.think(user_message)
        
        # Format response in OpenAI format
        if stream:
            # For now, return non-streaming (full support would require SSE)
            return jsonify({
                'id': f'chatcmpl-molecular-{molecular_agent.total_decisions}',
                'object': 'chat.completion',
                'created': 1709337600,
                'model': 'molecular-ai-31',
                'choices': [
                    {
                        'index': 0,
                        'message': {
                            'role': 'assistant',
                            'content': reply
                        },
                        'finish_reason': 'stop'
                    }
                ],
                'usage': {
                    'prompt_tokens': len(user_message.split()),
                    'completion_tokens': len(reply.split()),
                    'total_tokens': len(user_message.split()) + len(reply.split())
                }
            })
        else:
            # Non-streaming response
            return jsonify({
                'id': f'chatcmpl-molecular-{molecular_agent.total_decisions}',
                'object': 'chat.completion',
                'created': 1709337600,
                'model': 'molecular-ai-31',
                'choices': [
                    {
                        'index': 0,
                        'message': {
                            'role': 'assistant',
                            'content': reply
                        },
                        'finish_reason': 'stop'
                    }
                ],
                'usage': {
                    'prompt_tokens': len(user_message.split()),
                    'completion_tokens': len(reply.split()),
                    'total_tokens': len(user_message.split()) + len(reply.split())
                }
            })
    
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error in OpenAI chat completions: {e}")
        print(error_trace)
        return jsonify({
            'error': str(e),
            'traceback': error_trace
        }), 500


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Start the Molecular AI server."""
    global molecular_agent
    
    print("🧬" + "="*78 + "💀")
    print("   MOLECULAR AI SERVER")
    print("   Full 31-component cognitive architecture with agent tools")
    print("💀" + "="*78 + "🧬")
    print()
    
    # Initialize molecular agent
    print("Initializing Molecular AI...")
    molecular_agent = MolecularAgent()
    print("✓ Ready!")
    print()
    
    # Show workspace
    print(f"📂 Workspace: {workspace_path}")
    print()
    
    # Available tools
    print("🛠️ Available Tools:")
    print("   - read_file, write_file, replace_in_file")
    print("   - list_files, search_files")
    print("   - run_command, get_errors")
    print()
    
    # Endpoints
    print("🌐 API Endpoints:")
    print("   POST /chat - Chat with molecular AI")
    print("   POST /agent_mode - Autonomous task execution")
    print("   POST /execute_tool - Direct tool execution")
    print("   GET /stats - Get system statistics")
    print("   GET /health - Health check")
    print("   🔥 POST /v1/chat/completions - OpenAI-compatible (for Open WebUI)")
    print("   🔥 GET /v1/models - List models (OpenAI-compatible)")
    print()
    
    # Start server
    port = 5000
    print(f"🚀 Starting server on http://localhost:{port}")
    print("💀 Press Ctrl+C to stop")
    print()
    
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    main()
