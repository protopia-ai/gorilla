#!/usr/bin/env python3
"""
Convert BFCL function format to OpenAI chat completions tools format.
"""

from typing import List, Dict, Any
import json


def convert_bfcl_to_openai_tools(bfcl_functions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Convert BFCL function format to OpenAI chat completions tools format.
    
    Args:
        bfcl_functions: List of functions in BFCL format
        
    Returns:
        List of functions in OpenAI tools format
    """
    tools = []
    
    for func in bfcl_functions:
        # Extract parameters, ensuring type is 'object' instead of 'dict'
        parameters = func.get('parameters', {}).copy()
        if parameters.get('type') == 'dict':
            parameters['type'] = 'object'
        
        tool = {
            "type": "function",
            "function": {
                "name": func['name'],
                "description": func['description'],
                "parameters": parameters
            }
        }
        tools.append(tool)
    
    return tools


def test_convert_bfcl_to_openai_tools():
    """Test cases for the conversion function."""
    
    # Test case 1: Triangle area function
    bfcl_input_1 = [
        {
            'description': 'Calculate the area of a triangle given its base and height. '
                          'Note that the provided function is in Python 3 syntax.',
            'name': 'calculate_triangle_area',
            'parameters': {
                'properties': {
                    'base': {
                        'description': 'The base of the triangle.',
                        'type': 'integer'
                    },
                    'height': {
                        'description': 'The height of the triangle.',
                        'type': 'integer'
                    },
                    'unit': {
                        'description': 'The unit of measure (defaults to \'units\' if not specified)',
                        'type': 'string'
                    }
                },
                'required': ['base', 'height'],
                'type': 'dict'
            }
        }
    ]
    
    expected_output_1 = [
        {
            "type": "function",
            "function": {
                "name": "calculate_triangle_area",
                "description": "Calculate the area of a triangle given its base and height. "
                              "Note that the provided function is in Python 3 syntax.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "base": {
                            "description": "The base of the triangle.",
                            "type": "integer"
                        },
                        "height": {
                            "description": "The height of the triangle.",
                            "type": "integer"
                        },
                        "unit": {
                            "description": "The unit of measure (defaults to 'units' if not specified)",
                            "type": "string"
                        }
                    },
                    "required": ["base", "height"]
                }
            }
        }
    ]
    
    result_1 = convert_bfcl_to_openai_tools(bfcl_input_1)
    assert result_1 == expected_output_1, f"Test 1 failed. Got: {json.dumps(result_1, indent=2)}"
    print("✅ Test 1 (Triangle area function) passed")
    
    # Test case 2: Multiple functions
    bfcl_input_2 = [
        {
            'name': 'get_weather',
            'description': 'Get current weather information for a location',
            'parameters': {
                'type': 'dict',
                'properties': {
                    'location': {'type': 'string', 'description': 'City name'},
                    'units': {'type': 'string', 'description': 'Temperature units', 'enum': ['celsius', 'fahrenheit']}
                },
                'required': ['location']
            }
        },
        {
            'name': 'calculate_distance',
            'description': 'Calculate distance between two points',
            'parameters': {
                'type': 'dict',
                'properties': {
                    'point_a': {'type': 'object', 'description': 'First point coordinates'},
                    'point_b': {'type': 'object', 'description': 'Second point coordinates'}
                },
                'required': ['point_a', 'point_b']
            }
        }
    ]
    
    expected_output_2 = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current weather information for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"},
                        "units": {"type": "string", "description": "Temperature units", "enum": ["celsius", "fahrenheit"]}
                    },
                    "required": ["location"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "calculate_distance",
                "description": "Calculate distance between two points",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "point_a": {"type": "object", "description": "First point coordinates"},
                        "point_b": {"type": "object", "description": "Second point coordinates"}
                    },
                    "required": ["point_a", "point_b"]
                }
            }
        }
    ]
    
    result_2 = convert_bfcl_to_openai_tools(bfcl_input_2)
    assert result_2 == expected_output_2, f"Test 2 failed. Got: {json.dumps(result_2, indent=2)}"
    print("✅ Test 2 (Multiple functions) passed")
    
    # Test case 3: Function without parameters
    bfcl_input_3 = [
        {
            'name': 'get_current_time',
            'description': 'Get the current system time',
            'parameters': {
                'type': 'dict',
                'properties': {},
                'required': []
            }
        }
    ]
    
    expected_output_3 = [
        {
            "type": "function",
            "function": {
                "name": "get_current_time",
                "description": "Get the current system time",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    ]
    
    result_3 = convert_bfcl_to_openai_tools(bfcl_input_3)
    assert result_3 == expected_output_3, f"Test 3 failed. Got: {json.dumps(result_3, indent=2)}"
    print("✅ Test 3 (Function without parameters) passed")
    
    # Test case 4: Empty input
    result_4 = convert_bfcl_to_openai_tools([])
    assert result_4 == [], "Test 4 failed. Expected empty list"
    print("✅ Test 4 (Empty input) passed")
    
    # Test case 5: Function with already correct 'object' type (edge case)
    bfcl_input_5 = [
        {
            'name': 'test_function',
            'description': 'A test function',
            'parameters': {
                'type': 'object',  # Already correct
                'properties': {'param1': {'type': 'string'}},
                'required': ['param1']
            }
        }
    ]
    
    expected_output_5 = [
        {
            "type": "function",
            "function": {
                "name": "test_function",
                "description": "A test function",
                "parameters": {
                    "type": "object",
                    "properties": {"param1": {"type": "string"}},
                    "required": ["param1"]
                }
            }
        }
    ]
    
    result_5 = convert_bfcl_to_openai_tools(bfcl_input_5)
    assert result_5 == expected_output_5, f"Test 5 failed. Got: {json.dumps(result_5, indent=2)}"
    print("✅ Test 5 (Function with correct 'object' type) passed")
    
    print("\n🎉 All tests passed successfully!")


def main():
    """Main function to demonstrate usage and run tests."""
    print("BFCL to OpenAI Tools Format Converter")
    print("=" * 40)
    
    # Example usage
    example_bfcl = [
        {
            'description': 'Calculate the area of a triangle given its base and height. '
                          'Note that the provided function is in Python 3 syntax.',
            'name': 'calculate_triangle_area',
            'parameters': {
                'properties': {
                    'base': {'description': 'The base of the triangle.', 'type': 'integer'},
                    'height': {'description': 'The height of the triangle.', 'type': 'integer'},
                    'unit': {'description': 'The unit of measure (defaults to \'units\' if not specified)', 'type': 'string'}
                },
                'required': ['base', 'height'],
                'type': 'dict'
            }
        }
    ]
    
    print("\nExample Input (BFCL format):")
    print(json.dumps(example_bfcl, indent=2))
    
    converted = convert_bfcl_to_openai_tools(example_bfcl)
    
    print("\nExample Output (OpenAI tools format):")
    print(json.dumps(converted, indent=2))
    
    print("\nRunning tests...")
    print("-" * 20)
    test_convert_bfcl_to_openai_tools()


if __name__ == "__main__":
    main()