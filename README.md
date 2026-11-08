# ひめ配信（姫咲こはく SHOWROOM配信スケジュール）

https://laviera9.github.io/hime-showroom-calendar/ ― iPhone: Safariで開いて「共有 → ホーム画面に追加」。

- `index.html` / `hime_showroom.ics` / `manifest.webmanifest` / `sw.js` は `build_hime.py` が生成。
- 予定の元データ: `hime_events.json`（`tools/` にコピーあり。正本は box の `/workspace/hime_events.json`）。
- ビルド: `cd /workspace && python3 build_hime.py`（repo を `/workspace/hime-showroom-calendar` に置いた状態で実行）。
- 週間画像は `assets/week-*.jpg` を手動で差し替え、`build_hime.py` の `WEEK` を更新（自動生成ではない）。
- SHOWROOM は外部リンク（埋め込み再生不可）。サイトから通知は送らない。sw.js はネットワーク優先・オフライン時のみキャッシュ。
