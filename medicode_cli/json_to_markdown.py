#!/usr/bin/env python3
"""
Convert tutorial JSON to Markdown format for easier editing
and convert Markdown back to JSON
"""

import json
import os
import re
import sys

def clean_code_block(code):
    """Remove ```python and ``` from code blocks in the JSON solution strings"""
    if code.startswith('```python\n') and code.endswith('\n```'):
        return code[10:-4]
    return code

def json_to_markdown(json_data):
    """Convert tutorial JSON to structured markdown"""
    md_lines = []
    
    # Course header
    md_lines.append(f"# {json_data['title']}")
    md_lines.append(f"Language: {json_data['language']}")
    md_lines.append("")
    
    # Process each lesson
    for lesson_index, lesson in enumerate(json_data['lessons'], 1):
        lesson_type = lesson['type']
        md_lines.append(f"## Lesson {lesson_index}: {lesson['title']} ({lesson_type})")
        md_lines.append("")
        
        if lesson_type == "informational":
            # Informational lessons just have content
            md_lines.append(lesson['content'])
        else:  # Interactive lesson
            # Add lesson text
            md_lines.append(lesson['text'])
            md_lines.append("")
            
            # Add starter code if present
            if 'starter_code' in lesson and lesson['starter_code']:
                md_lines.append("### Starter Code")
                md_lines.append("```python")
                md_lines.append(lesson['starter_code'])
                md_lines.append("```")
                md_lines.append("")
            
            # Process each task
            for task_index, task in enumerate(lesson['tasks'], 1):
                md_lines.append(f"### Task {task_index}")
                md_lines.append(task['content'])
                md_lines.append("")
                
                # Add solution
                md_lines.append("#### Solution")
                md_lines.append("```python")
                solution_code = clean_code_block(task['solution'])
                md_lines.append(solution_code)
                md_lines.append("```")
                md_lines.append("")
                
                # Add driver code
                md_lines.append("#### Driver Code")
                md_lines.append("```python")
                md_lines.append(task['driver_code'])
                md_lines.append("```")
                md_lines.append("")
                
                # Add allow_error flag
                md_lines.append("#### Allow Error")
                md_lines.append(str(task['allow_error']).lower())
                md_lines.append("")
        
        md_lines.append("")  # Extra line between lessons
    
    return "\n".join(md_lines)

def extract_code_block(lines, start_idx):
    """Extract a code block from markdown lines starting at a specific index"""
    if start_idx >= len(lines) or not lines[start_idx].startswith("```"):
        return "", start_idx
    
    code_lines = []
    i = start_idx + 1
    
    # Skip the opening code fence and language identifier
    while i < len(lines) and not lines[i].startswith("```"):
        code_lines.append(lines[i])
        i += 1
    
    return "\n".join(code_lines), i + 1  # Skip the closing code fence

def markdown_to_json(md_content):
    """Convert the markdown back to JSON format"""
    lines = md_content.split("\n")
    result = {}
    lessons = []
    
    # Parse title and language
    if lines and lines[0].startswith("# "):
        result["title"] = lines[0][2:].strip()
    
    if len(lines) > 1 and lines[1].startswith("Language: "):
        result["language"] = lines[1][10:].strip()
    
    # Process each lesson
    i = 0
    current_lesson = None
    current_task = None
    
    while i < len(lines):
        line = lines[i].strip()
        
        # New lesson
        if line.startswith("## Lesson "):
            # Save previous lesson if exists
            if current_lesson:
                lessons.append(current_lesson)
            
            # Parse lesson title and type
            match = re.match(r"## Lesson \d+: (.*) \((.*)\)", line)
            if match:
                title, lesson_type = match.groups()
                current_lesson = {
                    "type": lesson_type,
                    "title": title
                }
                
                if lesson_type == "interactive":
                    current_lesson["tasks"] = []
            i += 1
        
        # Lesson content for informational lessons
        elif current_lesson and current_lesson["type"] == "informational" and i + 1 < len(lines):
            # Collect all content until next lesson or end
            content_lines = []
            i += 1  # Skip the current line
            
            while i < len(lines) and not lines[i].startswith("## Lesson "):
                content_lines.append(lines[i])
                i += 1
            
            current_lesson["content"] = "\n".join(content_lines).strip()
        
        # Lesson text for interactive lessons
        elif current_lesson and current_lesson["type"] == "interactive" and not line.startswith("###"):
            # Collect text until next section
            text_lines = []
            
            while i < len(lines) and not lines[i].startswith("###") and not lines[i].startswith("## Lesson "):
                text_lines.append(lines[i])
                i += 1
            
            if text_lines:
                current_lesson["text"] = "\n".join(text_lines).strip()
        
        # Starter code
        elif line == "### Starter Code":
            i += 1
            starter_code, i = extract_code_block(lines, i)
            current_lesson["starter_code"] = starter_code
        
        # Task 
        elif line.startswith("### Task "):
            task_number = int(line[8:].strip())
            current_task = {"content": ""}
            i += 1
            
            # Get task content
            content_lines = []
            while i < len(lines) and not lines[i].startswith("####") and not lines[i].startswith("###"):
                content_lines.append(lines[i])
                i += 1
            
            if content_lines:
                current_task["content"] = "\n".join(content_lines).strip()
        
        # Solution
        elif line == "#### Solution":
            i += 1
            solution_code, i = extract_code_block(lines, i)
            
            # Add ```python and ``` for consistency
            current_task["solution"] = f"```python\n{solution_code}\n```"
        
        # Driver code
        elif line == "#### Driver Code":
            i += 1
            driver_code, i = extract_code_block(lines, i)
            current_task["driver_code"] = driver_code
        
        # Allow error
        elif line == "#### Allow Error":
            i += 1
            if i < len(lines):
                current_task["allow_error"] = lines[i].strip().lower() == "true"
                i += 1
                
                # After processing full task, add it to the lesson
                if current_lesson and "tasks" in current_lesson:
                    current_lesson["tasks"].append(current_task)
        
        else:
            i += 1
    
    # Add the last lesson
    if current_lesson:
        lessons.append(current_lesson)
    
    result["lessons"] = lessons
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python json_to_markdown.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not output_file:
        if input_file.endswith('.json'):
            output_file = input_file.replace('.json', '.md')
        elif input_file.endswith('.md'):
            output_file = input_file.replace('.md', '.json')
        else:
            print("Error: Input file must be .json or .md")
            sys.exit(1)
    
    try:
        if input_file.endswith('.json'):
            # Convert JSON to Markdown
            with open(input_file, 'r') as f:
                json_data = json.load(f)
            
            markdown = json_to_markdown(json_data)
            
            with open(output_file, 'w') as f:
                f.write(markdown)
            
            print(f"Successfully converted {input_file} to {output_file}")
        
        elif input_file.endswith('.md'):
            # Convert Markdown to JSON
            with open(input_file, 'r') as f:
                md_content = f.read()
            
            json_data = markdown_to_json(md_content)
            
            with open(output_file, 'w') as f:
                json.dump(json_data, f, indent=2)
            
            print(f"Successfully converted {input_file} to {output_file}")
        
        else:
            print("Error: Input file must be .json or .md")
    
    except json.JSONDecodeError:
        print(f"Error: {input_file} is not a valid JSON file")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 