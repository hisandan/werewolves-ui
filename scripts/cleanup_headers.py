import os

# Markers to identify validity
start_marker = "# Copyright"
end_marker = "LICENSE-2.0"

# Walk through backend directory
target_dir = r"c:\Users\sadid\Documents\Curso IA Papers\werewolf_arena\backend\src"

print(f"Scanning {target_dir}...")

for root, dirs, files in os.walk(target_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                
                # Check if it looks like a file with the header (starts with Copyright)
                if len(lines) > 0 and start_marker in lines[0]:
                    print(f"Cleaning {path}")
                    
                    # Find end of license block
                    end_idx = -1
                    for i, line in enumerate(lines[:25]): # Look in first 25 lines
                        if end_marker in line:
                            end_idx = i
                            break
                    
                    if end_idx != -1:
                        # Keep content after the license
                        # usually there is an empty line or two
                        new_lines = lines[end_idx+1:]
                        
                        # Remove leading empty lines
                        while new_lines and not new_lines[0].strip():
                            new_lines.pop(0)
                            
                        with open(path, "w", encoding="utf-8") as f:
                            f.writelines(new_lines)
                    else:
                        print(f"Skipped {path}: Start marker found but end marker missing.")
            except Exception as e:
                print(f"Error processing {path}: {e}")

print("Cleanup complete.")
