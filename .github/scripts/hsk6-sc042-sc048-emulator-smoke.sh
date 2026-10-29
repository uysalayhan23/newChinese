#!/usr/bin/env bash
set -euo pipefail
mkdir -p qa-screens
# Keep device crash evidence even when an intermediate assertion exits early.
capture_failure_evidence() {
  local status=$?
  if [ "$status" -ne 0 ]; then
    adb logcat -d > qa-screens/failure_logcat.txt 2>&1 || true
    adb shell dumpsys activity activities > qa-screens/failure_activity.txt 2>&1 || true
    adb shell dumpsys meminfo com.uysal23.newchinese > qa-screens/failure_meminfo.txt 2>&1 || true
  fi
}
trap capture_failure_evidence EXIT

# A Pixel Launcher ANR can cover a fully rendered scene on the emulator.
# Save evidence and dismiss ONLY the exact launcher dialog, never an app ANR.
recover_launcher_anr() {
  local hierarchy="$1" tap x y stem
  if ! grep -Fq "Pixel Launcher isn't responding" "$hierarchy"; then
    return 1
  fi
  if ! tap="$(python3 - "$hierarchy" <<'PY'
import re
import sys
import xml.etree.ElementTree as ET
root = ET.parse(sys.argv[1]).getroot()
nodes = list(root.iter("node"))
titles = [n.get("text") for n in nodes if n.get("resource-id") == "android:id/alertTitle"]
if titles != ["Pixel Launcher isn't responding"]:
    sys.exit(1)
buttons = [n for n in nodes if n.get("resource-id") == "android:id/aerr_close" and n.get("text") == "Close app"]
if len(buttons) != 1:
    sys.exit(1)
bounds = re.fullmatch(r"\[(\d+),(\d+)\]\[(\d+),(\d+)\]", buttons[0].get("bounds", ""))
if not bounds:
    sys.exit(1)
x1, y1, x2, y2 = map(int, bounds.groups())
if x2 <= x1 or y2 <= y1:
    sys.exit(1)
print((x1 + x2) // 2, (y1 + y2) // 2)
PY
)"; then
    return 1
  fi
  read -r x y <<< "$tap"
  stem="${hierarchy%.xml}"
  cp "$hierarchy" "${stem}_launcher_anr.xml"
  adb exec-out screencap -p > "${stem}_launcher_anr.png" 2>/dev/null || true
  adb logcat -d > "${stem}_launcher_anr_logcat.txt" 2>&1 || true
  echo "::warning::Pixel Launcher ANR overlay dismissed; scene still requires independent PASS"
  adb shell input tap "$x" "$y"
  sleep 2
  return 0
}

# REVIEW-only hard gate: a successful APK build is not SC042/048 visual acceptance.
# Require the exact approved WebP blobs in both checkout and the APK assets.
assert_review_canonical_assets() {
  local apk="app/build/outputs/apk/debug/app-debug.apk"
  if [ ! -s "$apk" ]; then
    echo "::error::Debug APK missing before canonical asset QA"; return 1
  fi
  local -a expected_assets=(
    "bg:1eed67c86bd543c56ef9766a86b40b241afe3ecf"
    "char_zhang_wei:13c6761792396b85f0c4a4a1e20b581a8fc13aa2"
    "char_li_na:a02f88b5075f6cb590d8c0f23219b0e5fa3e80d0"
    "fg:61d80dcfd46fe74475e32578e86e01343de5ab40"
    "preview:1a82a31c12caa2cab57b64fb91c1beaf9f1b1028"
  )
  local scene entry suffix expected path repo_sha apk_sha
  for scene in 042 048; do
    for entry in "${expected_assets[@]}"; do
      suffix="${entry%%:*}"; expected="${entry#*:}"
      path="content/hsk6/sc${scene}/assets/hsk6_sc${scene}_${suffix}.webp"
      if [ ! -s "$path" ]; then
        echo "::error file=$path::Approved canonical review asset missing"; return 1
      fi
      repo_sha="$(git hash-object "$path")"
      if [ "$repo_sha" != "$expected" ]; then
        echo "::error file=$path::Wrong canonical blob: got $repo_sha, expected $expected"; return 1
      fi
      if ! apk_sha="$(unzip -p "$apk" "assets/${path#content/}" | git hash-object --stdin)"; then
        echo "::error file=$path::Canonical asset missing or unreadable in built APK"; return 1
      fi
      if [ "$apk_sha" != "$expected" ]; then
        echo "::error file=$path::Built APK contains wrong asset: got $apk_sha, expected $expected"; return 1
      fi
    done
  done
  echo "SC042/048 canonical repository + APK assets SHA PASS (10/10)"
}
assert_review_canonical_assets

adb install -r app/build/outputs/apk/debug/app-debug.apk
adb logcat -c

# Physical-device regression: selecting a real scene (intro/dialogue) was
# reported to close the app. The layer-only probe cannot catch this path.
check_real_scene_screen() {
  local scene="$1" screen="$2" title="$3"
  local prefix="qa-screens/sc${scene}_${screen}_app"
  local ready=false
  adb shell am force-stop com.uysal23.newchinese || true
  adb logcat -c
  adb shell am start -n com.uysal23.newchinese/.ui.Hsk6ReviewProbeActivity \
    --es scene "$scene" --es screen "$screen"
  for attempt in $(seq 1 16); do
    if ! adb shell pidof com.uysal23.newchinese >/dev/null 2>&1; then
      break
    fi
    if timeout 18s adb shell uiautomator dump /sdcard/newchinese-review.xml >/dev/null 2>&1 &&
       timeout 8s adb exec-out cat /sdcard/newchinese-review.xml > "${prefix}.xml" 2>/dev/null; then
      if recover_launcher_anr "${prefix}.xml"; then
        continue
      fi
      if grep -Fq "$title" "${prefix}.xml"; then
        sleep 2
        if adb shell pidof com.uysal23.newchinese >/dev/null 2>&1; then
          ready=true
          break
        fi
      fi
    fi
    sleep 2
  done
  adb exec-out screencap -p > "${prefix}.png" 2>/dev/null || true
  adb logcat -d > "${prefix}_logcat.txt" 2>&1 || true
  if [ "$ready" != true ] ||
     grep -Fq "Process: com.uysal23.newchinese" "${prefix}_logcat.txt"; then
    echo "::error::SC${scene} ${screen}: real content screen crashed or did not render"
    return 1
  fi
  echo "SC${scene} ${screen}: content loaded, screen visible and process alive"
}
for scene in 042 048; do
  title="Dil yaşamda neyi değiştirdi"
  if [ "$scene" = 048 ]; then title="Gelecekte de hata yapmak"; fi
  check_real_scene_screen "$scene" intro "$title"
  check_real_scene_screen "$scene" dialogue "$title"
done

# A running PID or a nonempty PNG does not prove the scene rendered.
# Previous successful workflow captured only Android's launch splash.
wait_until_scene_rendered() {
  local scene="$1" speaker="$2" mode="$3"
  local hierarchy="qa-screens/sc${scene}_${speaker}_${mode}.xml"
  local attempt
  for attempt in $(seq 1 20); do
    # UIAutomator inspects the visible window, rejecting the system splash.
    if timeout 18s adb shell uiautomator dump /sdcard/newchinese-review.xml >/dev/null 2>&1 &&
       timeout 8s adb exec-out cat /sdcard/newchinese-review.xml > "$hierarchy" 2>/dev/null; then
      if recover_launcher_anr "$hierarchy"; then
        continue
      fi
      if grep -Fq "canonical kaynaklar henüz yüklenmedi" "$hierarchy"; then
        echo "::error::SC${scene} canonical visual assets missing from APK"
        return 1
      fi
      # Fully overlapped Compose Images may disappear from accessibility
      # even when they render. The ready marker exists only after all four
      # canonical layers passed decoding, alpha and dimension checks.
      local expected_marker="SC${scene}_REVIEW_READY_${speaker^^}"
      if python3 tools/hsk6_review_evidence_gate.py --xml "$hierarchy" --scene "$scene" --speaker "$speaker" --mode "$mode" >/dev/null 2>&1; then
        echo "Rendered SC${scene} ${speaker} ${mode} on attempt ${attempt}"
        return 0
      fi
    fi
    if ! adb shell pidof com.uysal23.newchinese >/dev/null 2>&1; then
      echo "::error::SC${scene} application exited before scene rendered"
      return 1
    fi
    sleep 2
  done
  # Preserve the accessibility evidence too: missing nodes and failed UIAutomator
  # dumps previously produced the same opaque timeout message.
  if [ -s "$hierarchy" ]; then
    echo "SC${scene} ${speaker} ${mode}: last UIAutomator hierarchy:"
    head -c 3000 "$hierarchy" || true
    echo
  else
    echo "::warning::SC${scene} ${speaker} ${mode}: no UIAutomator hierarchy was captured"
  fi
  timeout 18s adb shell uiautomator dump /sdcard/newchinese-review.xml \
    > "qa-screens/sc${scene}_${speaker}_${mode}_uiautomator.txt" 2>&1 || true
  # Preserve evidence when scene detection fails, before the emulator shuts down.
  adb exec-out screencap -p > "qa-screens/sc${scene}_${speaker}_${mode}_failure.png" 2>/dev/null || true
  adb shell dumpsys window windows > "qa-screens/sc${scene}_${speaker}_${mode}_windows.txt" 2>&1 || true
  adb shell dumpsys activity top > "qa-screens/sc${scene}_${speaker}_${mode}_activity.txt" 2>&1 || true
  adb logcat -d > "qa-screens/sc${scene}_${speaker}_${mode}_logcat.txt" 2>&1 || true
  echo "::error::SC${scene} ${speaker} ${mode}: splash or unavailable scene; NOT PASS"
  adb shell dumpsys activity activities | tail -n 60 || true
  return 1
}

for scene in 042 048; do
  for speaker in zhang li; do
    for mode in compact expanded; do
      expanded=false
      if [ "$mode" = expanded ]; then expanded=true; fi
      adb shell am force-stop com.uysal23.newchinese || true
      adb shell am start -n com.uysal23.newchinese/.ui.Hsk6ReviewProbeActivity --es scene "$scene" --es speaker "$speaker" --ez expanded "$expanded"
      wait_until_scene_rendered "$scene" "$speaker" "$mode"
      # A correct accessibility tree can precede the first drawn frame.
      # Retry until BOTH the scene geometry and real screenshot pixels pass.
      local_capture="qa-screens/sc${scene}_${speaker}_${mode}.png"
      frame_pass=false
      for frame_attempt in $(seq 1 12); do
        adb exec-out screencap -p > "$local_capture"
        if python3 tools/hsk6_review_evidence_gate.py \
          --xml "qa-screens/sc${scene}_${speaker}_${mode}.xml" \
          --png "$local_capture" --scene "$scene" --speaker "$speaker" --mode "$mode"; then
          frame_pass=true
          break
        fi
        sleep 2
        timeout 18s adb shell uiautomator dump /sdcard/newchinese-review.xml >/dev/null 2>&1 || true
        timeout 8s adb exec-out cat /sdcard/newchinese-review.xml \
          > "qa-screens/sc${scene}_${speaker}_${mode}.xml" 2>/dev/null || true
      done
      if [ "$frame_pass" != true ]; then
        echo "::error::SC${scene} ${speaker} ${mode}: screenshot/geometry NOT PASS"
        adb logcat -d > "qa-screens/sc${scene}_${speaker}_${mode}_logcat.txt" 2>&1 || true
        exit 1
      fi
    done
  done
done
# Different speakers and viewport modes must produce distinct actual scene pixels.
# This catches silent reuse of a splash, stale framebuffer or wrong intent extras.
for scene in 042 048; do
  if cmp -s "qa-screens/sc${scene}_zhang_compact.png" "qa-screens/sc${scene}_li_compact.png"; then
    echo "::error::SC${scene} speaker change did not alter pixels"; exit 1
  fi
  if cmp -s "qa-screens/sc${scene}_zhang_compact.png" "qa-screens/sc${scene}_zhang_expanded.png"; then
    echo "::error::SC${scene} expanded mode did not alter pixels"; exit 1
  fi
done

adb logcat -d > qa-screens/logcat.txt
if grep -F "Process: com.uysal23.newchinese" qa-screens/logcat.txt; then
  echo "App crashed during Android scene runtime QA"
  exit 1
fi
sha256sum qa-screens/*.png > qa-screens/screenshots.sha256
