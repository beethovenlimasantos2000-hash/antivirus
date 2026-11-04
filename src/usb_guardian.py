#!/usr/bin/env python3
"""USB Guardian: diagnóstico USB e triagem local de arquivos, somente leitura."""
import shutil, subprocess, threading, tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
APP_VERSION="1.0.0"; BG="#0b1220"; PANEL="#111c2e"; CARD="#17243a"; TEXT="#e5edf8"; MUTED="#91a4bd"; ACCENT="#4da3ff"; GREEN="#38d996"; AMBER="#f5b942"
def read_text(path):
    try: return Path(path).read_text(errors="replace").strip()
    except OSError: return ""
def usb_devices():
    found=[]; root=Path("/sys/bus/usb/devices")
    if root.exists():
        for p in sorted(root.iterdir()):
            v=read_text(p/"idVendor"); pid=read_text(p/"idProduct")
            if not v or not pid: continue
            found.append(dict(name=read_text(p/"product") or "Dispositivo USB", manufacturer=read_text(p/"manufacturer") or "Não informado", vidpid=f"{v.upper()}:{pid.upper()}", serial=read_text(p/"serial") or "Não disponibilizado", bus=read_text(p/"busnum") or "?", devnum=read_text(p/"devnum") or "?", speed=read_text(p/"speed") or "?", cls=read_text(p/"bDeviceClass") or "?", path=str(p)))
    return found
class Guardian(tk.Tk):
    def __init__(self):
        super().__init__(); self.title("USB Guardian — Diagnóstico e Segurança"); self.geometry("1040x700"); self.minsize(860,600); self.configure(bg=BG); self.devices=[]; self.style_ui(); self.build(); self.refresh()
    def style_ui(self):
        s=ttk.Style(self); s.theme_use("clam"); s.configure("Treeview",background=CARD,foreground=TEXT,fieldbackground=CARD,rowheight=30,borderwidth=0,font=("Arial",10)); s.configure("Treeview.Heading",background="#20334f",foreground=TEXT,font=("Arial",10,"bold"),relief="flat"); s.map("Treeview",background=[("selected","#24558a")])
    def label(self,p,t,size=10,color=TEXT,bold=False): return tk.Label(p,text=t,bg=p.cget("bg"),fg=color,font=("Arial",size,"bold" if bold else "normal"))
    def button(self,p,t,cmd,color=ACCENT): return tk.Button(p,text=t,command=cmd,bg=color,fg="#07111f",activebackground=color,relief="flat",bd=0,padx=14,pady=9,font=("Arial",10,"bold"),cursor="hand2")
    def build(self):
        h=tk.Frame(self,bg="#101d31",padx=24,pady=18); h.pack(fill="x"); tk.Label(h,text="◈  USB GUARDIAN",bg="#101d31",fg=TEXT,font=("Arial",20,"bold")).pack(side="left"); tk.Label(h,text="DIAGNÓSTICO • USB • SEGURANÇA",bg="#101d31",fg=MUTED,font=("Arial",9,"bold")).pack(side="right")
        b=tk.Frame(self,bg=BG,padx=22,pady=18); b.pack(fill="both",expand=True); self.label(b,"Central de dispositivos",17,TEXT,True).pack(anchor="w"); self.label(b,"Identifique o hardware enumerado pelo Linux e execute verificações sem modificar o aparelho.",10,MUTED).pack(anchor="w",pady=(5,14))
        a=tk.Frame(b,bg=BG); a.pack(fill="x",pady=(0,12)); self.button(a,"↻  Procurar dispositivos",self.refresh).pack(side="left"); self.button(a,"⌕  Analisar arquivos",self.choose,GREEN).pack(side="left",padx=9); self.button(a,"Diagnóstico do ambiente",self.report,AMBER).pack(side="left")
        panel=tk.Frame(b,bg=PANEL,padx=14,pady=14); panel.pack(fill="both",expand=True); top=tk.Frame(panel,bg=PANEL); top.pack(fill="x",pady=(0,10)); self.label(top,"DISPOSITIVOS ENCONTRADOS",10,TEXT,True).pack(side="left"); self.count=self.label(top,"0 encontrados",9,MUTED); self.count.pack(side="right")
        cols=("name","manufacturer","vidpid","speed","bus"); self.table=ttk.Treeview(panel,columns=cols,show="headings",height=8)
        for c,t,w in [("name","Nome do aparelho",260),("manufacturer","Fabricante",210),("vidpid","VID:PID",110),("speed","Velocidade",100),("bus","Barramento",90)]: self.table.heading(c,text=t); self.table.column(c,width=w,anchor="w")
        self.table.pack(fill="both",expand=True); self.table.bind("<<TreeviewSelect>>",self.details_view)
        low=tk.Frame(b,bg=BG); low.pack(fill="x",pady=(14,0)); l=tk.Frame(low,bg=PANEL,padx=14,pady=12); l.pack(side="left",fill="both",expand=True,padx=(0,7)); self.label(l,"DETALHES DO DISPOSITIVO",10,TEXT,True).pack(anchor="w"); self.detail=tk.Text(l,height=6,bg=CARD,fg=TEXT,relief="flat",wrap="word",font=("Courier New",9),padx=9,pady=8); self.detail.pack(fill="both",expand=True,pady=(8,0)); self.detail.insert("1.0","Selecione um dispositivo para visualizar detalhes."); self.detail.configure(state="disabled")
        r=tk.Frame(low,bg=PANEL,padx=14,pady=12); r.pack(side="left",fill="both",expand=True,padx=(7,0)); self.label(r,"RELATÓRIO E SEGURANÇA",10,TEXT,True).pack(anchor="w"); self.log=tk.Text(r,height=6,bg=CARD,fg=MUTED,relief="flat",wrap="word",font=("Arial",9),padx=9,pady=8); self.log.pack(fill="both",expand=True,pady=(8,0)); self.log.configure(state="disabled")
        foot=tk.Frame(b,bg=BG); foot.pack(fill="x",pady=(12,0)); self.status=self.label(foot,"● Sistema pronto",9,GREEN); self.status.pack(side="left"); self.label(foot,f"Versão {APP_VERSION} • Linux x86-64",9,MUTED).pack(side="right")
    def logline(self,msg):
        self.log.configure(state="normal"); self.log.insert("end",msg+"\n"); self.log.see("end"); self.log.configure(state="disabled")
    def refresh(self):
        self.status.configure(text="● Consultando barramento USB...",fg=AMBER); self.update_idletasks(); self.devices=usb_devices()
        for row in self.table.get_children(): self.table.delete(row)
        for i,d in enumerate(self.devices): self.table.insert("","end",iid=str(i),values=(d["name"],d["manufacturer"],d["vidpid"],d["speed"]+" Mb/s",d["bus"]))
        self.count.configure(text=f"{len(self.devices)} encontrado(s)"); self.status.configure(text="● Busca concluída",fg=GREEN); self.logline(f"Busca USB: {len(self.devices)} dispositivo(s) enumerado(s).")
        if not self.devices: self.logline("Nada visível ao Linux. Verifique Configurações do ChromeOS > Linux > Gerenciar acesso USB.")
    def details_view(self,_=None):
        sel=self.table.selection()
        if not sel:return
        d=self.devices[int(sel[0])]; txt="\n".join([f"Nome: {d['name']}",f"Fabricante: {d['manufacturer']}",f"VID:PID: {d['vidpid']}",f"Número de série: {d['serial']}",f"Barramento/dispositivo: {d['bus']}/{d['devnum']}",f"Velocidade: {d['speed']} Mb/s",f"Classe USB: {d['cls']}",f"Sysfs: {d['path']}"])
        self.detail.configure(state="normal"); self.detail.delete("1.0","end"); self.detail.insert("1.0",txt); self.detail.configure(state="disabled")
    def report(self):
        self.logline("Diagnóstico do ambiente:")
        for n in ("lsusb","clamscan","udevadm"): self.logline(f"  {n}: {shutil.which(n) or 'não instalado'}")
        self.logline(f"  Dispositivos USB em sysfs: {len(self.devices)}"); self.logline("  Operação somente leitura; nenhuma gravação no dispositivo.")
    def choose(self):
        paths=filedialog.askopenfilenames(title="Selecione arquivos para análise")
        if paths: threading.Thread(target=self.scan,args=(list(paths),),daemon=True).start()
    def scan(self,paths):
        scanner=shutil.which("clamscan"); self.after(0,lambda:self.status.configure(text="● Analisando arquivos...",fg=AMBER))
        for raw in paths:
            p=Path(raw)
            try:
                if scanner:
                    result=subprocess.run([scanner,"--no-summary",str(p)],capture_output=True,text=True,timeout=120); lines=(result.stdout or result.stderr).strip().splitlines(); msg=lines[-1] if lines else f"{p.name}: sem saída"
                    self.after(0,lambda m=msg:self.logline("ClamAV: "+m))
                else:
                    risky=p.suffix.lower() in {".exe",".dll",".scr",".bat",".cmd",".ps1",".vbs",".js",".jar",".apk"}
                    msg=f"{p.name}: extensão executável/script; análise por assinaturas recomendada" if risky else f"{p.name}: sem alerta por extensão (não comprova segurança)"
                    self.after(0,lambda m=msg:self.logline("Heurística: "+m))
            except Exception as e:self.after(0,lambda m=str(e):self.logline("Erro: "+m))
        self.after(0,lambda:self.status.configure(text="● Análise concluída",fg=GREEN))
if __name__=="__main__": Guardian().mainloop()
