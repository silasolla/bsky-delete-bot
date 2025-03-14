# bsky-delete-bot

- 「あとで消す」を含む Bluesky のポストを削除します
- 定期実行することで，投稿したポストを数時間だけ表示することができます

## 使い方

1. このリポジトリをフォークします．
2. リポジトリの "Settings > Secrets and variables > Actions" に Secrets と Varibles を登録します

- `BSKY_IDENTIFIER` (Secrets): Bluesky の ID
- `BSKY_PASSWORD` (Secrets): Bluesky のアプリパスワード (「設定 > プライバシーとセキュリティ」から発行)
- `LIFE_TIME` (Variables): ポストが削除対象になるまでの時間 (sec)

## 定期実行の間隔について

- `.github/workflows/cron.yml` の `schedule` で定期実行の間隔を2時間ごとに設定しています
- この間隔を変更する場合は `schedule` の値を変更してください
  - GitHub Actions は 2,000 min/month まで無料で利用できます
  - 今のところ，このワークフローは 20 sec 以内で終了しています
  - 2時間おきだと，仮に 1 min 掛かっても，月に 360 min しか実行されません
