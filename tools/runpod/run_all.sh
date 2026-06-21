#!/usr/bin/env bash
# ============================================================================
# YAWatch-LUNA — Pipeline complet pod (provision + comparaison FramePack/Wan)
# ----------------------------------------------------------------------------
# Tout-en-un, détachable, journalisé. Conçu pour être lancé depuis le terminal
# web RunPod quand le SSH automatisé n'est pas disponible :
#
#   setsid bash tools/runpod/run_all.sh > /workspace/run_all.log 2>&1 < /dev/null &
#
# Suivi :   tail -f /workspace/run_all.log
# Fin OK :  la ligne "ALL_DONE" apparaît, suivie des 2 rapports Quality Gate.
# ============================================================================
set -o pipefail
cd "$(dirname "$0")/../.." || exit 1
ROOT="$(pwd)"
LOG() { echo -e "\n========== $* ($(date '+%H:%M:%S')) =========="; }

LOG "PROVISION"
bash tools/runpod/provision.sh
if [ $? -ne 0 ]; then echo "❌ PROVISION_FAILED — arrêt avant génération."; exit 1; fi

LOG "GÉNÉRATION FRAMEPACK"
/usr/local/bin/python tools/runpod/runner.py --engine framepack
echo "FRAMEPACK_RC=$?"

LOG "GÉNÉRATION WAN21 (natif fp16)"
/usr/local/bin/python tools/runpod/runner.py --engine wan21
echo "WAN21_RC=$?"

LOG "RAPPORTS QUALITY GATE I2V"
for f in /workspace/outputs/*.i2v_quality_gate.json; do
  [ -f "$f" ] && { echo "----- $f -----"; cat "$f"; echo; }
done

LOG "CLIPS PRODUITS"
ls -lh /workspace/outputs/*.mp4 2>/dev/null || echo "(aucun MP4 — voir erreurs ci-dessus)"

LOG "ALL_DONE"
