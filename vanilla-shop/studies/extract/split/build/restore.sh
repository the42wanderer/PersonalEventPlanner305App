#!/bin/bash
# Rebuilds the scratch layout the label scripts expect, from the copies in the repo.
# Usage: bash restore.sh <scratchpad dir>    (the scripts hard-code the old session's scratchpad path in T/CF;
#        pass that path, or edit T in splitwrap.py, kit.py, mock.py and proofpdf2.mjs to the new one)
set -e
S=${1:?scratchpad dir}; H=$(cd "$(dirname "$0")" && pwd); SPLIT=$H/..
mkdir -p $S/ext/d $S/ext/w $S/ext/n $S/candlefonts
cp $SPLIT/splitwrap.py $SPLIT/mock.py $SPLIT/proofpdf2.mjs $SPLIT/draw.py $SPLIT/comp.py $SPLIT/green.py $SPLIT/podstyles.py $S/ext/d/
cp $SPLIT/marks/*.png $H/wart-0*.png $H/shot.mjs $H/pdf.mjs $S/ext/d/
cp $H/kit.py $H/content.py $S/ext/w/
cp $H/bottle2.py $SPLIT/bottle3.py $S/ext/n/
# Roc Grotesk is a demo font from the user's zip and is not committed; re-upload roc-grotesk-font-family.zip and unzip it
Z=$(ls /root/.claude/uploads/*/*roc-grotesk-font-family.zip 2>/dev/null | head -1 || true)
if [ -n "$Z" ]; then
  T=$(mktemp -d); unzip -q -o "$Z" -d $T
  for p in "rocgrotesk-regular:roc-regular" "rocgrotesk-bold:roc-bold" "rocgroteskwide-regular:roc-wide-regular" "rocgroteskwide-medium:roc-wide-medium"; do
    cp "$T/Fontspring-DEMO-${p%%:*}.otf" "$S/candlefonts/${p##*:}.otf"; done
else echo "Roc Grotesk zip not found: upload it, then re-run (fonts go in $S/candlefonts)"; fi
echo "restored to $S"
