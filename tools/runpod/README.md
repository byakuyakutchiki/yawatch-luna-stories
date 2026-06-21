# Atelier vidéo cloud YAWatch-LUNA — config persistante (RunPod)

Objectif : générer les clips d'épisodes sur GPU cloud **sans re-télécharger les
modèles à chaque fois** et **sans bricolage**. La clé = un **volume réseau
persistant** réutilisé entre les pods.

## Principe : 1 volume persistant, N pods jetables

Les ~46 Go de modèles vivent sur un **network volume nommé** monté sur
`/workspace`. On télécharge **une seule fois**. Ensuite on démarre/arrête des
pods à volonté : le volume (donc les modèles) reste. Un pod arrêté ne coûte
presque rien ; un volume persiste.

> **Stop** (jamais **Terminate/Delete**) le pod après chaque session.
> Ne JAMAIS supprimer le network volume (= les modèles).

## Déploiement d'un pod

- Template : **runpod/pytorch** (SSH TCP direct fonctionne dessus).
- GPU conseillé : **RTX 6000 Ada** (48 Go, rapide, ~0,77 $/h) ou L40S.
- **Network volume : ≥ 80 Go** (FramePack 16 + Wan 14 + encoders ≈ 46 Go ; marge).
- Cocher **SSH terminal access**.

## Première fois sur un volume neuf (~15 min, une seule fois)

```bash
cd /workspace
git clone --depth 1 --branch feat/governed-i2v-engines \
  https://github.com/byakuyakutchiki/yawatch-luna-stories.git
bash yawatch-luna-stories/tools/runpod/provision.sh   # installe ComfyUI + nodes + modèles
```

`provision.sh` est **idempotent** : un fichier déjà complet (taille ==
Content-Length serveur) est sauté. Téléchargements en **curl + vérification de
taille** (rejette toute troncature — leçon du 21 juin).

## Sessions suivantes (modèles déjà là — rapide)

```bash
cd /workspace/yawatch-luna-stories && git pull
/usr/local/bin/python tools/runpod/runner.py --engine framepack   # ~5 min
/usr/local/bin/python tools/runpod/runner.py --engine wan21       # ~5 min
```

Récupérer les clips/rapports (depuis la machine locale, SCP en TCP direct) :
```bash
scp -P <port> -i ~/.ssh/id_ed25519 root@<ip>:/workspace/outputs/*.mp4  ~/Downloads/
```

## Accès

- **SSH TCP direct** (onglet Connect → « SSH over exposed TCP ») : propre, non
  interactif, supporte SCP. À privilégier.
- Repli si le TCP direct est refusé : passerelle `ssh -tt <user>@ssh.runpod.io`
  pilotée via stdin (`printf 'cmd\nexit\n' | ssh -tt ...`).

## Gotchas (corrigés / à retenir)

- Téléchargement : **curl simple**, jamais `wget -c` ni `curl -C -` (ils
  tronquent le fichier à 0 sur ralentissement → modèle corrompu).
- Vérifier la complétude par **Content-Length**, pas par une taille mini fixe.
- Volume < 50 Go = quota dépassé en plein download → prendre **≥ 80 Go**.
- Les deux moteurs ne tiennent pas si le volume est trop petit : sinon
  supprimer les modèles du moteur non utilisé (le clip généré est déjà sauvé).
- Pods communautaires : peuvent être préemptés → lancer en détaché
  (`nohup setsid ... </dev/null &`) et le volume encaisse les redémarrages.
