from weasyprint import HTML

html = HTML(string="""
<html><body>
<h1 style="color:green;">WeasyPrint werkt!</h1>
<p>PDF gegenereerd vanuit inline HTML string</p>
</body></html>
""")
html.write_pdf("tests/inline_test.pdf")

print("✅ PDF gegenereerd als test/inline_test.pdf")

