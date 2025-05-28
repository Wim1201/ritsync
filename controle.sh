#!/bin/bash

echo "📁 Start controle- en herstelscript voor RitSync-structuur..."

# 1. __init__.py in backend/ en backend/routes/
touch backend/__init__.py
touch backend/routes/__init__.py

# 2. Verplaats routes_pdf.py als die verkeerd staat
if [ -f routes_pdf.py ]; then
  echo "⚠️  routes_pdf.py stond fout, wordt verplaatst naar backend/routes/"
  mv routes_pdf.py backend/routes/
fi

# 3. Verplaats ocr_upload_route.py als die fout staat
if [ -f ocr_upload_route.py ]; then
  echo "⚠️  ocr_upload_route.py stond fout, wordt verplaatst naar backend/routes/"
  mv ocr_upload_route.py backend/routes/
fi

# 4. Controleer of main.js in frontend/static/js zit
if [ ! -f frontend/static/js/main.js ]; then
  echo "⚠️  Waarschuwing: main.js ontbreekt in frontend/static/js/"
else
  echo "✅ main.js correct geplaatst"
fi

# 5. Verwijder onnodige routes_pdf.py-bestanden
find . -name "routes_pdf.py" ! -path "./backend/routes/routes_pdf.py" -exec rm {} \;

# 6. Toon samenvatting
echo "📂 Structuur na herstel:"
find . -type f \( -name "*.py" -o -name "*.html" -o -name "*.js" \) | sort

echo "✅ Structuurcontrole afgerond. Start nu de server met: python app.py"
