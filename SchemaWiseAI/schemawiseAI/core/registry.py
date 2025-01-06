from typing import Dict, Any, Optional
import json
import yaml
import re
from dataclasses import dataclass

@dataclass
class SchemaRule:
   source_pattern: str
   target_pattern: str
   data_type: str
   validation_rules: Optional[Dict[str, Any]] = None

class SchemaRegistry:
   def __init__(self):
       self.rules: Dict[str, SchemaRule] = {}
   
   def load_json_schema(self, schema_file: str):
       with open(schema_file, 'r') as f:
           self._extract_rules(json.load(f))
           
   def load_yaml_schema(self, schema_file: str):
       with open(schema_file, 'r') as f:
           self._extract_rules(yaml.safe_load(f))
   
   def _extract_rules(self, schema: Dict):
       for entity, definition in schema.items():
           for field, props in definition.get('fields', {}).items():
               self.rules[f"{entity}.{field}"] = SchemaRule(
                   source_pattern=field,
                   target_pattern=props.get('map_to', field),
                   data_type=props.get('type', 'string'),
                   validation_rules=props.get('validation', {})
               )
