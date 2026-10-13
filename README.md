# Claude UI・UXデザインガイド

ClaudeなどのエージェントでWeb UIを設計・実装・改善するための、日本語のリソース比較ガイドです。

原典確認日：**2026-10-13**。6つのスキルと1つのライブラリを収録。スキルのインストール・動作検証は行っていません。

## モーション版との分担

[元投稿](https://x.com/RoundtableSpace/status/2109958757891346459)の#10 Motion.dev Animations SkillをUI側へ、#9 Motionは共通の実装基盤として掲載。UI設計・レビューの5件は追加調査です。映像制作、タイポグラフィ演出、GSAP・Lottieなどは[モーション版](https://studio-yebisu.github.io/awesome-claude-motion-design-ja/)にまとめています。

このガイドの中心は視覚設計・操作設計・実装レビューです。ユーザー調査、情報設計、ユーザーテストなどUXの全工程を網羅するものではありません。

## 選び方

| いま必要なこと | 候補 |
|---|---|
| 視覚方針を決める | Frontend Design / UI UX Pro Max |
| 既存画面を改善する | Impeccable |
| 操作性をコードで点検する | Web Design Guidelines |
| UIの動きを設計・実装する | Emil Design Engineering / Motion.dev Animations Skill |
| 動きを実行する依存ライブラリ | Motion |

## カタログ

### Frontend Design

**スキル / 追加調査**

対象サービスに合う文字、色、余白、レイアウトを考える、Anthropicのフロントエンド向けスキル。画面を新しくつくるときや、既存UIの印象を変える入口に。

- 向いていること：LP、サービスサイト、ダッシュボードの視覚方針と実装。
- 必要なもの：Claude Codeなど、SKILL.mdを扱うエージェント。実装先の言語や既存デザイン規約は依頼に添える。
- 範囲と限界：視覚設計が中心。ユーザー調査、導線の実証、アクセシビリティ適合をこのスキルだけで保証するものではない。
- ライセンス：Apache-2.0。frontend-design配下のLICENSE.txtを確認。リポジトリ全体へ一律に適用しない。

導入例（原典の記載を紹介。ここでは実行していません）：

```text
/plugin marketplace add anthropics/skills
/plugin install example-skills@anthropic-agent-skills
```

Claude Code内で入力。公式READMEのexample-skillsセット導入手順で、frontend-design単体のインストールではない。

依頼文のたたき台（本ガイドの独自文）：

> frontend-designを使って、このサービスのトップ画面を設計してください。対象ユーザーは【誰】、最優先の行動は【何】です。既存のブランド規約と実際の文言を使い、文字・色・余白の方針を短く示してから実装してください。スマートフォンとキーボード操作も確認してください。

[リポジトリ](https://github.com/anthropics/skills) · [確認した原典](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/frontend-design/SKILL.md) · [導入手順](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/README.md) · [ライセンス根拠](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/frontend-design/LICENSE.txt)

確認日 2026-10-13 / commit `dbd4588f9e1033efb41dad4bef2f7947c8993d44`

### Impeccable

**スキル＋CLI / 追加調査**

見た目の講評、文言、余白、端末対応、エラー状態などを目的別に扱うスキルとツール。既存の画面に対し、どこを直すかを絞って反復したいときに。

- 向いていること：既存UIの改善、UX文言の整理、画面品質の点検。
- 必要なもの：対応エージェントと対象プロジェクト。npx経由の導入はNode.jsが必要。エンジンを同梱または初回取得し、導入時にはフック設定も提示される。
- 範囲と限界：自動検出とAI講評は利用者による使いやすさの検証とは別。ライブ編集の利用には起動できるWebプロジェクトが必要。
- ライセンス：Apache-2.0。LICENSEを確認。Anthropic frontend-designを起点とする旨をREADMEが記載。

導入例（原典の記載を紹介。ここでは実行していません）：

```text
npx impeccable install
```

対象プロジェクトのターミナルで実行。公式の対話式インストーラーで対象エージェントと範囲を選ぶ。

依頼文のたたき台（本ガイドの独自文）：

> Impeccableで【画面】をレビューしてください。利用者が【目的】を達成する流れをたどり、視覚的な優先順位、説明文、入力エラー、空の状態を確認してください。問題の場所と理由を示し、影響の大きい3点を修正してください。

[リポジトリ](https://github.com/pbakaus/impeccable) · [確認した原典](https://github.com/pbakaus/impeccable/blob/245ad82def45831dc56a21b683c7a1ff530b06cc/.claude/skills/impeccable/SKILL.md) · [導入手順](https://github.com/pbakaus/impeccable/blob/245ad82def45831dc56a21b683c7a1ff530b06cc/README.md) · [ライセンス根拠](https://github.com/pbakaus/impeccable/blob/245ad82def45831dc56a21b683c7a1ff530b06cc/LICENSE)

確認日 2026-10-13 / commit `245ad82def45831dc56a21b683c7a1ff530b06cc`

### UI UX Pro Max

**スキル＋検索データ / 追加調査**

業種や画面の目的から、配色、書体、スタイル、UXの注意点を検索するスキル。新しいプロダクトの設計方針を整理し、実装スタックに合わせて具体化する。

- 向いていること：新規プロダクトの設計案、デザインシステムのたたき台。
- 必要なもの：CLI導入はNode.js/npm、検索スクリプトはPython 3.x。利用者、業種、用途、実装スタックを具体的に指定する。
- 範囲と限界：検索結果は設計候補。既存ブランド、業務要件、実ユーザーの行動に合わせて選別する。ここでは公開リポジトリのみを対象とし、別提供の有料機能は含めない。
- ライセンス：MIT。公開リポジトリのLICENSEを確認。外部の有料提供や参照素材の条件は別。

導入例（原典の記載を紹介。ここでは実行していません）：

```text
npx ui-ux-pro-max-cli init --ai claude
```

プロジェクトのターミナルで実行。公式READMEに記載された、グローバル導入を省く方法。

依頼文のたたき台（本ガイドの独自文）：

> ui-ux-pro-maxで【用途】のUI方針を提案してください。対象は【利用者】、実装は【スタック】です。既存の色・書体・操作規約を優先し、候補を理由付きで比較してください。選んだ方針を画面ごとのルールへ落とし込み、推測と確定要件を分けてください。

[リポジトリ](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) · [確認した原典](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/7246805992a42b7bba37d4cac83b01416f0c6c44/.claude/skills/ui-ux-pro-max/SKILL.md) · [導入手順](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/7246805992a42b7bba37d4cac83b01416f0c6c44/README.md) · [ライセンス根拠](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/blob/7246805992a42b7bba37d4cac83b01416f0c6c44/LICENSE)

確認日 2026-10-13 / commit `7246805992a42b7bba37d4cac83b01416f0c6c44`

### Web Design Guidelines

**レビュースキル / 追加調査**

VercelのWeb Interface Guidelinesを取得し、指定したUIコードを点検するスキル。フォーカス、フォーム、キーボード操作、動きを減らす設定などの実装レビューに。

- 向いていること：実装後の操作性・アクセシビリティ・フォームのコード点検。
- 必要なもの：対象ファイルを読めるエージェントと、最新版ガイドラインを取得するネットワーク接続。
- 範囲と限界：実行時に外部ガイドラインを取得するため、同じスキル版でも判定規則は変わり得る。コードレビューだけでWCAG適合や実機での使いやすさを保証しない。
- ライセンス：MIT（README表記）。agent-skillsのREADMEはMITと記載。ただし確認版のツリーにLICENSE条文ファイルはなく、GitHub APIのlicense値もnull。参照先web-interface-guidelinesは別リポジトリでMIT。

導入例（原典の記載を紹介。ここでは実行していません）：

```text
npx skills add vercel-labs/agent-skills
```

公式READMEのリポジトリ導入コマンド。選択画面でweb-design-guidelinesを選ぶ。

依頼文のたたき台（本ガイドの独自文）：

> web-design-guidelinesで【対象ファイル】をレビューしてください。フォームのラベル、エラーの伝達、Tab移動、フォーカスの戻り先、動きを減らす設定を確認してください。根拠のある指摘をファイル位置付きで示し、ブラウザで追加確認すべき点も分けてください。

[リポジトリ](https://github.com/vercel-labs/agent-skills) · [確認した原典](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/skills/web-design-guidelines/SKILL.md) · [導入手順](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/README.md) · [ライセンス根拠](https://github.com/vercel-labs/agent-skills/blob/063bee94c3f4df8453406c830b0a7df0f2860278/README.md)

確認日 2026-10-13 / commit `063bee94c3f4df8453406c830b0a7df0f2860278`

### Emil Design Engineering

**スキル / 追加調査**

Emil KowalskiのUI設計とアニメーションの判断をまとめたスキル。動かす必要性、反応速度、途中で操作された場合の挙動など、コンポーネントの細部を扱う。

- 向いていること：ボタン、ポップオーバー、ツールチップ、ドラッグ操作の仕上げ。
- 必要なもの：既存のUIコードと、確認できるブラウザ。現行スキル名はemil-design-eng。
- 範囲と限界：デザインエンジニアリングと動きが中心。情報設計や調査を含むUX全工程の代替ではない。
- ライセンス：MIT。LICENSEを確認。ガイドでは現行リポジトリ内のemil-design-engを紹介。

導入例（原典の記載を紹介。ここでは実行していません）：

```text
npx skills@latest add emilkowalski/skills
```

公式READMEの導入コマンド。選択画面でemil-design-engを選ぶ。

依頼文のたたき台（本ガイドの独自文）：

> emil-design-engを使って【コンポーネント】の操作感を整えてください。頻繁に使う操作は待たせず、開閉を連打した場合や途中で逆操作した場合も確認してください。動きを減らす設定とタッチ操作を含め、変更前後と理由を示してください。

[リポジトリ](https://github.com/emilkowalski/skills) · [確認した原典](https://github.com/emilkowalski/skills/blob/2d228630ba1446365f614a108cb8252f1feda202/skills/emil-design-eng/SKILL.md) · [導入手順](https://github.com/emilkowalski/skills/blob/2d228630ba1446365f614a108cb8252f1feda202/README.md) · [ライセンス根拠](https://github.com/emilkowalski/skills/blob/2d228630ba1446365f614a108cb8252f1feda202/LICENSE)

確認日 2026-10-13 / commit `2d228630ba1446365f614a108cb8252f1feda202`

### Motion.dev Animations Skill

**スキル / 元投稿 #10**

Motionのスクロール、ホバー、ドラッグ、レイアウト遷移を実装するためのClaude Codeスキル。元投稿の15項目から、操作画面向けの1件をこのガイドへ分離。

- 向いていること：React / Next.jsなどの、操作や状態変化を伝えるWeb UI。
- 必要なもの：Claude Code、Git、実装先のMotion環境。原典はReact 19+、Next.js 15+、Svelte 5+、Astro 4+を対象に記載。実案件のバージョン適合は別確認。
- 範囲と限界：READMEの120fpsなどは著者の目標・説明で、本ガイドの実測結果ではない。Vueはmotion-vの別API。CSSだけで済む小さな動きや映像書き出しには用途を見直す。
- ライセンス：MIT。LICENSEを確認。Motionライブラリ本体とは別の第三者スキル。

導入例（原典の記載を紹介。ここでは実行していません）：

```text
git submodule add https://github.com/199-biotechnologies/motion-dev-animations-skill.git .claude/skills/motion-dev-animations
```

Git管理している対象プロジェクトで実行。公式READMEのプロジェクト内導入例で、.gitmodulesも作成・更新する。

依頼文のたたき台（本ガイドの独自文）：

> motion-dev-animationsで【UIの状態変化】を実装してください。使用中のフレームワークとMotionの版を先に確認し、動きの目的を【位置関係／操作への反応／状態説明】から明確にしてください。操作を妨げず、キーボードと動きを減らす設定に対応し、対象端末で確認してください。

[リポジトリ](https://github.com/199-biotechnologies/motion-dev-animations-skill) · [確認した原典](https://github.com/199-biotechnologies/motion-dev-animations-skill/blob/3feedfb4dba8adae40fc9a5f9a23e3dda2121205/SKILL.md) · [導入手順](https://github.com/199-biotechnologies/motion-dev-animations-skill/blob/3feedfb4dba8adae40fc9a5f9a23e3dda2121205/README.md) · [ライセンス根拠](https://github.com/199-biotechnologies/motion-dev-animations-skill/blob/3feedfb4dba8adae40fc9a5f9a23e3dda2121205/LICENSE)

確認日 2026-10-13 / commit `3feedfb4dba8adae40fc9a5f9a23e3dda2121205`

### Motion

**ライブラリ / 元投稿 #9**

Webの動きを実行するJavaScript / React向けライブラリ。スキルに教わったUIアニメーションをコードで実現する土台として、両ガイドから参照する共通項目。

- 向いていること：UIのジェスチャー、スクロール連動、要素の出入り、レイアウト変化。
- 必要なもの：JavaScriptのプロジェクト。Reactはmotion/react、Vueは別パッケージmotion-vの公式手順を参照。
- 範囲と限界：ライブラリの導入だけでClaudeに設計スキルが追加されるわけではない。Motion+の素材・サービスは、このMITライブラリ本体と条件が異なる。
- ライセンス：MIT。Motion本体のLICENSE.mdを確認。Motion+までMITという意味ではない。

導入例（原典の記載を紹介。ここでは実行していません）：

```text
npm install motion
```

JavaScript / Reactプロジェクトのターミナルで実行。スキル導入ではなくアプリの依存追加。

依頼文のたたき台（本ガイドの独自文）：

> このプロジェクトでMotionを使い、【UI要素】の状態変化を実装してください。既存の依存関係と版を確認し、処理完了を待たせない動きにしてください。中断や連続操作、フォーカス維持、動きを減らす設定も確認してください。

[リポジトリ](https://github.com/motiondivision/motion) · [確認した原典](https://github.com/motiondivision/motion/blob/790a654dfef305307c566cf4e94d67a9f7a403c8/README.md) · [導入手順](https://github.com/motiondivision/motion/blob/790a654dfef305307c566cf4e94d67a9f7a403c8/README.md) · [ライセンス根拠](https://github.com/motiondivision/motion/blob/790a654dfef305307c566cf4e94d67a9f7a403c8/LICENSE.md)

確認日 2026-10-13 / commit `790a654dfef305307c566cf4e94d67a9f7a403c8`

## ローカルで読む・更新する

外部フォント・画像・ランタイム依存を持たない静的サイトです。`index.html`をブラウザで開くだけでも読めます。

```powershell
python scripts/build_site.py
python scripts/check_site.py
node scripts/test_filters.cjs
python -m http.server 8080 --bind 127.0.0.1
```

最後のコマンドを実行した場合は、ブラウザで `http://127.0.0.1:8080/` を開きます。ビルド・検査にはPython 3とNode.jsを使います。サイトの表示にはどちらも不要です。

`data/catalog.json`が掲載内容の正本です。編集後にビルドすると`index.html`とこのREADMEを再生成し、公開用の`dist/`も出力します。公開・デプロイは自動実行しません。

## 検証の意味

固定コミットの原典確認と、このガイドのデータ・リンク整合・検索ロジックの検査を分けています。第三者スキルの実行成績、生成UIの品質、アクセシビリティ適合は保証していません。

## 出典とライセンス

本ガイド独自の文章・依頼文・サイトコードは[MIT License](LICENSE)。紹介先のスキル、ライブラリ、ブランドは各権利者に帰属し、それぞれの条件に従います。第三者の全文・コード・ロゴは同梱していません。[出典・ライセンス一覧](ATTRIBUTION.md)を参照してください。
