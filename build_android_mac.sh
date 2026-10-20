#!/bin/bash
set -euo pipefail
# Do not enable shell tracing: signing passwords are inherited via environment.
project_root="$(cd "$(dirname "$0")/../UnityProject" && pwd)"
unity_editor="${ITME_UNITY_EDITOR:-/Applications/Unity/Hub/Editor/6000.0.62f1/Unity.app/Contents/MacOS/Unity}"
mode="${1:-test}"
case "$mode" in
 test) method=ItmeArena.Editor.ReleaseBuildTools.TestApk ;;
 release) method=ItmeArena.Editor.ReleaseBuildTools.ReleaseAab ;;
 *) echo 'Usage: bash Tools/build_android_mac.sh test|release' >&2; exit 2 ;;
esac
if [[ ! -x "$unity_editor" ]]; then echo 'Unity bulunamadı. Unity Hub kurun veya ITME_UNITY_EDITOR belirtin.' >&2; exit 3; fi
: "${ITME_API_URL:?Gerçek HTTPS sunucu kök adresini belirtin}"
: "${ITME_VERSION_CODE:?Son kullanılan koddan büyük sürüm kodu belirtin}"
if [[ "$mode" == release ]]; then
 : "${ITME_KEYSTORE_PATH:?Mevcut proje dışı keystore gerekli}"
 : "${ITME_KEY_ALIAS:?Anahtar alias gerekli}"
 : "${ITME_KEYSTORE_PASSWORD:?Keystore parolası gerekli}"
 : "${ITME_KEY_PASSWORD:?Anahtar parolası gerekli}"
fi
mkdir -p "$project_root/Builds/Logs"
"$unity_editor" -batchmode -quit -projectPath "$project_root" -buildTarget Android -executeMethod "$method" -logFile "$project_root/Builds/Logs/p31-$mode.log"
