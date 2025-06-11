from celery import chain
from app.modules import get_runner, get_available_modules

def create_workflow(normalized_input: dict, selected_modules: list) -> chain:
    """Build Celery workflow with validation"""
    tasks = []
    available = get_available_modules(normalized_input["type"])
    
    for module in selected_modules:
        if module not in available:
            raise ValueError(f"Module {module} not available for {normalized_input['type']}")
        
        runner = get_runner(module)
        tasks.append(runner.s(normalized_input["target"]))
    
    return chain(*tasks) if len(tasks) > 1 else tasks[0]  # Single task optimization