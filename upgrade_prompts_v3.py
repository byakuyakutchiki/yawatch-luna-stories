"""Passe les prompts en V3 avec des noms de fichiers distincts."""

from pathlib import Path

input_path = Path("PROMPTS_10_ONGLETS_PRODUCTION_RAPIDE_V2.md")
output_path = Path("PROMPTS_10_ONGLETS_PRODUCTION_RAPIDE_V3.md")

text = input_path.read_text(encoding="utf-8")

# Changer le titre
text = text.replace(
    "# Prompts 10 Onglets — Production Rapide V2",
    "# Prompts 10 Onglets — Production Rapide V3\n\n> Cette version V3 utilise des noms de fichiers distincts (`_v3_01`) pour ne pas écraser les images V2 déjà validées et poussées sur GitHub."
)

# Changer les noms cibles _01.png en _v3_01.png pour différencier
# On ne change que les lignes "Nom cible : ..._01.png"
lines = text.split("\n")
new_lines = []
for line in lines:
    if line.startswith("Nom cible :") and "_01.png" in line:
        line = line.replace("_01.png", "_v3_01.png")
    new_lines.append(line)

text = "\n".join(new_lines)

output_path.write_text(text, encoding="utf-8")
print(f"Fichier V3 mis à jour : {output_path}")
