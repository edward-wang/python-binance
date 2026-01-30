import ast
import os
import textwrap
import difflib
from collections import defaultdict

def get_method_source_map(filepath):
    """提取函数名到其完整源代码（含注释）的映射"""
    if not os.path.exists(filepath):
        return {}
        
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        content = "".join(lines)
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            print(f"[!] Syntax error in {filepath}: {e}")
            return {}
        
    source_map = {}
    for node in ast.walk(tree):
        # 我们只关心类里面的方法，或者顶层函数（如果是 Mixin，通常都在类里）
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # 1. 获取起始行（考虑装饰器）
            start_idx = node.lineno - 1
            if node.decorator_list:
                start_idx = min(d.lineno for d in node.decorator_list) - 1
            
            # 2. 获取结束行
            end_idx = getattr(node, "end_lineno", len(lines))
            
            # 3. 提取源代码
            func_lines = lines[start_idx:end_idx]
            func_source = "".join(func_lines)
            
            # 4. 标准化处理
            # 移除整体缩进，并去掉前后的空白字符
            normalized_source = textwrap.dedent(func_source).strip()
            
            source_map[node.name] = {
                'source': normalized_source,
                'file': filepath,
                'start_line': start_idx + 1,
                'end_line': end_idx
            }
    return source_map

def verify_full_consistency(original_file, new_paths):
    print(f"[*] Loading original functions from {original_file}...")
    original_map = get_method_source_map(original_file)
    
    new_map = {}
    duplicates = defaultdict(list)
    
    print(f"[*] Loading new functions from components...")
    for path in new_paths:
        if os.path.isfile(path):
            if "_core_typing.py" in path: continue
            comp_map = get_method_source_map(path)
            for name, data in comp_map.items():
                if name in new_map:
                    duplicates[name].append(data['file'])
                    if new_map[name]['file'] not in duplicates[name]:
                        duplicates[name].append(new_map[name]['file'])
                new_map[name] = data
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for f in files:
                    if f.endswith('.py') and not f.startswith('__'):
                        if "_core_typing.py" in f: continue
                        full_path = os.path.join(root, f)
                        comp_map = get_method_source_map(full_path)
                        for name, data in comp_map.items():
                            if name in new_map:
                                duplicates[name].append(data['file'])
                                if new_map[name]['file'] not in duplicates[name]:
                                    duplicates[name].append(new_map[name]['file'])
                            new_map[name] = data

    # 1. 检查遗漏
    missing = []
    for name in original_map:
        if name.startswith('__'): continue
        if name not in new_map:
            missing.append(name)

    # 2. 检查多余
    extra = []
    for name in new_map:
        if name.startswith('__'): continue
        if name not in original_map:
            extra.append(name)

    # 3. 检查重复
    if duplicates:
        print(f"\n[!] DUPLICATE METHODS FOUND:")
        for name, files in duplicates.items():
            print(f"  - {name}: found in {', '.join(files)}")

    # 4. 检查内容一致性
    mismatches = []
    perfect_matches = 0
    
    for name in original_map:
        if name.startswith('__') or name in missing:
            continue
            
        orig_source = original_map[name]['source']
        new_source = new_map[name]['source']
        
        if orig_source != new_source:
            mismatches.append(name)
        else:
            perfect_matches += 1

    # 报告结果
    print(f"\n{'='*60}")
    print(f"VERIFICATION REPORT")
    print(f"{'='*60}")
    print(f"Original Functions: {len([m for m in original_map if not m.startswith('__')])}")
    print(f"New Functions:      {len([m for m in new_map if not m.startswith('__')])}")
    print(f"Perfect Matches:    {perfect_matches}")
    print(f"Missing:            {len(missing)}")
    print(f"Extra:              {len(extra)}")
    print(f"Content Mismatches: {len(mismatches)}")
    print(f"{'='*60}")

    if missing:
        print(f"\n[!] MISSING METHODS:")
        for m in sorted(missing):
            print(f"  - {m} (Original line {original_map[m]['start_line']})")

    if extra:
        print(f"\n[?] EXTRA METHODS (New but not in original):")
        for m in sorted(extra):
            print(f"  - {m} (in {new_map[m]['file']})")

    if mismatches:
        print(f"\n[X] CONTENT MISMATCHES (Logic or Comments differ):")
        for m in mismatches:
            print(f"\n--- Diff for '{m}' ---")
            orig = original_map[m]['source'].splitlines()
            new = new_map[m]['source'].splitlines()
            diff = difflib.unified_diff(orig, new, fromfile='Original', tofile='New', lineterm='')
            for line in diff:
                print(line)

if __name__ == "__main__":
    ORIG_FILE = "binance/async_client.py"
    NEW_PATHS = ["binance/async_client_core.py", "binance/async_mixins"]
    
    if not os.path.exists(ORIG_FILE):
        print(f"Error: Original file {ORIG_FILE} not found.")
    else:
        verify_full_consistency(ORIG_FILE, NEW_PATHS)

