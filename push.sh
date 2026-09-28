#!/bin/bash
# Wiki push 腳本 — 包含 MkDocs build + GitHub Pages 發布
set -e

export PATH="/c/Program Files/GitHub CLI:$PATH"

WIKI="/c/MUWORK/GAME/MAPLESOTRY/wiki"
cd "$WIKI"

echo "================================================"
echo "  MapleStory v83 Wiki - GitHub Pages 部署"
echo "================================================"
echo ""

echo "=== 1. MkDocs build (本機預覽版本) ==="
mkdocs build --strict
echo ""

echo "=== 2. git init ==="
if [ ! -d ".git" ]; then
    git init -b main
fi
git config user.name "e78-png"
git config user.email "e78-png@users.noreply.github.com"
echo ""

echo "=== 3. git add ==="
git add .
echo ""

echo "=== 4. git status (將 commit 的檔案) ==="
git status --short | head -30
echo "  ... (更多檔案)"
echo ""

echo "=== 5. git commit ==="
git commit -m "Initial commit: MapleStory v83 dev Wiki (with GitHub Pages)

Wiki 內容:
- 51 markdown files / ~580 KB
- 17 章節 / 9 大類
- 47 wiki pages covering client analysis, UI classes, protocol, tools
- 6 MapleStory core functions decompiled pseudocode
- 54,357 functions / 1,262 strings from v83.idb analysis
- 13 CUIToolTip addresses from angel/RaGEZONE
- 24 IDC rename rules from diamondo25/RaGEZONE
- All third-party sources cited in docs/REFERENCES.md

GitHub Pages:
- MkDocs build 已驗證(2 秒 / 0 errors)
- 17 章節 / 912 indexed docs / 搜尋可用
- License: CC BY 4.0 (text) + MIT (code)
"
echo ""

echo "=== 6. gh repo create (public) ==="
gh repo create maplestory-v83-dev-wiki \
  --public \
  --description "MapleStory v83 二次開發知識庫 — 整合 IDA Pro 分析、UI classes、protocol dispatchers、kaentake hook 工具" \
  --source=. \
  --remote=origin
echo ""

echo "=== 7. git push ==="
git push -u origin main
echo ""

echo "=== 8. mkdocs gh-deploy (GitHub Pages) ==="
mkdocs gh-deploy --force --strict
echo ""

echo "================================================"
echo "  完成!"
echo "================================================"
echo ""
echo "Wiki URL: https://e78-png.github.io/maplestory-v83-dev-wiki/"
echo ""
