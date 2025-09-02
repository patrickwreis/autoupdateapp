import tkinter as tk
import subprocess
import sys
import os
import requests

# Versão atual do app
CURRENT_VERSION = "1.0.0"

def check_github_release_update():
    repo = "patrickwreis/autoupdateapp"
    api_url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        latest_version = data["tag_name"]
        if latest_version != CURRENT_VERSION:
            print(f"Nova versão disponível: {latest_version}. Baixando...")
            # Procura o asset .exe
            exe_asset = None
            for asset in data.get("assets", []):
                if asset["name"].endswith(".exe"):
                    exe_asset = asset["browser_download_url"]
                    break
            if exe_asset:
                exe_name = "autoupdateapp_new.exe"
                r = requests.get(exe_asset)
                with open(exe_name, "wb") as f:
                    f.write(r.content)
                print("Atualização baixada. Reiniciando...")
                os.startfile(exe_name)
                sys.exit()
            else:
                print("Nenhum arquivo .exe encontrado na release.")
        else:
            print("Nenhuma atualização disponível.")
    except Exception as e:
        print(f"Erro ao verificar atualização: {e}")

check_github_release_update()

REPO_PATH = os.path.dirname(os.path.abspath(__file__))

class HelloWorldApp:
    def __init__(self, root):
        self.root = root
        root.title("Hello World - Git AutoUpdate")
        self.label = tk.Label(root, text="Hello World!", font=("Arial", 16))
        self.label.pack(pady=20)
        self.update_btn = tk.Button(root, text="Verificar atualização (Git)", command=self.check_for_update)
        self.update_btn.pack(pady=10)
        self.status = tk.Label(root, text="", fg="blue")
        self.status.pack(pady=5)

    def check_for_update(self):
        self.status.config(text="Verificando atualizações no Git...")
        self.root.update()
        try:
            # Busca por novas atualizações
            subprocess.run(["git", "fetch"], cwd=REPO_PATH)
            local = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPO_PATH).strip()
            remote = subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=REPO_PATH).strip()
            if local != remote:
                self.status.config(text="Nova versão encontrada! Atualizando...")
                self.root.update()
                self.update_app()
            else:
                self.status.config(text="Você já está na última versão.")
        except Exception as e:
            self.status.config(text=f"Erro: {e}")

    def update_app(self):
        try:
            subprocess.run(["git", "pull"], cwd=REPO_PATH)
            self.status.config(text="Atualização concluída. Reinicie o app.")
            self.root.update()
            self.root.after(2000, self.root.quit)
        except Exception as e:
            self.status.config(text=f"Erro ao atualizar: {e}")

def main():
    root = tk.Tk()
    app = HelloWorldApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
