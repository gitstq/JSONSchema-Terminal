#!/usr/bin/env python3
"""
SchemaPilot - Lightweight JSON Schema Terminal Visualizer & Validator
轻量级JSON Schema终端可视化与验证工具

A zero-dependency CLI tool for visualizing, validating, and analyzing JSON Schema
直接依赖的CLI工具，用于可视化、验证和分析JSON Schema

Author: SchemaPilot Team
License: MIT
Version: 1.0.0
"""

import json
import sys
import os
import re
import argparse
from typing import Any, Dict, List, Optional, Tuple, Union
from pathlib import Path
from datetime import datetime

# ANSI Color Codes for Terminal Output
# 终端输出的ANSI颜色代码
class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'
    
    # Foreground colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright foreground colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


class SchemaValidator:
    """
    JSON Schema Validator supporting Draft 7 features
    支持Draft 7特性的JSON Schema验证器
    """
    
    # JSON Schema Draft 7 type mappings
    # JSON Schema Draft 7 类型映射
    TYPE_VALIDATORS = {
        'null': lambda x: x is None,
        'boolean': lambda x: isinstance(x, bool),
        'object': lambda x: isinstance(x, dict),
        'array': lambda x: isinstance(x, list),
        'number': lambda x: isinstance(x, (int, float)) and not isinstance(x, bool),
        'integer': lambda x: isinstance(x, int) and not isinstance(x, bool),
        'string': lambda x: isinstance(x, str),
    }
    
    # Format validators (basic implementations)
    # 格式验证器（基本实现）
    FORMAT_VALIDATORS = {
        'email': lambda x: re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', x) is not None,
        'uri': lambda x: re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*://', x) is not None,
        'date': lambda x: re.match(r'^\d{4}-\d{2}-\d{2}$', x) is not None,
        'date-time': lambda x: re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', x) is not None,
        'ipv4': lambda x: re.match(r'^(\d{1,3}\.){3}\d{1,3}$', x) is not None,
        'ipv6': lambda x: re.match(r'^[0-9a-fA-F:]+$', x) is not None,
        'uuid': lambda x: re.match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$', x) is not None,
        'hostname': lambda x: re.match(r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$', x) is not None,
    }
    
    def __init__(self):
        self.errors: List[Dict[str, Any]] = []
        self.warnings: List[Dict[str, Any]] = []
    
    def validate(self, instance: Any, schema: Dict[str, Any], path: str = "") -> bool:
        """
        Validate an instance against a schema
        验证实例是否符合schema
        """
        self.errors = []
        self.warnings = []
        self._validate_recursive(instance, schema, path)
        return len(self.errors) == 0
    
    def _validate_recursive(self, instance: Any, schema: Dict[str, Any], path: str):
        """Recursive validation helper"""
        # Handle boolean schemas
        if isinstance(schema, bool):
            if not schema and instance is not None:
                self.errors.append({
                    'path': path,
                    'message': 'Schema is false, any value is invalid',
                    'value': instance
                })
            return
        
        if not isinstance(schema, dict):
            return
        
        # Check type
        if 'type' in schema:
            self._validate_type(instance, schema['type'], path)
        
        # Check enum
        if 'enum' in schema:
            if instance not in schema['enum']:
                self.errors.append({
                    'path': path,
                    'message': f'Value must be one of: {schema["enum"]}',
                    'value': instance
                })
        
        # Check const
        if 'const' in schema:
            if instance != schema['const']:
                self.errors.append({
                    'path': path,
                    'message': f'Value must be: {schema["const"]}',
                    'value': instance
                })
        
        # String validations
        if isinstance(instance, str):
            self._validate_string(instance, schema, path)
        
        # Number validations
        if isinstance(instance, (int, float)) and not isinstance(instance, bool):
            self._validate_number(instance, schema, path)
        
        # Array validations
        if isinstance(instance, list):
            self._validate_array(instance, schema, path)
        
        # Object validations
        if isinstance(instance, dict):
            self._validate_object(instance, schema, path)
        
        # Check format
        if 'format' in schema and isinstance(instance, str):
            self._validate_format(instance, schema['format'], path)
    
    def _validate_type(self, instance: Any, types: Union[str, List[str]], path: str):
        """Validate instance type"""
        if isinstance(types, str):
            types = [types]
        
        valid = any(self.TYPE_VALIDATORS.get(t, lambda x: False)(instance) for t in types)
        if not valid:
            actual_type = self._get_json_type(instance)
            self.errors.append({
                'path': path,
                'message': f'Expected type: {types}, got: {actual_type}',
                'value': instance
            })
    
    def _validate_string(self, instance: str, schema: Dict[str, Any], path: str):
        """Validate string constraints"""
        if 'minLength' in schema and len(instance) < schema['minLength']:
            self.errors.append({
                'path': path,
                'message': f'String length {len(instance)} is less than minimum {schema["minLength"]}',
                'value': instance
            })
        
        if 'maxLength' in schema and len(instance) > schema['maxLength']:
            self.errors.append({
                'path': path,
                'message': f'String length {len(instance)} exceeds maximum {schema["maxLength"]}',
                'value': instance
            })
        
        if 'pattern' in schema:
            if not re.match(schema['pattern'], instance):
                self.errors.append({
                    'path': path,
                    'message': f'String does not match pattern: {schema["pattern"]}',
                    'value': instance
                })
    
    def _validate_number(self, instance: Union[int, float], schema: Dict[str, Any], path: str):
        """Validate number constraints"""
        if 'minimum' in schema and instance < schema['minimum']:
            self.errors.append({
                'path': path,
                'message': f'Value {instance} is less than minimum {schema["minimum"]}',
                'value': instance
            })
        
        if 'maximum' in schema and instance > schema['maximum']:
            self.errors.append({
                'path': path,
                'message': f'Value {instance} exceeds maximum {schema["maximum"]}',
                'value': instance
            })
        
        if 'exclusiveMinimum' in schema and instance <= schema['exclusiveMinimum']:
            self.errors.append({
                'path': path,
                'message': f'Value {instance} must be greater than {schema["exclusiveMinimum"]}',
                'value': instance
            })
        
        if 'exclusiveMaximum' in schema and instance >= schema['exclusiveMaximum']:
            self.errors.append({
                'path': path,
                'message': f'Value {instance} must be less than {schema["exclusiveMaximum"]}',
                'value': instance
            })
        
        if 'multipleOf' in schema:
            if isinstance(instance, float):
                # Handle floating point precision
                quotient = instance / schema['multipleOf']
                if abs(quotient - round(quotient)) > 1e-10:
                    self.errors.append({
                        'path': path,
                        'message': f'Value {instance} is not a multiple of {schema["multipleOf"]}',
                        'value': instance
                    })
            elif instance % schema['multipleOf'] != 0:
                self.errors.append({
                    'path': path,
                    'message': f'Value {instance} is not a multiple of {schema["multipleOf"]}',
                    'value': instance
                })
    
    def _validate_array(self, instance: List[Any], schema: Dict[str, Any], path: str):
        """Validate array constraints"""
        if 'minItems' in schema and len(instance) < schema['minItems']:
            self.errors.append({
                'path': path,
                'message': f'Array length {len(instance)} is less than minimum {schema["minItems"]}',
                'value': instance
            })
        
        if 'maxItems' in schema and len(instance) > schema['maxItems']:
            self.errors.append({
                'path': path,
                'message': f'Array length {len(instance)} exceeds maximum {schema["maxItems"]}',
                'value': instance
            })
        
        if 'uniqueItems' in schema and schema['uniqueItems']:
            seen = []
            for i, item in enumerate(instance):
                item_str = json.dumps(item, sort_keys=True)
                if item_str in seen:
                    self.errors.append({
                        'path': f"{path}[{i}]",
                        'message': 'Duplicate items found in array',
                        'value': item
                    })
                seen.append(item_str)
        
        # Validate items
        if 'items' in schema:
            for i, item in enumerate(instance):
                item_path = f"{path}[{i}]"
                self._validate_recursive(item, schema['items'], item_path)
    
    def _validate_object(self, instance: Dict[str, Any], schema: Dict[str, Any], path: str):
        """Validate object constraints"""
        # Check required properties
        if 'required' in schema:
            for prop in schema['required']:
                if prop not in instance:
                    self.errors.append({
                        'path': path,
                        'message': f'Missing required property: "{prop}"',
                        'value': None
                    })
        
        # Validate properties
        if 'properties' in schema:
            for prop, prop_schema in schema['properties'].items():
                if prop in instance:
                    prop_path = f"{path}.{prop}" if path else prop
                    self._validate_recursive(instance[prop], prop_schema, prop_path)
        
        # Validate additionalProperties
        if 'additionalProperties' in schema:
            defined_props = set(schema.get('properties', {}).keys())
            defined_props.update(schema.get('patternProperties', {}).keys())
            
            for prop in instance.keys():
                if prop not in defined_props:
                    if schema['additionalProperties'] is False:
                        self.errors.append({
                            'path': path,
                            'message': f'Additional property "{prop}" is not allowed',
                            'value': instance[prop]
                        })
                    elif isinstance(schema['additionalProperties'], dict):
                        prop_path = f"{path}.{prop}" if path else prop
                        self._validate_recursive(instance[prop], schema['additionalProperties'], prop_path)
        
        # Check minProperties and maxProperties
        if 'minProperties' in schema and len(instance) < schema['minProperties']:
            self.errors.append({
                'path': path,
                'message': f'Object has {len(instance)} properties, minimum is {schema["minProperties"]}',
                'value': instance
            })
        
        if 'maxProperties' in schema and len(instance) > schema['maxProperties']:
            self.errors.append({
                'path': path,
                'message': f'Object has {len(instance)} properties, maximum is {schema["maxProperties"]}',
                'value': instance
            })
    
    def _validate_format(self, instance: str, format_name: str, path: str):
        """Validate string format"""
        validator = self.FORMAT_VALIDATORS.get(format_name)
        if validator and not validator(instance):
            self.errors.append({
                'path': path,
                'message': f'Value does not match format "{format_name}"',
                'value': instance
            })
    
    def _get_json_type(self, value: Any) -> str:
        """Get the JSON type of a value"""
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return 'boolean'
        elif isinstance(value, int):
            return 'integer'
        elif isinstance(value, float):
            return 'number'
        elif isinstance(value, str):
            return 'string'
        elif isinstance(value, list):
            return 'array'
        elif isinstance(value, dict):
            return 'object'
        return 'unknown'


class SchemaVisualizer:
    """
    JSON Schema Terminal Visualizer
    JSON Schema终端可视化器
    """
    
    # Type icons and colors
    # 类型图标和颜色
    TYPE_STYLES = {
        'object': (Colors.BLUE, '⧉'),
        'array': (Colors.MAGENTA, '☰'),
        'string': (Colors.GREEN, '""'),
        'integer': (Colors.YELLOW, '#'),
        'number': (Colors.YELLOW, '#.'),
        'boolean': (Colors.CYAN, '◉'),
        'null': (Colors.BRIGHT_BLACK, 'ø'),
    }
    
    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors
        self.indent_size = 2
    
    def visualize(self, schema: Dict[str, Any], title: str = "JSON Schema") -> str:
        """
        Generate a visual representation of the schema
        生成schema的可视化表示
        """
        lines = []
        
        # Header
        lines.append(self._colorize(f"{'='*60}", Colors.BOLD + Colors.BLUE))
        lines.append(self._colorize(f"  📋 {title}", Colors.BOLD + Colors.WHITE))
        lines.append(self._colorize(f"{'='*60}", Colors.BOLD + Colors.BLUE))
        lines.append("")
        
        # Schema info
        schema_info = self._extract_schema_info(schema)
        lines.append(self._colorize("📊 Schema Information:", Colors.BOLD + Colors.CYAN))
        lines.append(f"  • ID: {schema_info.get('id', 'N/A')}")
        lines.append(f"  • Title: {schema_info.get('title', 'N/A')}")
        lines.append(f"  • Description: {schema_info.get('description', 'N/A')[:80]}..." if len(schema_info.get('description', '')) > 80 else f"  • Description: {schema_info.get('description', 'N/A')}")
        lines.append(f"  • Version: {schema_info.get('version', 'N/A')}")
        lines.append("")
        
        # Structure tree
        lines.append(self._colorize("🌳 Structure Tree:", Colors.BOLD + Colors.CYAN))
        lines.append("")
        tree_lines = self._build_tree(schema, "")
        lines.extend(tree_lines)
        lines.append("")
        
        # Statistics
        stats = self._calculate_stats(schema)
        lines.append(self._colorize("📈 Statistics:", Colors.BOLD + Colors.CYAN))
        lines.append(f"  • Total Properties: {stats['properties']}")
        lines.append(f"  • Required Fields: {stats['required']}")
        lines.append(f"  • Nested Objects: {stats['objects']}")
        lines.append(f"  • Arrays: {stats['arrays']}")
        lines.append(f"  • String Fields: {stats['strings']}")
        lines.append(f"  • Number Fields: {stats['numbers']}")
        lines.append(f"  • Boolean Fields: {stats['booleans']}")
        lines.append("")
        
        # Footer
        lines.append(self._colorize(f"{'='*60}", Colors.BOLD + Colors.BLUE))
        
        return "\n".join(lines)
    
    def _colorize(self, text: str, color: str) -> str:
        """Apply color to text if colors are enabled"""
        if self.use_colors:
            return f"{color}{text}{Colors.RESET}"
        return text
    
    def _extract_schema_info(self, schema: Dict[str, Any]) -> Dict[str, str]:
        """Extract basic schema information"""
        return {
            'id': schema.get('$id', 'N/A'),
            'title': schema.get('title', 'N/A'),
            'description': schema.get('description', 'N/A'),
            'version': schema.get('$schema', 'N/A'),
        }
    
    def _build_tree(self, schema: Any, prefix: str, name: str = "root") -> List[str]:
        """Build the tree structure for visualization"""
        lines = []
        
        if isinstance(schema, bool):
            icon = Colors.GREEN + "✓" if schema else Colors.RED + "✗"
            lines.append(f"{prefix}{icon} {name} (always {schema}){Colors.RESET}")
            return lines
        
        if not isinstance(schema, dict):
            lines.append(f"{prefix}• {name}: {schema}")
            return lines
        
        schema_type = schema.get('type', 'any')
        type_str = schema_type if isinstance(schema_type, str) else '|'.join(schema_type)
        
        # Get type style
        type_color, type_icon = self.TYPE_STYLES.get(type_str, (Colors.WHITE, '?'))
        
        # Build node label
        required = schema.get('required', [])
        is_required = name in required if isinstance(required, list) else False
        req_marker = self._colorize(" *", Colors.RED) if is_required else ""
        
        node_label = f"{type_icon} {name}: {type_str}{req_marker}"
        lines.append(f"{prefix}{self._colorize(node_label, type_color)}")
        
        # Add description if available
        if 'description' in schema:
            desc = schema['description'][:50] + "..." if len(schema['description']) > 50 else schema['description']
            lines.append(f"{prefix}  {self._colorize('│', Colors.DIM)} {self._colorize(f'💡 {desc}', Colors.BRIGHT_BLACK)}")
        
        # Add constraints
        constraints = self._extract_constraints(schema)
        if constraints:
            constraint_str = ", ".join(constraints)
            lines.append(f"{prefix}  {self._colorize('│', Colors.DIM)} {self._colorize(f'⚙️  {constraint_str}', Colors.BRIGHT_BLACK)}")
        
        # Process properties for objects
        if 'properties' in schema and isinstance(schema['properties'], dict):
            props = schema['properties']
            for i, (prop_name, prop_schema) in enumerate(props.items()):
                is_last = (i == len(props) - 1)
                branch = "└── " if is_last else "├── "
                next_prefix = prefix + ("    " if is_last else "│   ")
                
                subtree = self._build_tree(prop_schema, next_prefix, prop_name)
                if subtree:
                    lines.append(f"{prefix}  {self._colorize(branch, Colors.DIM)}{subtree[0].strip()}")
                    lines.extend(subtree[1:])
        
        # Process items for arrays
        if 'items' in schema:
            items = schema['items']
            branch = "└── "
            next_prefix = prefix + "    "
            
            subtree = self._build_tree(items, next_prefix, "items")
            if subtree:
                lines.append(f"{prefix}  {self._colorize(branch, Colors.DIM)}{subtree[0].strip()}")
                lines.extend(subtree[1:])
        
        return lines
    
    def _extract_constraints(self, schema: Dict[str, Any]) -> List[str]:
        """Extract validation constraints from schema"""
        constraints = []
        
        # String constraints
        if 'minLength' in schema:
            constraints.append(f"min:{schema['minLength']}")
        if 'maxLength' in schema:
            constraints.append(f"max:{schema['maxLength']}")
        if 'pattern' in schema:
            constraints.append("pattern")
        if 'format' in schema:
            constraints.append(f"format:{schema['format']}")
        
        # Number constraints
        if 'minimum' in schema:
            constraints.append(f"≥{schema['minimum']}")
        if 'maximum' in schema:
            constraints.append(f"≤{schema['maximum']}")
        if 'exclusiveMinimum' in schema:
            constraints.append(f">{schema['exclusiveMinimum']}")
        if 'exclusiveMaximum' in schema:
            constraints.append(f"<{schema['exclusiveMaximum']}")
        if 'multipleOf' in schema:
            constraints.append(f"×{schema['multipleOf']}")
        
        # Array constraints
        if 'minItems' in schema:
            constraints.append(f"items≥{schema['minItems']}")
        if 'maxItems' in schema:
            constraints.append(f"items≤{schema['maxItems']}")
        if 'uniqueItems' in schema:
            constraints.append("unique")
        
        # Object constraints
        if 'minProperties' in schema:
            constraints.append(f"props≥{schema['minProperties']}")
        if 'maxProperties' in schema:
            constraints.append(f"props≤{schema['maxProperties']}")
        if 'additionalProperties' in schema:
            if schema['additionalProperties'] is False:
                constraints.append("no extra props")
        
        # Enum and const
        if 'enum' in schema:
            constraints.append(f"enum[{len(schema['enum'])}]")
        if 'const' in schema:
            constraints.append("const")
        
        return constraints
    
    def _calculate_stats(self, schema: Any, stats: Optional[Dict[str, int]] = None) -> Dict[str, int]:
        """Calculate schema statistics"""
        if stats is None:
            stats = {
                'properties': 0,
                'required': 0,
                'objects': 0,
                'arrays': 0,
                'strings': 0,
                'numbers': 0,
                'booleans': 0,
            }
        
        if not isinstance(schema, dict):
            return stats
        
        schema_type = schema.get('type', '')
        
        if isinstance(schema_type, str):
            if schema_type == 'object':
                stats['objects'] += 1
            elif schema_type == 'array':
                stats['arrays'] += 1
            elif schema_type == 'string':
                stats['strings'] += 1
            elif schema_type in ('integer', 'number'):
                stats['numbers'] += 1
            elif schema_type == 'boolean':
                stats['booleans'] += 1
        
        if 'properties' in schema:
            props = schema['properties']
            stats['properties'] += len(props)
            
            required = schema.get('required', [])
            if isinstance(required, list):
                stats['required'] += len(required)
            
            for prop_schema in props.values():
                self._calculate_stats(prop_schema, stats)
        
        if 'items' in schema:
            self._calculate_stats(schema['items'], stats)
        
        return stats


class SchemaComparator:
    """
    JSON Schema Comparator for diff visualization
    JSON Schema差异比较器
    """
    
    def compare(self, schema1: Dict[str, Any], schema2: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare two schemas and return differences
        比较两个schema并返回差异
        """
        differences = {
            'added': [],
            'removed': [],
            'modified': [],
            'unchanged': []
        }
        
        self._compare_recursive(schema1, schema2, "", differences)
        return differences
    
    def _compare_recursive(self, s1: Any, s2: Any, path: str, differences: Dict[str, List]):
        """Recursive comparison helper"""
        if isinstance(s1, dict) and isinstance(s2, dict):
            all_keys = set(s1.keys()) | set(s2.keys())
            
            for key in all_keys:
                new_path = f"{path}.{key}" if path else key
                
                if key not in s1:
                    differences['added'].append({'path': new_path, 'value': s2[key]})
                elif key not in s2:
                    differences['removed'].append({'path': new_path, 'value': s1[key]})
                elif s1[key] != s2[key]:
                    if isinstance(s1[key], (dict, list)) and isinstance(s2[key], (dict, list)):
                        self._compare_recursive(s1[key], s2[key], new_path, differences)
                    else:
                        differences['modified'].append({
                            'path': new_path,
                            'old': s1[key],
                            'new': s2[key]
                        })
                else:
                    differences['unchanged'].append({'path': new_path, 'value': s1[key]})
        
        elif isinstance(s1, list) and isinstance(s2, list):
            max_len = max(len(s1), len(s2))
            for i in range(max_len):
                new_path = f"{path}[{i}]"
                if i >= len(s1):
                    differences['added'].append({'path': new_path, 'value': s2[i]})
                elif i >= len(s2):
                    differences['removed'].append({'path': new_path, 'value': s1[i]})
                elif s1[i] != s2[i]:
                    differences['modified'].append({
                        'path': new_path,
                        'old': s1[i],
                        'new': s2[i]
                    })
                else:
                    differences['unchanged'].append({'path': new_path, 'value': s1[i]})
        
        elif s1 != s2:
            differences['modified'].append({'path': path, 'old': s1, 'new': s2})
    
    def format_diff(self, differences: Dict[str, Any], use_colors: bool = True) -> str:
        """Format differences for display"""
        lines = []
        
        if use_colors:
            added_color = Colors.GREEN
            removed_color = Colors.RED
            modified_color = Colors.YELLOW
            reset = Colors.RESET
        else:
            added_color = removed_color = modified_color = reset = ""
        
        if differences['added']:
            lines.append(f"\n{added_color}✚ Added ({len(differences['added'])}):{reset}")
            for item in differences['added']:
                lines.append(f"  + {item['path']}")
        
        if differences['removed']:
            lines.append(f"\n{removed_color}✗ Removed ({len(differences['removed'])}):{reset}")
            for item in differences['removed']:
                lines.append(f"  - {item['path']}")
        
        if differences['modified']:
            lines.append(f"\n{modified_color}✎ Modified ({len(differences['modified'])}):{reset}")
            for item in differences['modified']:
                lines.append(f"  ~ {item['path']}")
                lines.append(f"    Old: {item['old']}")
                lines.append(f"    New: {item['new']}")
        
        if not any(differences[k] for k in ['added', 'removed', 'modified']):
            lines.append(f"\n{added_color}✓ Schemas are identical{reset}")
        
        return "\n".join(lines)


def load_json_file(filepath: str) -> Any:
    """Load and parse a JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Colors.RED}Error: File not found: {filepath}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}Error: Invalid JSON in {filepath}: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Error loading {filepath}: {e}{Colors.RESET}", file=sys.stderr)
        sys.exit(1)


def validate_command(args):
    """Handle validate command"""
    schema = load_json_file(args.schema)
    data = load_json_file(args.data)
    
    validator = SchemaValidator()
    is_valid = validator.validate(data, schema)
    
    if is_valid:
        print(f"{Colors.GREEN}✓ Validation passed!{Colors.RESET}")
        print(f"  Data conforms to schema: {args.schema}")
        return 0
    else:
        print(f"{Colors.RED}✗ Validation failed!{Colors.RESET}")
        print(f"  Found {len(validator.errors)} error(s):\n")
        
        for i, error in enumerate(validator.errors, 1):
            print(f"  {Colors.RED}{i}.{Colors.RESET} Path: {Colors.CYAN}{error['path'] or '(root)'}{Colors.RESET}")
            print(f"     Message: {error['message']}")
            if error['value'] is not None:
                value_str = str(error['value'])[:50]
                if len(str(error['value'])) > 50:
                    value_str += "..."
                print(f"     Value: {Colors.YELLOW}{value_str}{Colors.RESET}")
            print()
        
        return 1


def visualize_command(args):
    """Handle visualize command"""
    schema = load_json_file(args.schema)
    
    visualizer = SchemaVisualizer(use_colors=not args.no_color)
    output = visualizer.visualize(schema, args.title or Path(args.schema).stem)
    
    print(output)
    return 0


def compare_command(args):
    """Handle compare command"""
    schema1 = load_json_file(args.schema1)
    schema2 = load_json_file(args.schema2)
    
    comparator = SchemaComparator()
    differences = comparator.compare(schema1, schema2)
    
    print(f"{Colors.BOLD}Comparing schemas:{Colors.RESET}")
    print(f"  Left:  {args.schema1}")
    print(f"  Right: {args.schema2}")
    
    diff_output = comparator.format_diff(differences, use_colors=not args.no_color)
    print(diff_output)
    
    # Return non-zero if there are differences
    has_diff = any(differences[k] for k in ['added', 'removed', 'modified'])
    return 1 if has_diff and args.strict else 0


def stats_command(args):
    """Handle stats command"""
    schema = load_json_file(args.schema)
    
    visualizer = SchemaVisualizer(use_colors=not args.no_color)
    stats = visualizer._calculate_stats(schema)
    
    print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}  📊 Schema Statistics{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
    print()
    print(f"  File: {args.schema}")
    print()
    print(f"  {Colors.CYAN}Structure:{Colors.RESET}")
    print(f"    • Total Properties: {stats['properties']}")
    print(f"    • Required Fields:  {stats['required']}")
    print(f"    • Nested Objects:   {stats['objects']}")
    print(f"    • Arrays:           {stats['arrays']}")
    print()
    print(f"  {Colors.CYAN}Types:{Colors.RESET}")
    print(f"    • Strings:   {stats['strings']}")
    print(f"    • Numbers:   {stats['numbers']}")
    print(f"    • Booleans:  {stats['booleans']}")
    print()
    print(f"{Colors.BOLD}{'='*50}{Colors.RESET}")
    
    return 0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        prog='schemapilot',
        description='SchemaPilot - Lightweight JSON Schema Terminal Visualizer & Validator',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s visualize schema.json           # Visualize schema structure
  %(prog)s validate schema.json data.json  # Validate JSON data
  %(prog)s compare schema1.json schema2.json  # Compare two schemas
  %(prog)s stats schema.json               # Show schema statistics

For more information, visit: https://github.com/gitstq/SchemaPilot
        """
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 1.0.0'
    )
    
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Validate command
    validate_parser = subparsers.add_parser(
        'validate',
        help='Validate JSON data against a schema',
        description='Validate JSON data against a JSON Schema'
    )
    validate_parser.add_argument('schema', help='Path to JSON schema file')
    validate_parser.add_argument('data', help='Path to JSON data file to validate')
    
    # Visualize command
    visualize_parser = subparsers.add_parser(
        'visualize',
        help='Visualize schema structure',
        aliases=['viz'],
        description='Visualize JSON Schema structure in terminal'
    )
    visualize_parser.add_argument('schema', help='Path to JSON schema file')
    visualize_parser.add_argument('-t', '--title', help='Custom title for visualization')
    
    # Compare command
    compare_parser = subparsers.add_parser(
        'compare',
        help='Compare two schemas',
        aliases=['diff'],
        description='Compare two JSON Schemas and show differences'
    )
    compare_parser.add_argument('schema1', help='Path to first schema file')
    compare_parser.add_argument('schema2', help='Path to second schema file')
    compare_parser.add_argument(
        '--strict',
        action='store_true',
        help='Return non-zero exit code if schemas differ'
    )
    
    # Stats command
    stats_parser = subparsers.add_parser(
        'stats',
        help='Show schema statistics',
        description='Display statistics about a JSON Schema'
    )
    stats_parser.add_argument('schema', help='Path to JSON schema file')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 0
    
    # Dispatch to appropriate command handler
    commands = {
        'validate': validate_command,
        'visualize': visualize_command,
        'viz': visualize_command,
        'compare': compare_command,
        'diff': compare_command,
        'stats': stats_command,
    }
    
    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        parser.print_help()
        return 0


if __name__ == '__main__':
    sys.exit(main())
