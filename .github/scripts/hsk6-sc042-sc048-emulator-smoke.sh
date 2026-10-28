#!/usr/bin/env bash
set -euo pipefail
mkdir -p qa-screens
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb logcat -c

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
      if grep -Fq "canonical kaynaklar henüz yüklenmedi" "$hierarchy"; then
        echo "::error::SC${scene} canonical visual assets missing from APK"
        return 1
      fi
      if grep -Fq "Sahne arka planı" "$hierarchy" &&
         grep -Fq "Zhang Wei" "$hierarchy" &&
         grep -Fq "Li Na" "$hierarchy" &&
         grep -Fq "Derinlik katmanı" "$hierarchy"; then
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
      adb exec-out screencap -p > "qa-screens/sc${scene}_${speaker}_${mode}.png"
      test -s "qa-screens/sc${scene}_${speaker}_${mode}.png"
    done
  done
done
adb logcat -d > qa-screens/logcat.txt
if grep -F "Process: com.uysal23.newchinese" qa-screens/logcat.txt; then
  echo "App crashed during Android scene runtime QA"
  exit 1
fi
sha256sum qa-screens/*.png > qa-screens/screenshots.sha256
