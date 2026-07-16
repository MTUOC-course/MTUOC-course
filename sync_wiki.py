import os
import shutil
import subprocess
import re

# 1. Configuració de rutes de la Wiki del Mòdul 1
REPO_WIKI_URL = "https://github.com/MTUOC-course/Module-1.-Deployment-Integration-and-Evaluation.wiki.git"
TEMP_DIR = "temp_wiki_mod1"
DEST_DIR = os.path.join("docs", "module-1")

def fix_wiki_links(file_path):
    """
    Llegeix el fitxer (com index.md) i converteix els enllaços absoluts de la Wiki de GitHub
    en enllaços relatius locals perquè MkDocs els obri dins de la teva pròpia web.
    """
    if not os.path.exists(file_path):
        return

    print(f"Corregint enllaços absoluts de la Wiki a {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Aquest patró detecta qualsevol enllaç que contingui '/wiki/Nom-Del-Fitxer'
    # de qualsevol repositori de GitHub (com MTUOC-course o mtuoc/EAMT2026-Tutorial)
    pattern = r'https://github\.com/[^/]+/[^/]+/wiki/([^)\s]+)'
    
    # Substituïm la URL web pel nom del fitxer local amb l'extensió .md
    # Exemple: [OpusMT](https://github.com/.../wiki/2.1.-OpusMT) -> [OpusMT](2.1.-OpusMT.md)
    fixed_content = re.sub(pattern, r'\1.md', content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(fixed_content)

def sync_wiki():
    # Netejar directori temporal si existia d'un intent fallit
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
        
    print(f"Descarregant la Wiki externa des de: {REPO_WIKI_URL}...")
    try:
        subprocess.run(["git", "clone", REPO_WIKI_URL, TEMP_DIR], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error en clonar la Wiki: {e}")
        return

    os.makedirs(DEST_DIR, exist_ok=True)
    
    # Netejar la carpeta destí abans de copiar els fitxers nous
    for filename in os.listdir(DEST_DIR):
        file_path = os.path.join(DEST_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)

    print("Copiant els fitxers de la Wiki...")
    copied_count = 0
    for item in os.listdir(TEMP_DIR):
        s = os.path.join(TEMP_DIR, item)
        d = os.path.join(DEST_DIR, item)
        
        # Ignorem la carpeta interna de git, el Sidebar i fitxers de sistema
        if item == ".git" or item == "_Sidebar.md" or item.startswith('.'):
            continue
            
        if os.path.isdir(s):
            shutil.copytree(s, d)
            copied_count += 1
        else:
            shutil.copy2(s, d)
            copied_count += 1

    # --- TRACTAMENT DE LA PORTADA ---
    # Busquem el fitxer "home.md" o "Home.md" per reanomenar-lo obligatòriament a "index.md"
    home_file = None
    for filename in os.listdir(DEST_DIR):
        if filename.lower() == "home.md":
            home_file = filename
            break

    if home_file:
        old_path = os.path.join(DEST_DIR, home_file)
        new_path = os.path.join(DEST_DIR, "index.md")
        if os.path.exists(new_path):
            os.remove(new_path)
        os.rename(old_path, new_path)
        print(f"S'ha reanomenat '{home_file}' a 'index.md' correctament.")
        
        # Corregim els enllaços del fitxer de portada perquè es quedin a la teva web de Pages
        fix_wiki_links(new_path)
    
    # Netegem la carpeta temporal per deixar el repositori polit
    shutil.rmtree(TEMP_DIR)
    print(f"Sincronització completada! {copied_count} elements copiats i enllaços corregits.")

if __name__ == "__main__":
    sync_wiki()
