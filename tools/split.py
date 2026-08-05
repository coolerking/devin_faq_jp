#!/usr/bin/env python3
"""org/faq.md を分割し、docs/ 配下に 1 問 1 ファイルで再生成する。

使い方:
    python tools/split.py        # docs/ 配下を再生成
    python tools/split.py --dry  # 検証のみ（ファイルを書かない）

前提:
    - org/faq.md が source of truth（編集の中心）
    - docs/ 配下は本スクリプトで再生成される（直接編集しない）
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC = REPO_ROOT / "org" / "faq.md"
DOCS = REPO_ROOT / "docs"

# ---------------------------------------------------------------------------
# カテゴリ定義（順序が docs 配下のディレクトリ番号と一致）
# ---------------------------------------------------------------------------

CATEGORIES: list[tuple[str, str, str]] = [
    # (dir_name, jp_title, description)
    ("01-introduction", "Devin入門（What/Who）",
     "Devin の概要・対象者・前提知識・関連ドキュメント・競合"),
    ("02-pricing", "料金・プラン",
     "Devin の料金体系、Windsurf プランとの関係"),
    ("03-basic-operations", "基本操作・セッション",
     "Ask Devin / Session の違い、状態判定、粒度、フルスクラッチ手順"),
    ("04-github-scm", "GitHub・SCM連携",
     "GitHub 等 SCM 連携、権限、Issue/Kanban、clone 失敗、組織リソース移行"),
    ("05-ide-cli", "IDE・エディタ・CLI",
     "Windsurf / VSCode / Copilot / Devin for Terminal の関係と使い分け"),
    ("06-commands-skills", "コマンド・スキル",
     "Skill / Slash Command / カスタムコマンドの作成方法と使い分け"),
    ("07-devin-resources", "Devinリソース",
     "Machine Configuration / Playbook / Knowledge / Wiki / Schedule"),
    ("08-secrets-api", "Secrets・API",
     "Secrets スコープ・API Key・Legacy 表記"),
    ("09-multi-session-repo", "マルチセッション・複数リポ",
     "並行セッションのスコープ、複数リポを 1 セッションで扱う方法"),
    ("10-database-test-quality", "DB・テスト・品質・Review",
     "DB 運用、テスト戦略、TDD、Test Mode、Review タブ"),
    ("11-data-docs", "データ入出力・ドキュメント理解",
     "入出力可能データ、図/表の理解、機微情報、大量データ"),
    ("12-security-governance", "セキュリティ・監査・ガバナンス",
     "データ保管、削除、監査対応、セッション可視性"),
    ("13-cloud-infra", "クラウド連携・インフラ",
     "AWS 連携、VPC、認証情報の取扱い"),
    ("14-external-pm", "外部連携（Slack・PM）",
     "Slack、Asana、Backlog、PM ツール連携"),
    ("15-organization-ops", "組織展開・分析",
     "プロセス統合、標準化、マルチエージェント、生産性計測"),
    ("16-session-recovery", "セッション停止・復旧",
     "Sleep / Usage Settings / 再開手順"),
]

# ---------------------------------------------------------------------------
# Q番号 → (カテゴリディレクトリ名, slug)
# ---------------------------------------------------------------------------

QMAP: dict[int, tuple[str, str]] = {
    1:  ("01-introduction", "devin-overview"),
    2:  ("01-introduction", "devin-ai-model"),
    3:  ("01-introduction", "target-users"),
    4:  ("01-introduction", "required-knowledge"),
    5:  ("01-introduction", "getting-started-docs"),
    6:  ("01-introduction", "competitors"),
    7:  ("02-pricing", "devin-pricing"),
    8:  ("03-basic-operations", "ask-vs-session"),
    9:  ("03-basic-operations", "session-status"),
    10: ("03-basic-operations", "session-granularity"),
    11: ("03-basic-operations", "fullscratch-flow"),
    12: ("04-github-scm", "scm-prerequisite"),
    13: ("04-github-scm", "developer-git-knowledge"),
    14: ("04-github-scm", "developer-vs-devin-github"),
    15: ("04-github-scm", "github-permissions"),
    16: ("04-github-scm", "issue-as-task"),
    17: ("04-github-scm", "kanban"),
    18: ("05-ide-cli", "windsurf-vs-vscode"),
    19: ("05-ide-cli", "vscode-copilot-bundled"),
    20: ("05-ide-cli", "copilot-coexistence"),
    21: ("05-ide-cli", "beginner-fitness"),
    22: ("06-commands-skills", "skills-existence"),
    23: ("06-commands-skills", "skills-creation"),
    24: ("06-commands-skills", "slash-commands"),
    25: ("06-commands-skills", "slash-vs-skill"),
    26: ("07-devin-resources", "machine-config"),
    27: ("07-devin-resources", "playbook"),
    28: ("07-devin-resources", "resource-comparison"),
    29: ("07-devin-resources", "devin-wiki"),
    30: ("07-devin-resources", "schedule"),
    31: ("08-secrets-api", "secrets"),
    32: ("08-secrets-api", "api-key"),
    33: ("08-secrets-api", "api-legacy"),
    34: ("09-multi-session-repo", "parallel-sessions"),
    35: ("09-multi-session-repo", "multi-repo"),
    36: ("10-database-test-quality", "database"),
    37: ("10-database-test-quality", "db-fixture-reset"),
    38: ("10-database-test-quality", "integration-test-env"),
    39: ("10-database-test-quality", "test-mode"),
    40: ("10-database-test-quality", "test-types"),
    41: ("10-database-test-quality", "internal-network-test"),
    42: ("10-database-test-quality", "tdd"),
    43: ("10-database-test-quality", "review-tab"),
    44: ("10-database-test-quality", "faq-review-procedure"),
    45: ("11-data-docs", "input-data-types"),
    46: ("11-data-docs", "output-data-types"),
    47: ("11-data-docs", "image-pdf-diagrams"),
    48: ("11-data-docs", "input-data-cautions"),
    49: ("11-data-docs", "bulk-data-handling"),
    50: ("12-security-governance", "data-retention"),
    51: ("12-security-governance", "terminate-archive-delete"),
    52: ("12-security-governance", "org-admin-visibility"),
    53: ("12-security-governance", "compliance-audit"),
    54: ("13-cloud-infra", "aws-credentials"),
    55: ("13-cloud-infra", "aws-vpc"),
    56: ("14-external-pm", "multi-org-slack"),
    57: ("14-external-pm", "slack-workspace-strategy"),
    58: ("14-external-pm", "asana-backlog"),
    59: ("15-organization-ops", "existing-process-integration"),
    60: ("15-organization-ops", "standards-docs-auto-resource"),
    61: ("15-organization-ops", "internal-standards-example"),
    62: ("15-organization-ops", "multi-agent-collaboration"),
    63: ("15-organization-ops", "productivity-metrics"),
    64: ("04-github-scm", "clone-failures"),
    65: ("16-session-recovery", "session-sleep"),
    66: ("12-security-governance", "session-visibility-teams"),
    67: ("04-github-scm", "personal-vs-org-resources"),
    68: ("04-github-scm", "clone-without-wiki"),
    69: ("05-ide-cli", "devin-cli-modes"),
    70: ("02-pricing", "devin-vs-windsurf-plans"),
    71: ("02-pricing", "personal-pro-email-limit"),
}

assert len(QMAP) == 71, f"QMAP has {len(QMAP)} entries (expected 71)"
for qno, (cat, _) in QMAP.items():
    assert any(c[0] == cat for c in CATEGORIES), f"Q{qno}: category {cat!r} not in CATEGORIES"


# ---------------------------------------------------------------------------
# データ構造
# ---------------------------------------------------------------------------

@dataclass
class Question:
    qno: int
    title: str
    body: str            # 本文（メタ行を含む。`## QN.` 行や `<a id>` 行は除外済）
    meta_line: str       # `> **メタ**: ...` 行そのまま
    last_verified: str   # YYYY-MM-DD
    sources: list[str]
    estimated: bool
    related: list[int]   # 本文中で参照している他のQ番号

    @property
    def slug(self) -> str:
        return QMAP[self.qno][1]

    @property
    def category_dir(self) -> str:
        return QMAP[self.qno][0]

    @property
    def filename(self) -> str:
        return f"q{self.qno:02d}-{self.slug}.md"

    @property
    def relpath_from_docs(self) -> str:
        return f"{self.category_dir}/{self.filename}"


# ---------------------------------------------------------------------------
# パーサ
# ---------------------------------------------------------------------------

ANCHOR_RE = re.compile(r'^<a id="q(\d+)"></a>\s*$', re.MULTILINE)
H2_Q_RE = re.compile(r'^## Q(\d+)\.\s+(.*)$', re.MULTILINE)
META_RE = re.compile(r'^> \*\*メタ\*\*\s*:\s*(.*)$', re.MULTILINE)
XREF_RE = re.compile(r'\[Q(\d+)([^\]]*?)\]\(#q(\d+)\)')


def parse_meta(meta_body: str) -> tuple[str, list[str], bool]:
    """`最終確認日 YYYY/M/D ｜ 根拠 URL ｜ 推定あり/なし` を分解。"""
    parts = [p.strip() for p in re.split(r'[｜|]', meta_body)]
    last_verified = ""
    sources: list[str] = []
    estimated = False
    for p in parts:
        if p.startswith("最終確認日"):
            m = re.search(r'(\d{4})[/-](\d{1,2})[/-](\d{1,2})', p)
            if m:
                y, mth, d = m.groups()
                last_verified = f"{y}-{int(mth):02d}-{int(d):02d}"
        elif p.startswith("根拠"):
            urls = re.findall(r'https?://\S+', p)
            sources.extend(urls)
        elif p.startswith("推定"):
            if "あり" in p:
                estimated = True
            elif "なし" in p:
                estimated = False
    return last_verified, sources, estimated


def parse_faq(text: str) -> list[Question]:
    """faq.md を Question のリストに分解。

    各 Q ブロックは `<a id="qN"></a>` 行で始まり、次の `<a id="qM"></a>` 行の
    直前で終わる。
    """
    anchors = [(int(m.group(1)), m.start()) for m in ANCHOR_RE.finditer(text)]
    if not anchors:
        raise SystemExit("anchor `<a id=\"qN\"></a>` が見つからない")

    questions: list[Question] = []
    for i, (qno, start) in enumerate(anchors):
        end = anchors[i + 1][1] if i + 1 < len(anchors) else len(text)
        block = text[start:end]

        # ヘッダ抽出: `<a id>` の次の `## QN. Title`
        h2_match = H2_Q_RE.search(block)
        if not h2_match:
            raise SystemExit(f"Q{qno}: `## Q{qno}.` ヘッダが見つからない")
        title = h2_match.group(2).strip()
        body_start = h2_match.end() + 1  # 改行を飛ばす

        body = block[body_start:].rstrip() + "\n"

        # メタ行
        meta_match = META_RE.search(body)
        if not meta_match:
            raise SystemExit(f"Q{qno}: メタ行が見つからない")
        meta_body = meta_match.group(1)
        last_verified, sources, estimated = parse_meta(meta_body)
        meta_line = meta_match.group(0)

        # クロス参照対象 Q 番号
        related = sorted({int(m.group(1)) for m in XREF_RE.finditer(body)
                          if int(m.group(1)) != qno})

        questions.append(Question(
            qno=qno,
            title=title,
            body=body,
            meta_line=meta_line,
            last_verified=last_verified,
            sources=sources,
            estimated=estimated,
            related=related,
        ))

    if len(questions) != 70:
        raise SystemExit(f"Q数が 70 でない（{len(questions)}）")

    return questions


# ---------------------------------------------------------------------------
# クロス参照書き換え
# ---------------------------------------------------------------------------

def rewrite_xrefs(body: str, current_qno: int) -> str:
    """`[QN](#qN)` を相対パスリンクに書き換える。"""

    cur_cat = QMAP[current_qno][0]

    def replacer(m: re.Match[str]) -> str:
        target_qno = int(m.group(1))
        suffix = m.group(2)  # `[Q7. ...]` の `. ...` 部分など
        if target_qno not in QMAP:
            return m.group(0)
        target_cat, target_slug = QMAP[target_qno]
        target_filename = f"q{target_qno:02d}-{target_slug}.md"
        if target_cat == cur_cat:
            relpath = target_filename
        else:
            relpath = f"../{target_cat}/{target_filename}"
        return f"[Q{target_qno}{suffix}]({relpath})"

    return XREF_RE.sub(replacer, body)


# ---------------------------------------------------------------------------
# 出力
# ---------------------------------------------------------------------------

def make_question_md(q: Question, prev_q: Question | None,
                     next_q: Question | None,
                     all_qs: dict[int, Question]) -> str:
    """1問分の Markdown を組み立てる。"""

    # frontmatter
    sources_yaml = "\n".join(f"  - {url}" for url in q.sources) or "  []"
    related_yaml = ", ".join(str(r) for r in q.related)

    fm_lines = [
        "---",
        f"qno: {q.qno}",
        f'title: "{q.title.replace(chr(34), chr(92) + chr(34))}"',
        f"category: {q.category_dir}",
        f'last_verified: "{q.last_verified}"',
        "sources:",
        *(f"  - {url}" for url in q.sources),
        f"related: [{related_yaml}]" if q.related else "related: []",
        f"estimated: {str(q.estimated).lower()}",
        "---",
        "",
    ]
    if not q.sources:
        # remove the empty `sources:` block items: keep `sources: []`
        fm_lines = [
            "---",
            f"qno: {q.qno}",
            f'title: "{q.title.replace(chr(34), chr(92) + chr(34))}"',
            f"category: {q.category_dir}",
            f'last_verified: "{q.last_verified}"',
            "sources: []",
            f"related: [{related_yaml}]" if q.related else "related: []",
            f"estimated: {str(q.estimated).lower()}",
            "---",
            "",
        ]

    # H1 + breadcrumb
    cat_label = next(c[1] for c in CATEGORIES if c[0] == q.category_dir)
    h1 = f"# Q{q.qno}. {q.title}"
    breadcrumb = (
        f"📚 [トップ索引](../../README.md) ｜ "
        f"[カテゴリ索引: {cat_label}](README.md)"
    )

    # 本文（クロス参照書き換え済）
    body_rewritten = rewrite_xrefs(q.body, q.qno)
    # 末尾の Q 区切り `---` は重複するので除去
    body_rewritten = re.sub(r'\n+---\s*$', '\n', body_rewritten.rstrip()) + "\n"
    # メタ行はそのまま冒頭に残す（既に body 内にある）。重複させない。
    # ナビゲーション
    nav_parts: list[str] = []
    if prev_q is not None:
        prev_path = relative_path(q.category_dir, prev_q)
        nav_parts.append(f"[← Q{prev_q.qno}. {prev_q.title}]({prev_path})")
    if next_q is not None:
        next_path = relative_path(q.category_dir, next_q)
        nav_parts.append(f"[Q{next_q.qno}. {next_q.title} →]({next_path})")
    nav_line = " ｜ ".join(nav_parts) if nav_parts else ""

    # 関連 FAQ セクション（本文に既に含まれていない場合は追加しない）
    # → 既存本文に「関連 FAQ」のクロスリンクが書かれている場合が多いので、
    #   末尾に自動 navigation のみ追加する方針。

    out_parts = [
        "\n".join(fm_lines),
        h1,
        "",
        breadcrumb,
        "",
        "---",
        "",
        body_rewritten.rstrip(),
        "",
    ]
    if nav_line:
        out_parts.extend([
            "---",
            "",
            nav_line,
            "",
        ])

    return "\n".join(out_parts)


def relative_path(from_cat: str, to_q: Question) -> str:
    if to_q.category_dir == from_cat:
        return to_q.filename
    return f"../{to_q.category_dir}/{to_q.filename}"


# ---------------------------------------------------------------------------
# 索引生成
# ---------------------------------------------------------------------------

def make_top_readme(questions: list[Question]) -> str:
    by_cat: dict[str, list[Question]] = {c[0]: [] for c in CATEGORIES}
    for q in questions:
        by_cat[q.category_dir].append(q)

    last_verified_max = max((q.last_verified for q in questions if q.last_verified),
                            default="")

    lines: list[str] = []
    lines.append("# Devin FAQ JP")
    lines.append("")
    lines.append("日本語で記述された Devin に関する FAQ集。社内向けに作成された問答を Public 化したもの。")
    lines.append("")
    lines.append("| | |")
    lines.append("|---|---|")
    lines.append(f"| **総質問数** | {len(questions)}問 |")
    lines.append(f"| **最終確認** | {last_verified_max} |")
    lines.append("| **対応 Devin バージョン** | 2026年4月時点（2026/4/16 料金改定反映） |")
    lines.append("| **対象読者** | Devin 検討〜エンタープライズ管理者 |")
    lines.append("| **記述方針** | 結論→詳細→表→具体例→注意→まとめ（核心） |")
    lines.append("")
    lines.append("> ⚠️ **免責**: 公式情報は変動するため、最新は [docs.devin.ai](https://docs.devin.ai/) を参照。")
    lines.append("")
    lines.append("---")
    lines.append("")

    # カテゴリ別索引（サマリ）
    lines.append("## カテゴリ別索引")
    lines.append("")
    lines.append("| # | カテゴリ | 質問数 | リンク |")
    lines.append("|---|---|---|---|")
    for i, (cat_dir, jp_title, _desc) in enumerate(CATEGORIES, 1):
        qs = by_cat[cat_dir]
        lines.append(
            f"| {i:02d} | {jp_title} | {len(qs)} | "
            f"[docs/{cat_dir}/](docs/{cat_dir}/README.md) |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")

    # 番号順 全Q索引
    lines.append("## 番号順 全Q索引")
    lines.append("")
    for q in sorted(questions, key=lambda x: x.qno):
        lines.append(f"- [Q{q.qno}. {q.title}](docs/{q.relpath_from_docs})")
    lines.append("")
    lines.append("---")
    lines.append("")

    # カテゴリ別 全Q索引
    lines.append("## カテゴリ別 全Q索引")
    lines.append("")
    for i, (cat_dir, jp_title, desc) in enumerate(CATEGORIES, 1):
        qs = by_cat[cat_dir]
        if not qs:
            continue
        lines.append(f"### {i:02d}. {jp_title}")
        lines.append("")
        lines.append(desc)
        lines.append("")
        for q in sorted(qs, key=lambda x: x.qno):
            lines.append(f"- [Q{q.qno}. {q.title}](docs/{q.relpath_from_docs})")
        lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 編集について")
    lines.append("")
    lines.append("- 編集元のモノリス `org/faq.md` は VM 内のみ参照可能（`.gitignore` 済）")
    lines.append("- `docs/` 配下は `tools/split.py` が自動生成。直接編集しない")
    lines.append("- 新規 Q 追加手順は [CONTRIBUTING.md](CONTRIBUTING.md) 参照")
    lines.append("")

    return "\n".join(lines) + "\n"


def make_category_readme(cat_dir: str, jp_title: str, desc: str,
                         qs: list[Question]) -> str:
    cat_idx = next(i for i, c in enumerate(CATEGORIES, 1) if c[0] == cat_dir)
    lines: list[str] = []
    lines.append(f"# {cat_idx:02d}. {jp_title}")
    lines.append("")
    lines.append(desc)
    lines.append("")
    lines.append("## 含まれる質問")
    lines.append("")
    for q in sorted(qs, key=lambda x: x.qno):
        lines.append(f"- [Q{q.qno}. {q.title}]({q.filename})")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("[← トップ索引](../../README.md)")
    lines.append("")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true", help="ファイルを書かず検証のみ")
    args = ap.parse_args()

    if not SRC.exists():
        print(f"ERROR: {SRC} が存在しない", file=sys.stderr)
        return 1

    text = SRC.read_text(encoding="utf-8")
    questions = parse_faq(text)
    print(f"parsed: {len(questions)} questions")

    # Q番号順
    questions.sort(key=lambda q: q.qno)

    # 既存 docs/ クリア（README/ サブディレクトリだけ）
    if not args.dry and DOCS.exists():
        for p in DOCS.rglob("*.md"):
            p.unlink()

    # 各カテゴリディレクトリ作成
    for cat_dir, _, _ in CATEGORIES:
        (DOCS / cat_dir).mkdir(parents=True, exist_ok=True)

    by_cat: dict[str, list[Question]] = {c[0]: [] for c in CATEGORIES}
    for q in questions:
        by_cat[q.category_dir].append(q)

    qmap_dict = {q.qno: q for q in questions}

    # 各 Q ファイル
    for q in questions:
        prev_q = qmap_dict.get(q.qno - 1)
        next_q = qmap_dict.get(q.qno + 1)
        out_path = DOCS / q.category_dir / q.filename
        content = make_question_md(q, prev_q, next_q, qmap_dict)
        if not args.dry:
            out_path.write_text(content, encoding="utf-8")
        print(f"  wrote {out_path.relative_to(REPO_ROOT)}")

    # カテゴリ README
    for cat_dir, jp_title, desc in CATEGORIES:
        qs = by_cat[cat_dir]
        if not qs:
            continue
        cat_readme = DOCS / cat_dir / "README.md"
        if not args.dry:
            cat_readme.write_text(
                make_category_readme(cat_dir, jp_title, desc, qs),
                encoding="utf-8",
            )

    # トップ README
    top_readme = REPO_ROOT / "README.md"
    if not args.dry:
        top_readme.write_text(make_top_readme(questions), encoding="utf-8")

    print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
