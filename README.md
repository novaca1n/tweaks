# novaca1n tweaks

The official source of [TweakStore](https://github.com/novaca1n/tweakstore) — tweaks for
[derealization](https://github.com/novaca1n/derealization). TweakStore reads [`repo.json`](repo.json); the APKs are
attached to each tweak's GitHub release.

| Tweak | Type | What it does |
|---|---|---|
| [Hive](https://github.com/novaca1n/hive) | app | Apple Watch–style honeycomb home screen |

## Publishing a version

```sh
tools/add-version.py dev.novacain.hive hive.apk \
    https://github.com/novaca1n/hive/releases/download/v0.1/hive-0.1.apk \
    --changelog-en "…" --changelog-ru "…"
```

It reads the version from the APK and fills in `sha256` and `size`, so they always match the file. Upload the same APK
to the release, then commit `repo.json`.

Want your own source? See the [format](https://github.com/novaca1n/tweakstore#make-your-own-source).
