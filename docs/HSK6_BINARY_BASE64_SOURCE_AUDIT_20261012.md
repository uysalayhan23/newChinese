# HSK6 base64 WebP binary-read audit — 2026-10-12

Repository: `uysalayhan23/newChinese`; branch: `main`.

## Newly available connector capability
The GitHub connector's `fetch_file` with `encoding="base64"` returns actual WebP bytes. Prior UTF-8 read errors no longer prevent source-level binary header inspection.

## Executed verification
- Evaluated the SHA-pinned source list at `tools/hsk6_ready_preview_blobs.json`: 16 scene records, 64 asset references, **14 distinct Git blob IDs**.
- Successfully fetched and base64-decoded all **14 distinct source blobs** by their scene paths.
- Parsed RIFF/WEBP container headers, compared embedded RIFF sizes to decoded byte counts, extracted format and dimensions, and matched GitHub-returned file blob IDs against the lock manifest.
- Expanded verified blobs back to the 64 scene asset references: **64/64 source checks PASS**.

## Qualification
The verified SHA matches use the GitHub-provided blob SHA field, not an independently recomputed cryptographic digest. This is a binary container/manifest audit, not complete image decode, per-pixel alpha QA, composition QA, or character continuity acceptance.

## Pending
- Move decoded WebP bytes from the connector execution context to an image-processing runtime (a compatible binary transport is still needed).
- Run original repository Python/Pillow suites on real source files.
- Compose and inspect 16 exact 720×1280 previews and 20 face-right candidates.
- Leave media and acceptance state as pending until independent QA passes.

No GitHub Actions were run; no canonical assets or locked scene content were modified.
