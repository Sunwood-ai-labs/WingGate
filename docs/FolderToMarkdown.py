import os

def is_excluded(path, exclude_patterns):
    """
    パスが除外パターンに一致するかどうかをチェックします。
    """
    return any(pattern in path for pattern in exclude_patterns)

def generate_markdown_for_folder(folder_path, exclude_patterns=[]):
    """
    指定されたフォルダのファイル構造と内容をマークダウン形式で生成します。
    """
    markdown_content = ""
    base_level = folder_path.count(os.sep)
    for root, dirs, files in os.walk(folder_path, topdown=True):
        if is_excluded(root, exclude_patterns):
            dirs[:] = []  # Don't walk into excluded directories
            continue
        level = root.count(os.sep) - base_level + 1
        header_level = '#' * (level + 1)
        relative_path = os.path.relpath(root, folder_path)
        markdown_content += f"{header_level} {relative_path}\n\n"
        for f in files:
            file_path = os.path.join(root, f)
            if is_excluded(file_path, exclude_patterns):
                continue
            relative_file_path = os.path.relpath(file_path, folder_path)
            try:
                with open(file_path, 'r', encoding='utf-8') as file_content:
                    content = file_content.read().strip()
                    markdown_content += f"`{relative_file_path}`\n\n```plaintext\n{content}\n```\n\n"
            except Exception as e:
                markdown_content += f"`{relative_file_path}` - Error reading file: {e}\n\n"
    return markdown_content

def generate_markdown_for_folders(folders, exclude_patterns=[], output_file='output.md'):
    """
    複数のフォルダのマークダウン形式のファイル構造と内容を生成し、ファイルに保存します。
    """
    with open(output_file, 'w', encoding='utf-8') as md_file:
        for folder in folders:
            markdown_content = generate_markdown_for_folder(folder, exclude_patterns)
            md_file.write(markdown_content + '\n\n')

# 使用例
folders = ['./']  # 現在のディレクトリを対象に
exclude_patterns = ['.git', '__pycache__', 'LICENSE', 'output.md', 'README.md', 'docs']  # 除外するファイル/フォルダのパターン
generate_markdown_for_folders(folders, exclude_patterns=exclude_patterns, output_file='output.md')