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
    Llegeix un fitxer de text (com index.md o qualsevol altre fitxer de la wiki)
    i converteix tots els enllaços absoluts de wikis de GitHub en enllaços relatius locals de MkDocs.
    """
    if not os.path.exists(file_path):
        return

    print(f"Corregint enllaços a: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Aquest patró millorat detecta qualsevol enllaç que acabi a la wiki de GitHub de qualsevol usuari
    # i extreu només el nom del fitxer final (fins a trobar el tancament de parèntesi ')')
    pattern = r'https://github\.com/[^/]+/[^/]+/wiki/([^)\s]+)'
    
    # Substituïm la URL de GitHub per: nom-del-fitxer.md
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
    
    # Netejar completament la carpeta destí abans de copiar per assegurar-nos de fer neteja del sidebar antic
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
        
        # Ignorem la carpeta interna de git, fitxers de sistema i QUALSEVOL variació de Sidebar (minúscules/majúscules)
        if item == ".git" or "sidebar" in item.lower() or item.startswith('.'):
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

    # --- CORRECCIÓ DE TOTS ELS FITXERS ---
    # Ara l'script fa una passada per tots els fitxers .md de la carpeta 'module-1'
    # i corregeix els enllaços a tot arreu, no només a index.md!
    for filename in os.listdir(DEST_DIR):
        if filename.endswith(".md"):
            file_path = os.path.join(DEST_DIR, filename)
            fix_wiki_links(file_path)
    
    # Netegem la carpeta temporal
    shutil.rmtree(TEMP_DIR)
    print(f"Sincronització completada! {copied_count} elements copiats, sidebars eliminats i enllaços corregits a tot arreu.")

if __name__ == "__main__":
    sync_wiki()
