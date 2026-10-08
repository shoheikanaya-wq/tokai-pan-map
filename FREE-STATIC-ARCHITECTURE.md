# ぷらっと東海 — 無料運用固定方針

最終更新: 2026-10-09

現在の本番は **GitHub Pages + 静的JSON + PWA** です。

## 本番で使うもの

- `index.html` — ぷらっと東海入口
- `new-pan.html` — ぷらっとパン本体
- `ramen.html` — ぷらっとラーメン
- `data/static-catalog.json` — 市町村データ索引
- `data/*.json` — 店舗静的データ
- `manifest.webmanifest`
- `sw.js`

## 本番で使わないもの

- Google Cloud Run
- Google Places API の本番自動取得
- Google Routes API の本番自動取得
- Firestore
- 旧 `route-api`（履歴保管のみ）
- 旧 Cloud Run / Places 監査ワークフロー

## 変更ルール

1. 本番HTML・Service Workerへ `*.run.app` を戻さない。
2. Google APIキーをフロントへ置かない。
3. 新しい外部APIや有料サービスを導入する場合は、無料運用への影響を確認してから変更する。
4. `tests/audit.mjs` と GitHub Actions の `PAN Audit` を通してから本番扱いにする。
5. 旧Cloud構成を再利用する場合は、明示的な再設計・承認を前提とする。

このファイルは、無料枠終了や請求設定変更でアプリが停止する事態を防ぐための運用基準です。
