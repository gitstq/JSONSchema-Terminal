#!/usr/bin/env python3
"""
Tests for SchemaValidator
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemapilot import SchemaValidator


class TestSchemaValidator(unittest.TestCase):
    """Test cases for SchemaValidator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validator = SchemaValidator()
    
    def test_type_validation_null(self):
        """Test null type validation"""
        schema = {"type": "null"}
        self.assertTrue(self.validator.validate(None, schema))
        self.assertFalse(self.validator.validate("not null", schema))
    
    def test_type_validation_boolean(self):
        """Test boolean type validation"""
        schema = {"type": "boolean"}
        self.assertTrue(self.validator.validate(True, schema))
        self.assertTrue(self.validator.validate(False, schema))
        self.assertFalse(self.validator.validate("true", schema))
        self.assertFalse(self.validator.validate(1, schema))
    
    def test_type_validation_string(self):
        """Test string type validation"""
        schema = {"type": "string"}
        self.assertTrue(self.validator.validate("hello", schema))
        self.assertFalse(self.validator.validate(123, schema))
        self.assertFalse(self.validator.validate(None, schema))
    
    def test_type_validation_integer(self):
        """Test integer type validation"""
        schema = {"type": "integer"}
        self.assertTrue(self.validator.validate(42, schema))
        self.assertFalse(self.validator.validate(3.14, schema))
        self.assertFalse(self.validator.validate("42", schema))
        self.assertFalse(self.validator.validate(True, schema))
    
    def test_type_validation_number(self):
        """Test number type validation"""
        schema = {"type": "number"}
        self.assertTrue(self.validator.validate(42, schema))
        self.assertTrue(self.validator.validate(3.14, schema))
        self.assertFalse(self.validator.validate("3.14", schema))
    
    def test_type_validation_array(self):
        """Test array type validation"""
        schema = {"type": "array"}
        self.assertTrue(self.validator.validate([], schema))
        self.assertTrue(self.validator.validate([1, 2, 3], schema))
        self.assertFalse(self.validator.validate("not an array", schema))
    
    def test_type_validation_object(self):
        """Test object type validation"""
        schema = {"type": "object"}
        self.assertTrue(self.validator.validate({}, schema))
        self.assertTrue(self.validator.validate({"key": "value"}, schema))
        self.assertFalse(self.validator.validate("not an object", schema))
    
    def test_string_constraints_minlength(self):
        """Test string minLength constraint"""
        schema = {"type": "string", "minLength": 3}
        self.assertTrue(self.validator.validate("abc", schema))
        self.assertTrue(self.validator.validate("abcd", schema))
        self.assertFalse(self.validator.validate("ab", schema))
    
    def test_string_constraints_maxlength(self):
        """Test string maxLength constraint"""
        schema = {"type": "string", "maxLength": 5}
        self.assertTrue(self.validator.validate("abc", schema))
        self.assertTrue(self.validator.validate("abcde", schema))
        self.assertFalse(self.validator.validate("abcdef", schema))
    
    def test_string_constraints_pattern(self):
        """Test string pattern constraint"""
        schema = {"type": "string", "pattern": "^[a-z]+$"}
        self.assertTrue(self.validator.validate("abc", schema))
        self.assertFalse(self.validator.validate("ABC", schema))
        self.assertFalse(self.validator.validate("123", schema))
    
    def test_number_constraints_minimum(self):
        """Test number minimum constraint"""
        schema = {"type": "number", "minimum": 0}
        self.assertTrue(self.validator.validate(0, schema))
        self.assertTrue(self.validator.validate(5, schema))
        self.assertFalse(self.validator.validate(-1, schema))
    
    def test_number_constraints_maximum(self):
        """Test number maximum constraint"""
        schema = {"type": "number", "maximum": 100}
        self.assertTrue(self.validator.validate(50, schema))
        self.assertTrue(self.validator.validate(100, schema))
        self.assertFalse(self.validator.validate(101, schema))
    
    def test_number_constraints_multipleof(self):
        """Test number multipleOf constraint"""
        schema = {"type": "integer", "multipleOf": 5}
        self.assertTrue(self.validator.validate(10, schema))
        self.assertTrue(self.validator.validate(15, schema))
        self.assertFalse(self.validator.validate(7, schema))
    
    def test_array_constraints_minitems(self):
        """Test array minItems constraint"""
        schema = {"type": "array", "minItems": 2}
        self.assertTrue(self.validator.validate([1, 2], schema))
        self.assertTrue(self.validator.validate([1, 2, 3], schema))
        self.assertFalse(self.validator.validate([1], schema))
    
    def test_array_constraints_maxitems(self):
        """Test array maxItems constraint"""
        schema = {"type": "array", "maxItems": 3}
        self.assertTrue(self.validator.validate([1, 2], schema))
        self.assertTrue(self.validator.validate([1, 2, 3], schema))
        self.assertFalse(self.validator.validate([1, 2, 3, 4], schema))
    
    def test_array_constraints_uniqueitems(self):
        """Test array uniqueItems constraint"""
        schema = {"type": "array", "uniqueItems": True}
        self.assertTrue(self.validator.validate([1, 2, 3], schema))
        self.assertFalse(self.validator.validate([1, 2, 2], schema))
    
    def test_object_constraints_required(self):
        """Test object required constraint"""
        schema = {
            "type": "object",
            "required": ["name", "email"],
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string"}
            }
        }
        self.assertTrue(self.validator.validate({"name": "John", "email": "john@example.com"}, schema))
        self.assertFalse(self.validator.validate({"name": "John"}, schema))
    
    def test_object_constraints_additionalproperties_false(self):
        """Test object additionalProperties: false"""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string"}
            },
            "additionalProperties": False
        }
        self.assertTrue(self.validator.validate({"name": "John"}, schema))
        self.assertFalse(self.validator.validate({"name": "John", "extra": "value"}, schema))
    
    def test_enum_constraint(self):
        """Test enum constraint"""
        schema = {"enum": ["red", "green", "blue"]}
        self.assertTrue(self.validator.validate("red", schema))
        self.assertTrue(self.validator.validate("blue", schema))
        self.assertFalse(self.validator.validate("yellow", schema))
    
    def test_const_constraint(self):
        """Test const constraint"""
        schema = {"const": "specific value"}
        self.assertTrue(self.validator.validate("specific value", schema))
        self.assertFalse(self.validator.validate("other value", schema))
    
    def test_format_email(self):
        """Test email format validation"""
        schema = {"type": "string", "format": "email"}
        self.assertTrue(self.validator.validate("test@example.com", schema))
        self.assertFalse(self.validator.validate("invalid-email", schema))
    
    def test_format_uuid(self):
        """Test UUID format validation"""
        schema = {"type": "string", "format": "uuid"}
        self.assertTrue(self.validator.validate("550e8400-e29b-41d4-a716-446655440000", schema))
        self.assertFalse(self.validator.validate("not-a-uuid", schema))
    
    def test_complex_nested_schema(self):
        """Test complex nested schema validation"""
        schema = {
            "type": "object",
            "required": ["user"],
            "properties": {
                "user": {
                    "type": "object",
                    "required": ["id", "name"],
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            }
        }
        
        valid_data = {
            "user": {
                "id": 1,
                "name": "John",
                "tags": ["admin", "active"]
            }
        }
        self.assertTrue(self.validator.validate(valid_data, schema))
        
        invalid_data = {
            "user": {
                "id": "not an integer",
                "name": "John"
            }
        }
        self.assertFalse(self.validator.validate(invalid_data, schema))


if __name__ == '__main__':
    unittest.main()
