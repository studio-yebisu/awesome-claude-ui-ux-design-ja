"""Generate the browsable guide and README from the reviewed catalog (stdlib only)."""
from html import escape
from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / 'data/catalog.json').read_text(encoding='utf-8'))
SKILLS = [x for x in DATA['entries'] if x['kind'] == 'skill']
LIBRARIES = [x for x in DATA['entries'] if x['kind'] == 'library']
CATEGORIES = [('all', 'すべて'), ('direction', '見た目・設計'), ('review', 'レビュー・改善'),
              ('interaction', '操作・動き'), ('implementation', 'コンポーネント実装'),
              ('design-system', 'デザインシステム'), ('workflow', 'デザイン連携')]


def e(value):
    return escape(str(value), quote=True)


def card(item, number):
    origin = f'元投稿 #{item["source_post_number"]}' if item['origin'] == 'source-post' else '追加調査'
    extra = ''.join(f'<a href="{e(s["url"])}">{e(s["label"])}</a>' for s in item.get('extra_sources', []))
    example = '<a class="applied" href="examples/studio-desk/index.html">作例に適用 ↗</a>' if item.get('application') == 'studio-desk' else ''
    attribute = 'data-resource' if item['kind'] == 'skill' else 'data-library'
    return f'''<article class="resource" id="{e(item['id'])}" {attribute}="{e(item['id'])}">
  <div class="resource-top"><span class="number">{number:02d}</span><span>{e(item['category_label'])}</span><span class="origin">{origin}</span></div>
  <h3>{e(item['name'])}</h3><span class="kind">{e(item['kind_label'])}</span>{example}
  <p class="headline">{e(item['headline'])}</p><p>{e(item['summary'])}</p>
  <p class="best"><strong>向いていること</strong>{e(item['best_for'])}</p>
  <div class="tags">{''.join(f'<span>{e(t)}</span>' for t in item['tags'][:4])}</div>
  <details><summary>使い方・導入・確認した原典</summary>
    <div class="details-body"><h4>必要なもの</h4><p>{e(item['requirements'])}</p>
    <h4>範囲と限界</h4><p>{e(item['limits'])}</p>
    <h4>導入例</h4><p>{e(item['install_context'])}</p><pre><code>{e(item['install'])}</code></pre>
    <p class="small">原典の導入例を紹介しています。導入コマンドは未実行です。「作例に適用」はSKILL.mdを読み、設計・実装・点検に使ったものを示します。コマンドは実行時の最新版を取得する場合があります。</p>
    <h4>依頼文のたたき台</h4><p class="brief" id="brief-{e(item['id'])}">{e(item['task_brief'])}</p>
    <button class="copy" type="button" data-copy="brief-{e(item['id'])}" aria-label="{e(item['name'])}の依頼文をコピー">依頼文をコピー <span aria-hidden="true">↗</span></button>
    <h4>ライセンス：{e(item['license'])}</h4><p>{e(item['license_note'])}</p>
    <div class="source-links"><a href="{e(item['source_url'])}">確認した{'README' if item['kind'] == 'library' else 'SKILL.md'} ↗</a><a href="{e(item['readme_url'])}">導入手順の原典 ↗</a><a href="{e(item['license_url'])}">ライセンスの根拠 ↗</a>{extra}</div>
    <p class="small revision">確認日 {e(item['verified_on'])} · commit <code>{e(item['revision'])}</code></p></div>
  </details>
  <a class="repo-link" href="{e(item['repository_url'])}">{e(item['repo'])} <span aria-hidden="true">↗</span></a>
</article>'''


def build():
    cards = '\n'.join(card(item, i + 1) for i, item in enumerate(SKILLS))
    library_cards = '\n'.join(card(item, i + 1) for i, item in enumerate(LIBRARIES))
    serial = json.dumps(SKILLS, ensure_ascii=False).replace('<', '\\u003c')
    count = len(SKILLS)
    supplement_count = sum(x['origin'] == 'supplement' for x in SKILLS)
    table_rows = '\n'.join(f'<tr><th scope="row"><a href="#{e(x["id"])}">{e(x["name"])}</a></th><td>{e(x["kind_label"])}</td><td>{e(x["best_for"])}</td></tr>' for x in DATA['entries'])
    page = f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="UI・UX向けのエージェントスキルを、用途・導入条件・原典から選ぶ日本語ガイド。スキルを適用した動く作例も掲載。">
<meta name="color-scheme" content="light"><title>{e(DATA['title'])}</title><link rel="stylesheet" href="styles.css"><script src="app.js" defer></script></head>
<body><a class="skip" href="#main">本文へ移動</a>
<header class="site-header"><a class="brand" href="#top"><span class="brand-mark" aria-hidden="true">Y</span> STUDIO YEBISU <span class="brand-sub">DESIGN GUIDES</span></a><nav aria-label="ガイドのナビゲーション"><a href="#catalog">スキルを探す</a><a href="#example">作例を見る</a><a href="{e(DATA['motion_guide'])}">モーション版 ↗</a></nav></header>
<main id="main"><section class="hero" id="top" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow">AGENT SKILLS × INTERFACE DESIGN</p><h1 id="hero-title">使いやすさを、<br>つくる道具。</h1><p class="hero-name">UI・UX エージェントスキルガイド</p><p class="intro">見た目を決める。操作を整える。実装を見直す。<br>GitHubで探して、原典を読み、実際につくる。</p><a class="primary" href="#catalog">{count}のスキル・スキル集を見る <span aria-hidden="true">↓</span></a><p class="hero-note">用途ごとに比較 · 動く作例付き · 原典確認 {e(DATA['verified_on'])}</p></div>
<div class="hero-art" aria-hidden="true"><div class="art-label">AN INTERFACE IS A CONVERSATION.</div><div class="type-ui">UI<span>→</span></div><div class="art-rule"></div><div class="type-ux">UX<span class="art-dot"></span></div><div class="art-bottom"><span>意図を、画面へ。</span><span>使う人の、その先へ。</span></div></div></section>
<section class="example-feature" id="example" aria-labelledby="example-title"><div><p class="eyebrow">READ THE SKILLS. BUILD SOMETHING.</p><h2 id="example-title">スキルから生まれた、<br>小さな制作デスク。</h2><p>調べたスキルのうち4件を適用して、制作プロジェクトを整理する「Studio Yebisu Desk」をつくりました。検索、追加・編集、状態変更、タスクの完了まで試せます。</p><a class="primary" href="examples/studio-desk/index.html">動く作例を開く <span aria-hidden="true">↗</span></a><p class="example-note">試作 / 架空のデータ / 保存はこのブラウザ内</p></div><div class="example-process"><p class="example-number">EXAMPLE 01</p><h3>Studio Yebisu Desk</h3><ol><li><b>Frontend Design</b><span>視覚方針・画面の情報階層</span></li><li><b>Emil Design Engineering</b><span>フォーム・フォーカス・操作の感触</span></li><li><b>Web Design Guidelines</b><span>実装の点検と修正</span></li><li><b>UI Skills / fixing-accessibility</b><span>ラベルとキーボード操作の点検</span></li></ol><a href="examples/studio-desk/README.md">適用した判断と実装を読む ↗</a></div></section>
<section class="pathways" id="choose" aria-labelledby="choose-title"><div class="section-heading"><p class="eyebrow">START WITH YOUR TASK</p><h2 id="choose-title">いま、何を進めたい？</h2><p>最初から全部を入れず、目の前の課題に合わせて。</p></div><div class="path-grid">
<a class="path" href="#frontend-design"><span>01 / DIRECTION</span><h3>見た目の軸を決めたい</h3><p>Frontend Designで視覚方針を考える。用途から候補を探すならUI UX Pro Max。</p><b aria-hidden="true">↗</b></a>
<a class="path" href="#impeccable"><span>02 / REVIEW</span><h3>できた画面を直したい</h3><p>Impeccableで改善点を整理。操作性のコード点検はWeb Design Guidelinesへ。</p><b aria-hidden="true">↗</b></a>
<a class="path" href="#emil-design-eng"><span>03 / INTERACTION</span><h3>操作の感触を整えたい</h3><p>Emilの判断基準で動きの要否を考え、Motion向けスキルとライブラリで実装する。</p><b aria-hidden="true">↗</b></a></div></section>
<section id="catalog" class="catalog" aria-labelledby="catalog-title"><div class="section-heading catalog-heading"><div><p class="eyebrow">THE AGENT SKILLS SHELF</p><h2 id="catalog-title">目的から、選ぶ。</h2></div><p>{count}のスキル・スキル集を収録。<br>作例への適用と、資料のみの確認を区別しています。</p></div>
<form class="filters" id="filters" role="search"><div class="search-row"><div class="search-field"><label for="search">キーワードで探す</label><input id="search" name="q" type="search" placeholder="例：フォーム、React、配色" autocomplete="off"></div><div class="source-field"><label for="origin">掲載の由来</label><select id="origin" name="origin"><option value="all">すべて</option><option value="source-post">元投稿のリソース</option><option value="supplement">追加調査</option></select></div><button class="reset" type="reset">条件をリセット</button></div>
<fieldset class="category-filter"><legend>目的で絞る</legend><div>{''.join(f'<button type="button" data-category="{value}" aria-pressed="{str(value == "all").lower()}">{label}</button>' for value,label in CATEGORIES)}</div></fieldset><output id="result-count" aria-live="polite" aria-atomic="true">{count} / {count} 件</output></form>
<noscript><p class="notice">JavaScriptが無効のため絞り込みは使えません。全リソースはこのまま読めます。</p></noscript><p id="empty" class="empty" hidden>条件に合うリソースがありません。キーワードを短くするか、条件をリセットしてください。</p><div class="resources">{cards}</div><p id="copy-status" class="copy-status" role="status" aria-live="polite"></p></section>
<section class="supporting" id="supporting" aria-labelledby="supporting-title"><div class="section-heading"><p class="eyebrow">SUPPORTING LIBRARY</p><h2 id="supporting-title">動きを実装するときに。</h2><p>ここからは補助ライブラリ。上のスキル件数・検索には含めません。</p></div><div class="resources">{library_cards}</div></section>
<section class="comparison" aria-labelledby="compare-title"><div class="section-heading"><p class="eyebrow">AT A GLANCE</p><h2 id="compare-title">スキルと実装の役割を分ける。</h2></div><div class="table-wrap" tabindex="0" role="region" aria-label="リソース比較表。狭い画面では横にスクロールできます"><table><caption>用途の早見表</caption><thead><tr><th scope="col">リソース</th><th scope="col">種類</th><th scope="col">主な用途</th></tr></thead><tbody>{table_rows}</tbody></table></div></section>
<section class="notes" id="about" aria-labelledby="about-title"><div><p class="eyebrow">ABOUT THIS GUIDE</p><h2 id="about-title">画面づくりを、ひとつの分野として。</h2><p><a href="{e(DATA['source_post'])}">RoundtableSpaceの元投稿</a>を起点に、GitHubでUI・UX向けのエージェントスキルを追加調査。元投稿の#10に、独自調査の{supplement_count}件を加えました。スキル集は一つの掲載単位とし、中のファイル数で件数を増やしていません。</p><p>元投稿#9のMotionは補助ライブラリとして別枠へ。映像・タイポグラフィ演出などは<a href="{e(DATA['motion_guide'])}">モーションデザイン版</a>へ。<a href="RESEARCH.md">調査範囲と選定理由</a>も記録しています。</p></div><div class="boundary"><h3>このガイドの範囲</h3><p>中心はWeb UIの視覚設計、操作設計、実装レビューです。UXには調査、情報設計、ユーザーテストも含まれます。ここに挙げたスキルで、その全工程を検証したものではありません。</p><p>確認版は固定コミットで記録。4件の指針を作例へ適用しましたが、導入コマンドや外部サービス接続は試していません。紹介先のスキル本体は同梱していません。</p></div></section>
</main><footer><span>STUDIO YEBISU / UI・UX DESIGN GUIDE</span><a href="README.md">README</a><a href="ATTRIBUTION.md">出典・ライセンス</a><a href="data/catalog.json">カタログデータ</a><a href="#top">先頭へ ↑</a></footer><script id="catalog-data" type="application/json">{serial}</script></body></html>
'''
    (ROOT / 'index.html').write_text(page, encoding='utf-8')
    lines = ['# UI・UX エージェントスキルガイド', '', 'Claude・CodexなどのエージェントでWeb UIを設計・実装・改善するための、日本語のスキル比較ガイドです。', '',
             f'原典確認日：**{DATA["verified_on"]}**。**{count}のスキル・スキル集**を収録し、Motionライブラリは補助資料として別枠にしています。', '',
             '## 実際につくる', '', '[Studio Yebisu Deskを開く](examples/studio-desk/index.html) — 架空の制作プロジェクトを検索・追加・編集・整理する、ブラウザ内保存の試作です。', '',
             'Frontend Design、Emil Design Engineering、Web Design Guidelines、UI Skillsの4件を読み、設計・実装・点検へ適用しました。導入コマンドの実行や外部サービスへの接続はしていません。', '',
             '[適用内容と実装](examples/studio-desk/README.md) · [スキル適用の記録](examples/studio-desk/skill-application.json) · [調査範囲と選定理由](RESEARCH.md)', '',
             '## モーション版との分担', '',
             f'[元投稿]({DATA["source_post"]})の#10 Motion.dev Animations SkillをUI側へ、#9 Motionは補助ライブラリとして掲載。残りの{supplement_count}件は追加調査です。映像制作、タイポグラフィ演出、GSAP・Lottieなどは[モーション版]({DATA["motion_guide"]})にまとめています。', '',
             'このガイドの中心は視覚設計・操作設計・実装レビューです。ユーザー調査、情報設計、ユーザーテストなどUXの全工程を網羅するものではありません。', '',
             '## 選び方', '', '| いま必要なこと | 候補 |', '|---|---|',
             '| 視覚方針を決める | Frontend Design / UI UX Pro Max |',
             '| 既存画面を改善する | Impeccable |',
             '| 操作性をコードで点検する | Web Design Guidelines |',
             '| UIの動きを設計・実装する | Emil Design Engineering / Motion.dev Animations Skill |',
             '| アクセシビリティを修正する | UI Skills / fixing-accessibility |',
             '| ブランドや画面の統一を考える | Taste Skill / Bencium / Allonsy Design System |',
             '| 既存コンポーネント・生成サービスを使う | shadcn/ui Skill / Stitch Skills |',
             '| 動きを実行する依存ライブラリ | Motion |', '', '## カタログ', '']
    for item in DATA['entries']:
        source = f'元投稿 #{item["source_post_number"]}' if item['origin'] == 'source-post' else '追加調査'
        application = ' / [作例に適用](examples/studio-desk/README.md)' if item.get('application') == 'studio-desk' else ' / 原典資料を確認'
        lines += [f'### {item["name"]}', '', f'**{item["kind_label"]} / {source}**{application}', '', item['summary'], '',
                  f'- 向いていること：{item["best_for"]}', f'- 必要なもの：{item["requirements"]}', f'- 範囲と限界：{item["limits"]}',
                  f'- ライセンス：{item["license"]}。{item["license_note"]}', '', '導入例（原典の記載を紹介。ここでは実行していません）：', '',
                  '```text', item['install'], '```', '', item['install_context'], '', '依頼文のたたき台（本ガイドの独自文）：', '', '> ' + item['task_brief'], '',
                  f'[リポジトリ]({item["repository_url"]}) · [確認した原典]({item["source_url"]}) · [導入手順]({item["readme_url"]}) · [ライセンス根拠]({item["license_url"]})', '',
                  f'確認日 {item["verified_on"]} / commit `{item["revision"]}`', '']
    lines += ['## ローカルで読む・更新する', '', '外部フォント・画像・ランタイム依存を持たない静的サイトです。`index.html`をブラウザで開くだけでも読めます。', '',
              '```powershell', 'python scripts/build_site.py', 'python scripts/check_site.py', 'node scripts/test_filters.cjs', 'python -m http.server 8080 --bind 127.0.0.1', '```', '',
              '最後のコマンドを実行した場合は、ブラウザで `http://127.0.0.1:8080/` を開きます。ビルド・検査にはPython 3とNode.jsを使います。サイトの表示にはどちらも不要です。', '',
              '`data/catalog.json`が掲載内容の正本です。編集後にビルドすると`index.html`とこのREADMEを再生成し、公開用の`dist/`も出力します。公開・デプロイは自動実行しません。', '',
              '## 検証の意味', '', '固定コミットの原典確認、4件の指針を適用した作例、このガイドのデータ・リンク整合・検索ロジック検査を分けています。作例は単一の試作であり、スキル間の優劣を比較するベンチマークではありません。アクセシビリティ適合や第三者スキルの導入動作を保証するものでもありません。', '',
              '## 出典とライセンス', '', '本ガイド独自の文章・依頼文・サイトコードは[MIT License](LICENSE)。紹介先のスキル、ライブラリ、ブランドは各権利者に帰属し、それぞれの条件に従います。第三者の全文・コード・ロゴは同梱していません。[出典・ライセンス一覧](ATTRIBUTION.md)を参照してください。', '']
    (ROOT / 'README.md').write_text('\n'.join(lines), encoding='utf-8')
    attribution = ['# 出典・ライセンス', '', f'確認日：{DATA["verified_on"]}', '', '本ガイドの独自文章・依頼文・サイトコードはMIT。下記は紹介先の条件であり、本ガイドのMITへ置き換えるものではありません。導入コマンドは原典に記載された手順の短い引用です。第三者の全文・スキル本体・サンプルコード・ロゴは再配布していません。', '', '| 紹介先 | 条件 | 根拠 |', '|---|---|---|']
    for item in DATA['entries']:
        attribution += [f'| {item["repo"]} | {item["license"]} | [確認版]({item["license_url"]}) |']
    attribution += ['', 'Vercel agent-skillsはREADMEのMIT表記を確認していますが、確認時点のツリーにLICENSE条文ファイルがなく、GitHub APIのlicense値もnullでした。そのため「MIT（README表記）」と区別しています。Web Design Guidelinesが実行時に参照する別リポジトリ、vercel-labs/web-interface-guidelinesにはMIT LICENSEがあります。', '',
                    f'選定の起点：[RoundtableSpaceの投稿]({DATA["source_post"]})。投稿由来の2項目と補足調査の{supplement_count}項目はカタログ内で区別しています。第三者の評価数・性能目標を本ガイドの検証成果とは扱っていません。', '']
    (ROOT / 'ATTRIBUTION.md').write_text('\n'.join(attribution), encoding='utf-8')
    dist = ROOT / 'dist'
    dist.mkdir(exist_ok=True)
    for path in ['index.html', 'styles.css', 'app.js', 'README.md', 'RESEARCH.md', 'ATTRIBUTION.md', 'LICENSE', 'data/catalog.json', 'data/research-2026-10-13.json', 'data/research-official-2026-10-13.json']:
        target = dist / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / path, target)
    shutil.copytree(ROOT / 'examples/studio-desk', dist / 'examples/studio-desk', dirs_exist_ok=True)
    print(f'Built {len(DATA["entries"])} resources: index.html, README.md, ATTRIBUTION.md, dist/')


if __name__ == '__main__':
    build()
