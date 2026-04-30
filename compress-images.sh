#!/bin/bash
# ═══════════════════════════════════════════════════════════════════════
#  compress-images.sh — Bulk-optimize all images for La Table Marrakech
# ═══════════════════════════════════════════════════════════════════════
#
#  USAGE (Mac Terminal, from your website folder):
#      bash compress-images.sh             # apply
#      bash compress-images.sh --dry-run   # preview only
#
#  REQUIREMENTS:
#      brew install webp imagemagick
#
#  Originals are backed up to ./images-original-backup/ before being replaced.
# ═══════════════════════════════════════════════════════════════════════

set -e

DRY_RUN=false
[[ "$1" == "--dry-run" ]] && DRY_RUN=true

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
BLUE='\033[0;34m'; BOLD='\033[1m'; DIM='\033[2m'; NC='\033[0m'

THRESHOLD_KB=200
MAX_WIDTH=1920
QUALITY=80
BACKUP_DIR="./images-original-backup"

echo ""
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}${BLUE}  🖼  Bulk Image Optimizer · La Table Marrakech${NC}"
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo "  Threshold: ${THRESHOLD_KB} KB"
echo "  Max width: ${MAX_WIDTH} px"
echo "  Quality:   ${QUALITY}"
echo "  Mode:      $([[ $DRY_RUN == true ]] && echo 'DRY RUN' || echo 'WRITE')"
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"

if ! command -v cwebp &> /dev/null; then
  echo -e "${RED}❌ cwebp not installed. Run: brew install webp${NC}"
  exit 1
fi

if ! command -v identify &> /dev/null; then
  echo -e "${YELLOW}⚠  ImageMagick not installed (resize will be skipped). Run: brew install imagemagick${NC}"
  USE_IM=false
else
  USE_IM=true
fi

[[ $DRY_RUN == false ]] && mkdir -p "$BACKUP_DIR"

processed=0
saved_kb=0

while IFS= read -r -d '' file; do
  size_kb=$(($(stat -f%z "$file") / 1024))
  [[ $size_kb -lt $THRESHOLD_KB ]] && continue

  [[ "$file" == *images-original-backup* ]] && continue
  [[ "$file" == *node_modules* ]] && continue
  [[ "$file" == *.git* ]] && continue

  rel="${file#./}"
  ext="${file##*.}"
  base="${file%.*}"
  output="${base}.webp"

  echo ""
  echo -e "${BOLD}  📷 ${rel}${NC}  ${DIM}(${size_kb} KB)${NC}"

  if [[ $DRY_RUN == true ]]; then
    echo -e "     ${DIM}would compress → ${output}${NC}"
    continue
  fi

  backup_path="${BACKUP_DIR}/${rel}"
  mkdir -p "$(dirname "$backup_path")"
  cp -p "$file" "$backup_path"

  if [[ $USE_IM == true ]]; then
    img_width=$(identify -format "%w" "$file" 2>/dev/null || echo "0")
  else
    img_width=0
  fi

  if [[ "$ext" == "webp" ]]; then
    cwebp -q $QUALITY -resize $([[ $img_width -gt $MAX_WIDTH ]] && echo "$MAX_WIDTH 0" || echo "0 0") \
          "$file" -o "${file}.tmp" 2>/dev/null
    mv "${file}.tmp" "$file"
    final="$file"
  else
    if [[ $img_width -gt $MAX_WIDTH ]]; then
      cwebp -q $QUALITY -resize $MAX_WIDTH 0 "$file" -o "$output" 2>/dev/null
    else
      cwebp -q $QUALITY "$file" -o "$output" 2>/dev/null
    fi
    rm "$file"
    final="$output"
  fi

  new_size_kb=$(($(stat -f%z "$final") / 1024))
  diff_kb=$((size_kb - new_size_kb))
  saved_kb=$((saved_kb + diff_kb))
  processed=$((processed + 1))

  echo -e "     ${GREEN}✓${NC} ${size_kb} KB → ${new_size_kb} KB  ${DIM}(saved ${diff_kb} KB)${NC}"

done < <(find . -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.png" -o -iname "*.webp" \) -print0)

echo ""
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo -e "${BOLD}  📊 Results${NC}"
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo "  Files compressed: $processed"
echo "  Total saved:      ${saved_kb} KB ($((saved_kb / 1024)) MB)"
echo ""
if [[ $DRY_RUN == true ]]; then
  echo -e "  ${YELLOW}💡 Re-run without --dry-run to apply.${NC}"
else
  echo -e "  ${GREEN}✅ Done!${NC}"
  echo ""
  echo "  Originals backed up to: ${BACKUP_DIR}"
fi
echo -e "${BOLD}${BLUE}═══════════════════════════════════════════════════════════════${NC}"
echo ""
