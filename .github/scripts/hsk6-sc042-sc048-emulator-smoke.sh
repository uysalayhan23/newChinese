#!/usr/bin/env bash
set -euo pipefail
mkdir -p qa-screens
adb install -r app/build/outputs/apk/debug/app-debug.apk
adb logcat -c
for scene in 042 048; do
  for speaker in zhang li; do
    for mode in compact expanded; do
      expanded=false
      if [ "$mode" = expanded ]; then expanded=true; fi
      adb shell am force-stop com.uysal23.newchinese || true
      adb shell am start -n com.uysal23.newchinese/.ui.Hsk6ReviewProbeActivity --es scene "$scene" --es speaker "$speaker" --ez expanded "$expanded"
      sleep 3
      adb shell pidof com.uysal23.newchinese > /dev/null
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
