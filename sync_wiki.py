import os
import shutil
import subprocess

# 1. Configuració de rutes
REPO_WIKI_URL = "https://github.com/MTUOC-course/Module-1.-Deployment-Integration-and-Evaluation.wiki.git"
TEMP_DIR = "temp_wiki_mod1"
DEST_DIR = os.path.join("docs", "module-1")

def sync_wiki():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        
    print(f"Descarregant la Wiki externa des de: {REPO_WIKI_URL}...")
    try:
        subprocess.run(["git", "clone", REPO_WIKI_URL, TEMP_DIR], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error en clonar la Wiki: {e}")
        return

    os.makedirs(DEST_DIR, exist_ok=True)
    
    # Netejar la carpeta destí
    for filename in os.listdir(DEST_DIR):
        file_path = os.path.join(DEST_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    print("Copiant fitxers de la Wiki al mòdul 1...")
    copied_count = 0
    for item in os.listdir(TEMP_DIR):
        s = os.path.join(TEMP_DIR, item)
        d = os.path.join(DEST_DIR, item)
        
        if item == ".git":
            continue
            
        if os.path.isdir(s):
            shutil.copytree(s, d)
            copied_count += 1
        else:
            shutil.copy2(s, d)
            copied_count += 1

    # --- TRUC PER A MKDOCS ---
    # Busquem "home.md" o "Home.md" per reanomenar-lo a "index.md"
    home_file = None
    for filename in os.listdir(DEST_DIR):
        if filename.lower() == "home.md":
            home_file = filename
            break

    if home_file:
        old_path = os.path.join(DEST_DIR, home_file)
        new_path = os.path.join(DEST_DIR, "index.md")
        os.rename(old_path, new_path)
        print(f"S'ha reanomenat '{home_file}' a 'index.md' correctament.")
    
    # Esborrem el fitxer "_Sidebar.md" si existeix (no el necessitem a la web)
    sidebar_path = os.path.join(DEST_DIR, "_Sidebar.md")
    if os.path.exists(sidebar_path):
        os.remove(sidebar_path)
        print("S'ha eliminat el fitxer '_Sidebar.md' de la Wiki per evitar problemes visual.")
    # -------------------------

    shutil.rmtree(TEMP_DIR)
    print(f"Sincronització completada! {copied_count} elements copiats.")

if __name__ == "__main__":
    sync_wiki()
