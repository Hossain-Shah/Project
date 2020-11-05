import markdown
md = markdown.Markdown()
print(md.convert("# sample heading text"))
print(md.convert("## sample sub-heading text"))
print(md.convert("### sample deep heading text"))
print(md.convert("*sample italicized text*"))
print(md.convert("**sample bold text**"))
print(md.convert("[sample link text](kite.com)"))
