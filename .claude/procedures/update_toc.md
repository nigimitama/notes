# _toc.yml 更新手順

このドキュメントは、Jupyter Bookの目次ファイル (`book/_toc.yml`) を実際のノートブックファイル構造に合わせて更新する手順を記載しています。

## 概要

`book/` ディレクトリ内の `.ipynb` ファイルと `book/_toc.yml` の内容を同期させ、すべてのノートブックが正しく目次に登録されていることを確認します。

## 実行タイミング

以下のような場合に実行してください：

- 新しいノートブックファイルを追加した後
- ノートブックファイルを移動・リネームした後
- ディレクトリ構造を変更した後
- 定期的なメンテナンス（月1回程度推奨）

## 前提条件

- Python 3.10以上がインストールされていること
- PyYAMLパッケージがインストールされていること (`pip install pyyaml`)
- 作業ディレクトリが `/home/mitama/notes` であること

## 手順

### Step 1: 差分確認スクリプトの作成

以下のPythonスクリプトを `/tmp/compare_toc.py` として保存します：

```python
import os
import yaml

# _toc.ymlを読み込む
with open('/home/mitama/notes/book/_toc.yml', 'r') as f:
    toc = yaml.safe_load(f)

# _toc.ymlに登録されているファイルを抽出
def extract_files(obj, prefix='book/'):
    files = []
    if isinstance(obj, dict):
        if 'file' in obj:
            files.append(prefix + obj['file'] + '.ipynb')
        if 'sections' in obj:
            for section in obj['sections']:
                files.extend(extract_files(section, prefix))
    elif isinstance(obj, list):
        for item in obj:
            files.extend(extract_files(item, prefix))
    return files

toc_files = set()
if 'parts' in toc:
    for part in toc['parts']:
        if 'chapters' in part:
            for chapter in part['chapters']:
                toc_files.update(extract_files(chapter))

# 実際のファイルを取得
actual_files = set()
for root, dirs, files in os.walk('/home/mitama/notes/book'):
    # .ipynb_checkpointsを除外
    if '.ipynb_checkpoints' in root:
        continue
    for file in files:
        if file.endswith('.ipynb'):
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, '/home/mitama/notes')
            actual_files.add(rel_path)

# 差分を計算
missing_in_toc = sorted(actual_files - toc_files)
missing_in_actual = sorted(toc_files - actual_files)

print("=== _toc.ymlに存在しないファイル ===")
if missing_in_toc:
    for f in missing_in_toc:
        print(f)
    print(f"\n合計: {len(missing_in_toc)}個")
else:
    print("なし")

print("\n=== 実際のファイルに存在しない_toc.ymlのエントリ ===")
if missing_in_actual:
    for f in missing_in_actual:
        print(f)
    print(f"\n合計: {len(missing_in_actual)}個")
else:
    print("なし")

# 要約
if not missing_in_toc and not missing_in_actual:
    print("\n✅ _toc.ymlと実際のファイル構造は完全に同期しています")
else:
    print(f"\n⚠️  同期が必要です: {len(missing_in_toc)}個追加, {len(missing_in_actual)}個削除")
```

### Step 2: 差分の確認

```bash
cd /home/mitama/notes
python3 /tmp/compare_toc.py
```

出力例：
```
=== _toc.ymlに存在しないファイル ===
book/new_section/new_notebook.ipynb
book/statistics/new_topic.ipynb

合計: 2個

=== 実際のファイルに存在しない_toc.ymlのエントリ ===
book/old_section/deleted_notebook.ipynb

合計: 1個

⚠️  同期が必要です: 2個追加, 1個削除
```

### Step 3: _toc.ymlの編集

差分確認の結果に基づいて、`book/_toc.yml` を編集します。

#### 3.1 不要なエントリの削除

実際に存在しないファイルへの参照を削除します。

**例：**
```yaml
# 削除前
- file: old_section/deleted_notebook

# 削除後（エントリごと削除）
```

#### 3.2 新しいファイルの追加

実際に存在するが _toc.yml に登録されていないファイルを追加します。

**ファイル階層の対応関係：**

```yaml
# 単一ファイルの場合
- file: section_name/notebook_name

# index.ipynb を持つセクションの場合
- file: section_name/index
  sections:
    - file: section_name/sub_notebook1
    - file: section_name/sub_notebook2

# ネストされたセクションの場合
- file: section_name/index
  sections:
    - file: section_name/subsection/index
      sections:
        - file: section_name/subsection/notebook1
        - file: section_name/subsection/notebook2
```

**注意事項：**

1. ファイルパスは `book/` からの相対パスで、拡張子 `.ipynb` は**省略**します
2. インデントはスペース2個を使用します
3. 階層構造は論理的なグループ分けに従います
4. `index.ipynb` はセクションのトップページとして使用します

### Step 4: 構文チェック

編集後、YAMLの構文が正しいかチェックします：

```bash
python3 -c "import yaml; yaml.safe_load(open('book/_toc.yml'))" && echo "✅ YAML構文OK" || echo "❌ YAML構文エラー"
```

### Step 5: 再度差分確認

```bash
python3 /tmp/compare_toc.py
```

すべての差分が解消されていることを確認します：

```
=== _toc.ymlに存在しないファイル ===
なし

=== 実際のファイルに存在しない_toc.ymlのエントリ ===
なし

✅ _toc.ymlと実際のファイル構造は完全に同期しています
```

### Step 6: Jupyter Bookのビルドテスト

最終確認として、Jupyter Bookが正しくビルドできるかテストします：

```bash
cd /home/mitama/notes
jupyter-book build book --builder linkcheck 2>&1 | head -100
```

エラーがなく、すべてのファイルが正しく読み込まれることを確認します。

## よくある問題と対処法

### 問題1: ファイルパスの不一致

**症状：** ファイルは存在するのに「存在しない」と表示される

**原因：** _toc.yml のパスが間違っている（例：`financial_economics/` と `economics/financial_economics/`）

**対処法：**
1. 実際のファイルパスを確認：`find book -name "filename.ipynb"`
2. _toc.yml のパスを実際のパスに合わせて修正

### 問題2: index.ipynb の扱い

**症状：** index.ipynb が重複または欠落している

**原因：** セクションの親ファイルとして正しく登録されていない

**対処法：**
```yaml
# 正しい例
- file: section_name/index
  sections:
    - file: section_name/child1
    - file: section_name/child2
```

### 問題3: Untitled.ipynb などの一時ファイル

**症状：** Untitled.ipynb が差分として表示される

**原因：** Jupyter で作成した一時ファイル

**対処法：**
- 一時ファイルは _toc.yml に追加**しない**
- 必要に応じて削除またはリネームする

### 問題4: .ipynb_checkpoints ディレクトリ

**症状：** checkpoints ディレクトリ内のファイルが表示される

**原因：** スクリプトのフィルタリングミス

**対処法：** 上記のスクリプトは自動的に除外するため、通常は問題なし

## 自動化（オプション）

定期的なチェックを自動化したい場合、以下のようなシェルスクリプトを作成できます：

```bash
#!/bin/bash
# check_toc.sh

cd /home/mitama/notes
python3 /tmp/compare_toc.py

if [ $? -eq 0 ]; then
    echo "✅ チェック完了"
else
    echo "❌ エラーが発生しました"
    exit 1
fi
```

## チェックリスト

更新作業完了時に以下を確認してください：

- [ ] `python3 /tmp/compare_toc.py` で差分がないことを確認
- [ ] YAML構文チェックが通ること
- [ ] `jupyter-book build` が警告なく実行できること
- [ ] 新しく追加したノートブックが適切なセクションに配置されていること
- [ ] ファイルパスに拡張子 `.ipynb` が含まれていないこと
- [ ] インデントがスペース2個で統一されていること

## 参考情報

- [Jupyter Book ドキュメント - Table of Contents](https://jupyterbook.org/en/stable/structure/toc.html)
- [YAML 構文ガイド](https://yaml.org/spec/1.2/spec.html)

## 更新履歴

- 2025-10-24: 初版作成
