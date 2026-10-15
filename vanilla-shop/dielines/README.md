# Dielines for other Vanilla Shop products

Drop one folder per product here, e.g. `dielines/vanilla-extract-100ml/`.

In each folder, put:

1. **The dieline** as a PDF (or AI/SVG), cut and fold lines only if possible.
   Delete artwork layers in Illustrator and save with "Preserve Illustrator Editing
   Capabilities" unticked; that keeps it small. Web upload limit is 25 MB per file.
2. **A photo or PDF of the current pack** (optional, but helps with copy and legal text).
3. **`info.txt`** with whatever you know:
   - Product name as it should read (e.g. "Natural Vanilla Extract")
   - Size / net content (e.g. 100 ml, 50 g, 25 bags)
   - Barcode number (GTIN), if it has one
   - Ingredients, storage, usage instructions
   - Anything the pack must carry (logos, certifications, warnings)
   - Which panel is the front, if it isn't obvious

Upload to branch `claude/vanilla-shop-redesign-kwnfzk` (not main):
GitHub → switch branch → open `vanilla-shop/dielines/` → Add file → Upload files.
To create a product folder in the web upload, type the folder name followed by `/`
in the file name box, or drag a whole folder in.

Existing dielines (for reference):
- Tea cube, 12 bags: `research/` source 2.pdf, generator `dieline.js`
- Tea long box, 25 bags: `research/dieline-long-25bag.pdf`, generator `dieline-long.js`
