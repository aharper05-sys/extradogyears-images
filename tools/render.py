# Usage: python3 render.py <project_dir> <out_dir> Name1 Name2 ...
import sys,re,asyncio,os
from playwright.async_api import async_playwright
P,O,names=sys.argv[1],sys.argv[2],sys.argv[3:]
F=os.path.join(os.path.dirname(os.path.abspath(__file__)),"fonts")
FACES=(f"@font-face{{font-family:'Fraunces';src:url('file://{F}/Fraunces.ttf');font-weight:100 900}}"
       f"@font-face{{font-family:'DM Sans';src:url('file://{F}/DMSans.ttf');font-weight:100 1000}}")
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1243/chrome-linux64/chrome")
        pg=await b.new_page(viewport={"width":1080,"height":1350},device_scale_factor=2)
        for n in names:
            s=open(f"{P}/{n}.dc.html").read()
            body=re.search(r"</helmet>(.*)</x-dc>",s,re.S).group(1)
            html=f"<html><head><style>{FACES}body{{margin:0}}[style*='DM Sans'],[style*='DM Sans'] *{{font-variation-settings:'opsz' 14}}[style*='Fraunces']{{font-variation-settings:normal}}</style></head><body>{body}</body></html>"
            tmp=f"{O}/_{n}.html"; open(tmp,"w").write(html)
            await pg.goto("file://"+tmp); await pg.evaluate("document.fonts.ready")
            h=await pg.evaluate("document.body.firstElementChild.scrollHeight")
            if h>1350: print("OVERFLOW",n,h)
            await pg.screenshot(path=f"{O}/{n}.png",clip={"x":0,"y":0,"width":1080,"height":1350})
            os.remove(tmp)
        await b.close()
asyncio.run(main())
