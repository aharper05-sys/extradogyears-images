# Usage: python3 make_reel.py out.mp4 "slide.jpg:seconds:BGHEX" ...
import sys,subprocess,os,tempfile
out=sys.argv[1]; items=[a.split(":") for a in sys.argv[2:]]; t=0.4
d=tempfile.mkdtemp(); segs=[]
for i,(img,sec,col) in enumerate(items):
    fr=int(float(sec)*30); seg=f"{d}/s{i}.mp4"; segs.append((seg,float(sec)))
    vf=(f"format=rgb24,scale=2160:2700,zoompan=z='1+0.035*on/{fr}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={fr}:s=1080x1350:fps=30,"
        f"pad=1080:1920:0:285:color=0x{col},format=yuv420p")
    subprocess.run(["ffmpeg","-y","-loglevel","error","-loop","1","-framerate","30","-i",img,"-vf",vf,"-frames:v",str(fr),
                    "-c:v","libx264","-preset","veryfast","-crf","18",seg],check=True)
parts=[];prev="[0:v]";off=0
for i in range(1,len(segs)):
    off+=segs[i-1][1]-t; o=f"[v{i}]"
    parts.append(f"{prev}[{i}:v]xfade=transition=fade:duration={t}:offset={off:.2f}{o}"); prev=o
cmd=["ffmpeg","-y","-loglevel","error"]
for s,_ in segs: cmd+=["-i",s]
cmd+=["-filter_complex",";".join(parts),"-map",prev,"-c:v","libx264","-preset","veryfast","-crf","20","-pix_fmt","yuv420p","-movflags","+faststart","-r","30",out]
subprocess.run(cmd,check=True); print("ok",out)
