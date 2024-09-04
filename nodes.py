import re

class SearchBySubstring:
    # Class method to define input types
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True, "default": "whole_word", "tooltip": "Source to be searched"}), 
                "pattern": ("STRING", {"default": "eyes", "tooltip": "Substring to match (e.g., 'eyes')"}), 
            },
            "optional": {
                "default": ("STRING", {"default": "not found", "tooltip": "Fallback value if 'pattern' is not found"}), 
            }
        }

    # Define return types and names
    RETURN_TYPES = ("STRING", "LIST", "INT", "BOOLEAN")
    RETURN_NAMES = ("match", "matchList", "count", "found")

    FUNCTION = "searchBySubstring"
    CATEGORY = "Phando/Text"

    def searchBySubstring(self, text: str, pattern: str, default="not found") -> tuple:
        pattern = pattern.encode().decode("unicode_escape").lower()
        text = text.lower()

        regex = rf'\b\w*{pattern}\w*\b'
        matchList = re.findall(regex, text)

        match = matchList[0] if matchList else default

        # Prepare the output tuple
        output = (match, matchList, len(matchList), len(matchList) > 0)
        return output
    

class TextConcatenateDynamic:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        min_input = 2
        max_input = 10
        inputs = {
            "required": {
                "delimiter": ("STRING", {"default": ",", "tooltip": "Delimiter to use for concatenation"}),
                "count": ("INT", {"default": min_input, "min": min_input, "max": max_input}),
            },
        }
        
        inputCount = inputs['required']['count'][1]['default']
        for i in range(1, inputCount+1):
            inputs["dynamic"][f"text_{i+1}"] = ("STRING", {"default": "", "tooltip": f"Text input {i + 1}"})

        return inputs

    # Define the return types
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)

    FUNCTION = "textConcatenateDynamic"
    CATEGORY = "Phando/Text"
    
    def textConcatenateDynamic(self, delimiter, count, optional_lora_stack=None, **kwargs):
        inputs = [kwargs.get(f"text_{i + 1}", "") for i in range(count)]
        concatenated_result = delimiter.join(inputs)
        return (concatenated_result,)
    

NODE_CLASS_MAPPINGS = {
    'SearchBySubstring': SearchBySubstring,
    'TextConcatenateDynamic': TextConcatenateDynamic,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    'SearchBySubstring': 'Search by Substring',
    'TextConcatenateDynamic': 'Text Concatenate - Dynamic',
}