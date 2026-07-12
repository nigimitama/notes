---
allowed-tools: Bash(python3 /tmp/compare_toc.py), Bash(python3 -c:*), Bash(git add:*), Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git commit:*), Read, Edit
description: myst.yml の toc を更新してコミットする
---

## Context

- Current git status: !`git status`
- Current git diff: !`git diff HEAD -- book/myst.yml`
- Recent commits: !`git log --oneline -10`

## Your task

以下の手順を順番に実行してください。

### Step 1: 差分確認

以下のスクリプトを `/tmp/compare_toc.py` に保存して実行し、`book/myst.yml` の `project.toc` と実際のファイル構造の差分を確認してください。

```python
import os
import yaml

with open('/home/mitama/notes/book/myst.yml', 'r') as f:
    config = yaml.safe_load(f)

def extract_files(obj, prefix='book/'):
    files = []
    if isinstance(obj, dict):
        if 'file' in obj and obj['file'].endswith('.ipynb'):
            files.append(prefix + obj['file'])
        if 'children' in obj:
            for child in obj['children']:
                files.extend(extract_files(child, prefix))
    elif isinstance(obj, list):
        for item in obj:
            files.extend(extract_files(item, prefix))
    return files

toc_files = set(extract_files(config['project']['toc']))

actual_files = set()
for root, dirs, files in os.walk('/home/mitama/notes/book'):
    if '.ipynb_checkpoints' in root or '/_build/' in root or root.endswith('/_build'):
        continue
    for file in files:
        if file.endswith('.ipynb'):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, '/home/mitama/notes')
            actual_files.add(rel_path)

missing_in_toc = sorted(actual_files - toc_files)
missing_in_actual = sorted(toc_files - actual_files)

print("=== myst.yml の toc に存在しないファイル ===")
if missing_in_toc:
    for f in missing_in_toc:
        print(f)
    print(f"\n合計: {len(missing_in_toc)}個")
else:
    print("なし")

print("\n=== 実際のファイルに存在しない toc のエントリ ===")
if missing_in_actual:
    for f in missing_in_actual:
        print(f)
    print(f"\n合計: {len(missing_in_actual)}個")
else:
    print("なし")

if not missing_in_toc and not missing_in_actual:
    print("\n✅ myst.yml の toc と実際のファイル構造は完全に同期しています")
else:
    print(f"\n⚠️  同期が必要です: {len(missing_in_toc)}個追加, {len(missing_in_actual)}個削除")
```

### Step 2: myst.yml の編集

差分がある場合は `book/myst.yml` の `project.toc` を編集してください。

- **不要なエントリの削除**: 実際に存在しないファイルへの参照を削除
- **新しいファイルの追加**: 実際に存在するが toc に未登録のファイルを追加

ファイル追加時のルール:
- パスは `book/` からの相対パスで拡張子 `.ipynb` を**含める**
- インデントはスペース2個
- `index.ipynb` はセクションのトップページとして `children:` の親にする
- パート（大見出し）は `- title: 名前` + `children:` で表す
- Untitled.ipynb などの一時ファイルは追加しない

```yaml
# 単一ファイル
- file: section_name/notebook_name.ipynb

# index.ipynb を持つセクション
- file: section_name/index.ipynb
  children:
    - file: section_name/sub_notebook1.ipynb
    - file: section_name/sub_notebook2.ipynb
```

差分がない場合はStep 3へスキップしてください。

### Step 3: 構文チェックと再確認

```bash
python3 -c "import yaml; yaml.safe_load(open('book/myst.yml'))" && echo "✅ YAML構文OK"
```

再度 `/tmp/compare_toc.py` を実行して差分が解消されていることを確認してください。

### Step 4: コミット

`book/myst.yml` に変更があった場合のみコミットしてください。

- 変更内容を分析してコミットメッセージを生成する
- 追加・削除されたノートブックのパスをコミットメッセージに含める
- `git add book/myst.yml` でステージしてからコミットする
- 変更がなかった場合は「同期済みのため、コミットは不要です」と報告して終了する
