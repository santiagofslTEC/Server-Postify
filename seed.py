import httpx

BASE = "http://localhost:8000"

users = [
    {"username": "aria_vance", "name": "Aria", "lastname": "Vance", "email": "aria@postify.com", "password": "1234"},
    {"username": "marcus_thorne", "name": "Marcus", "lastname": "Thorne", "email": "marcus@postify.com", "password": "1234"},
    {"username": "elena_rossi", "name": "Elena", "lastname": "Rossi", "email": "elena@postify.com", "password": "1234"},
]

posts = [
    "The intersection of light, shadow, and brutalist architecture.",
    "Stripping away the noise and returning to pure form.",
    "A study in obsidian silk and limestone light.",
    "Fluidity in motion — the body as architecture.",
    "Editorial silence. The space between the frames.",
    "Monochrome landscapes and the weight of atmosphere.",
    "Texture as language. Form as feeling.",
    "Season of stark contrasts and quiet intensity.",
]

created_users = []
for u in users:
    res = httpx.post(f"{BASE}/users/", json=u, follow_redirects=True)
    if res.status_code == 201:
        created_users.append(res.json())
        print(f"Created user: {u['username']} → {res.json()['id']}")
    else:
        print(f"Failed to create {u['username']}: {res.status_code} — {res.text}")

for i, desc in enumerate(posts):
    user = created_users[i % len(created_users)]
    res = httpx.post(f"{BASE}/posts/", json={"description": desc, "user_id": user["id"]}, follow_redirects=True)
    if res.status_code == 201:
        print(f"Created post: \"{desc[:40]}...\"")
    else:
        print(f"Failed to create post: {res.text}")

print("\nDone! Navigate to:")
for u in created_users:
    print(f"  /profile/{u['id']}  ({u['username']})")

#Done! Navigate to:
  #/profile/53706a67-3c12-4857-89ad-6b9a67b6322b  (aria_vance)
  #/profile/d20449f6-75b5-4a9f-8517-b521ef9ba4b1  (marcus_thorne)
  #/profile/e8e30270-5dba-4c2b-b7d1-b8d7795d5909  (elena_rossi)