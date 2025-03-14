import requests
import os
import datetime

# Bluesky API 認証情報
BSKY_IDENTIFIER = os.getenv("BSKY_IDENTIFIER")
BSKY_PASSWORD = os.getenv("BSKY_PASSWORD")

# Bluesky API のエンドポイント
BASE_URL = "https://bsky.social/xrpc"

# 投稿削除の対象となる時間 (sec)
LIFE_TIME = int(os.getenv("LIFE_TIME") or 10800)

def login():
    """Bluesky にログインしてセッション情報を取得"""
    response = requests.post(
        f"{BASE_URL}/com.atproto.server.createSession",
        json={"identifier": BSKY_IDENTIFIER, "password": BSKY_PASSWORD},
    )
    response.raise_for_status()
    return response.json()["accessJwt"]

def fetch_posts(jwt):
    """自分の投稿を取得"""
    response = requests.get(
        f"{BASE_URL}/app.bsky.feed.getAuthorFeed?actor={BSKY_IDENTIFIER}",
        headers={"Authorization": f"Bearer {jwt}"},
    )
    response.raise_for_status()
    return response.json()["feed"]

def delete_post(jwt, uri):
    """指定された投稿を削除"""
    response = requests.post(
        f"{BASE_URL}/com.atproto.repo.deleteRecord",
        headers={"Authorization": f"Bearer {jwt}"},
        json={"repo": BSKY_IDENTIFIER, "collection": "app.bsky.feed.post", "rkey": uri.split("/")[-1]},
    )
    return response.status_code == 200

def main():
    """「あとで消す」を含む投稿を指定時間後に削除"""
    jwt = login()
    posts = fetch_posts(jwt)

    now = datetime.datetime.now(datetime.UTC).replace(tzinfo=None)
    for post in posts:
        content = post["post"]["record"]["text"]
        timestamp = datetime.datetime.strptime(post["post"]["record"]["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ")

        # 指定時間経過かつ 「あとで消す」を含む投稿のみ削除
        if "あとで消す" in content and (now - timestamp).total_seconds() >= LIFE_TIME:
            uri = post["post"]["uri"]
            if delete_post(jwt, uri):
                print(f"削除: {content} ({uri})")
            else:
                print(f"削除失敗: {uri}")

if __name__ == "__main__":
    main()
