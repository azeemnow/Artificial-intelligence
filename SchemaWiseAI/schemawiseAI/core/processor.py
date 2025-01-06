import re
from .registry import SchemaRegistry

class MiddlewareProcessor:
   def __init__(self, registry: SchemaRegistry):
       self.registry = registry
   
   def process_query(self, llm_query: str) -> str:
       modified = llm_query
       for rule in self.registry.rules.values():
           pattern = fr'\b{rule.source_pattern}\b'
           modified = re.sub(pattern, rule.target_pattern, modified)
       return modified