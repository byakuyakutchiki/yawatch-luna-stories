# I2V_ENGINE — MATRICE DE DÉCISION

> **Document de sélection stratégique.**
> Aucune option ne doit être choisie avant lecture complète.
> La décision finale appartient à Ludovic.
> Ce document ne nomme pas d'outil par défaut — il fournit les données pour décider sans dériver.

**Date :** 2026-06-20  
**Référence :** `YAWATCH_LUNA_FACTORY_MASTER_PLAN.md` — Partie 7  
**Statut Kling :** exclu définitivement (décision 2026-06-20) — mentionné uniquement comme référence historique rejetée

---

## 1. Contraintes réelles du projet

Avant de comparer les outils, poser les vrais besoins de l'usine YAWatch-LUNA.

### 1.1 Les 9 plans du teaser S01E00 et leurs mouvements

| Plan | Sujet | Mouvement requis | Difficulté I2V | Visage humain |
|---|---|---|---|---|
| 1 | Tour YAWatch La Défense | Pan vertical lent, logo stable | Faible | Non |
| 2 | Luna adulte portrait | Push-in imperceptible | **Élevée** | **Oui — critique** |
| 3 | Luna au bureau | Micro-mouvement / respiration | **Élevée** | **Oui — critique** |
| 4 | Luna + photo retournée | Main qui bouge, tension | Moyenne | Oui + objet |
| 5 | Luna enfant nuit | Ombre qui passe, peur | **Élevée** | **Oui — enfant** |
| 6 | Luna enfant + poupée | Push-in doux, réconfort | **Élevée** | **Oui — enfant** |
| 7 | Gros plan yeux poupée | Macro très lente | Faible | Non (poupée) |
| 8 | Aby observe Luna | Léger mouvement latéral, reflet | **Élevée** | **Oui — critique** |
| 9 | Aby enfant + jeton noir | Focus pull, main + objet | Moyenne | Oui + objet |

**Conclusion : 6/9 plans impliquent un visage humain en gros plan.**
**La stabilité des visages est le critère n°1 de l'usine, pas la qualité générale.**

### 1.2 Contraintes à l'échelle de la série

| Indicateur | Teaser (S01E00) | Épisode 7 min | Saison 1 (20 épisodes) |
|---|---|---|---|
| Clips I2V à générer | 9 | 50-80 | 1 000-1 600 |
| Personnages récurrents | Luna, Aby | Luna, Aby, Malik, Père, Luna Doll | Idem + extensions |
| Budget par clip (cloud) | Tolérable | Significatif | **Coût majeur** |
| Cohérence identité | 9 clips | 50-80 clips | Milliers de clips |

**Conséquence directe :** un outil qui produit un beau clip isolé mais dérive sur le visage
de Luna entre le clip 1 et le clip 47 détruit la cohérence de l'épisode.

### 1.3 Situation hardware actuelle

```
Machine de développement : VirtualBox VM (Linux)
GPU détecté             : VMware SVGA II Adapter (émulation — aucune VRAM réelle)
CUDA disponible         : Non
```

**Les options locales nécessitent une machine physique dédiée ou un cloud GPU (RunPod, Lambda Labs, Vast.ai).**
Cette contrainte est temporaire mais doit figurer dans la décision.

---

## 2. Critères de sélection (pondérés par importance YAWatch-LUNA)

| # | Critère | Poids | Pourquoi ce poids |
|---|---|---|---|
| 1 | Stabilité des visages | ★★★★★ | Luna apparaît dans 1 000+ clips. Toute dérive détruit la cohérence. |
| 2 | Compatibilité 9:16 natif | ★★★★★ | Le format Shorts est la contrainte technique de base. |
| 3 | Contrôle artistique | ★★★★☆ | L'usine doit produire LA vision de Ludovic, pas une esthétique générique. |
| 4 | Coût à l'échelle | ★★★★☆ | 1 000+ clips en saison 1 — le coût par clip devient structurant. |
| 5 | Dépendance fournisseur | ★★★☆☆ | Un changement de tarif ou une fermeture d'API peut bloquer la production. |
| 6 | Risque de dérive visuelle | ★★★☆☆ | Certains outils "embellissent" ou modifient subtilement les personnages. |
| 7 | Capacité teaser 9 plans | ★★★☆☆ | Premier jalon immédiat. |
| 8 | Difficulté d'installation | ★★☆☆☆ | Investissement initial — acceptable si le résultat est bon. |
| 9 | Qualité motion générale | ★★☆☆☆ | Secondaire si les visages sont stables et le mouvement cohérent. |

---

## 3. Options locales

Les options locales fonctionnent sur GPU personnel ou cloud GPU loué (RunPod, Vast.ai, Lambda Labs).

### 3.1 Wan2.1 I2V 14B (Wan-AI)

**Modèle :** open source, HuggingFace `Wan-AI/Wan2.1-I2V-14B-480P`

| Critère | Note | Détail |
|---|---|---|
| Stabilité visages | ★★★★★ | Meilleure fidélité à l'image source parmi les modèles open source |
| Format 9:16 | ★★★★☆ | Natif vertical, résolution native 480P (upscaling nécessaire pour 1080×1920) |
| Contrôle artistique | ★★★★★ | Prompt text-to-motion, seed fixe, IPAdapter pour cohérence personnage possible |
| Coût à l'échelle | ★★★★★ | Gratuit (coût hardware uniquement) |
| Dépendance fournisseur | ★★★★★ | Aucune — modèle téléchargé, auto-hébergé |
| Risque dérive visuelle | ★★★★★ | Très faible — fidèle à l'image source |
| Capacité teaser 9 plans | ★★★★☆ | Oui, avec workflow répété par plan |
| Difficulté installation | ★☆☆☆☆ | **Complexe** — modèle 28 GB, dépendances Diffusers, CUDA requis |
| Qualité motion | ★★★★★ | Meilleure open source |

**VRAM requise :** 16+ GB (GPU dédié type RTX 3090 / 4090 / A100)  
**Durée de génération :** ~2-5 min par clip (GPU local) / ~30-90s (RunPod A100)  
**Upscaling :** Real-ESRGAN ou Topaz Video nécessaire pour atteindre 1080×1920 depuis 480P  
**Risque principal :** l'installation complexe + l'upscaling ajoutent de la friction  

---

### 3.2 CogVideoX-5B I2V (THUDM)

**Modèle :** open source, HuggingFace `THUDM/CogVideoX-5b-I2V`  
**Déjà documenté dans :** `DIFFUSERS_VIDEO_MODELS_REFERENCE.md`

| Critère | Note | Détail |
|---|---|---|
| Stabilité visages | ★★★★☆ | Bonne fidélité — légèrement inférieure à Wan2.1 |
| Format 9:16 | ★★★★☆ | Vertical supporté avec configuration (480×832 natif) |
| Contrôle artistique | ★★★★☆ | Text-guided motion, seed fixe, API Diffusers connue |
| Coût à l'échelle | ★★★★★ | Gratuit |
| Dépendance fournisseur | ★★★★★ | Aucune |
| Risque dérive visuelle | ★★★★☆ | Faible — respectueux de l'image source |
| Capacité teaser 9 plans | ★★★★★ | 49 frames à 8fps = 6,1s par clip — idéal pour plans de 3-6s |
| Difficulté installation | ★★★☆☆ | **Modéré** — Diffusers standard, workflow existant dans le repo |
| Qualité motion | ★★★★☆ | Bonne — narratif et guidé par prompt |

**VRAM requise :** 8-10 GB (RTX 3070/3080, 4070/4080)  
**Durée de génération :** ~3-8 min par clip (GPU local)  
**Avantage :** déjà documenté et intégré conceptuellement dans la base de connaissances du repo  
**Risque principal :** qualité légèrement inférieure à Wan2.1 pour des mouvements complexes  

---

### 3.3 CogVideoX-2B I2V (THUDM)

| Critère | Note | Détail |
|---|---|---|
| Stabilité visages | ★★★☆☆ | Acceptable |
| Format 9:16 | ★★★★☆ | Supporté |
| Contrôle artistique | ★★★☆☆ | Paramètres réduits vs 5B |
| Coût à l'échelle | ★★★★★ | Gratuit |
| Dépendance fournisseur | ★★★★★ | Aucune |
| Risque dérive visuelle | ★★★☆☆ | Moyen — moins précis que 5B |
| Difficulté installation | ★★★☆☆ | Identique à 5B |
| Qualité motion | ★★★☆☆ | Mouvements simples corrects |

**VRAM requise :** 4-6 GB  
**Usage recommandé :** prototypage rapide uniquement — pas production finale  

---

### 3.4 SVD XT (Stable Video Diffusion — Stability AI)

| Critère | Note | Détail |
|---|---|---|
| Format 9:16 | ★☆☆☆☆ | **Entraîné en 16:9 — problème majeur pour l'usine** |
| Stabilité visages | ★★★☆☆ | Convenable |
| Contrôle artistique | ★★☆☆☆ | Pas de text-guided motion — motion_bucket_id uniquement |
| Qualité motion | ★★★☆☆ | Bonne pour plans statiques |

**Verdict YAWatch-LUNA : non recommandé.** Le format 16:9 natif est incompatible avec Shorts.
Le forçage en 9:16 produit des artefacts et une qualité dégradée.

---

### 3.5 AnimateDiff v3 (via ComfyUI)

| Critère | Note | Détail |
|---|---|---|
| Format 9:16 | ★★★☆☆ | Configurable mais non natif |
| Stabilité visages | ★★★☆☆ | Nécessite IPAdapter pour fidélité au personnage |
| Contrôle artistique | ★★★★☆ | Forte — ControlNet, IPAdapter, LoRA personnage |
| Difficulté installation | ★★☆☆☆ | **Élevée** — ComfyUI + extensions + modèles multiples |
| Qualité motion | ★★★☆☆ | Bon pour personnages en mouvement, moins bon pour plans contemplatifs |

**Usage potentiel :** plans dynamiques (plan 4 : main qui bouge, plan 9 : dépôt jeton).
**Pas recommandé comme outil principal** — trop complexe pour un outil primaire.

---

### 3.6 LTX-Video (Lightricks)

**Modèle :** open source, 2024-2025, optimisé pour la vitesse

| Critère | Note | Détail |
|---|---|---|
| Format 9:16 | ★★★★☆ | Supporté |
| Stabilité visages | ★★★☆☆ | Correct, moins que Wan2.1 |
| Vitesse génération | ★★★★★ | 10-30x plus rapide que les autres modèles |
| Qualité motion | ★★★☆☆ | Acceptable, pas premium |
| VRAM requise | 8 GB | Accessible |

**Usage potentiel :** itérations rapides de prototypage.
**Pas recommandé comme outil de production final** pour YAWatch-LUNA — qualité insuffisante pour le niveau cinématique requis.

---

## 4. Options cloud/API

Ces options ne nécessitent pas de GPU local. Elles facturent à l'usage (par clip ou par seconde).

### 4.1 Runway Gen-3 Alpha / Gen-4 (Runway ML)

**API :** `pip install runwayml` — endpoint REST

| Critère | Note | Détail |
|---|---|---|
| Stabilité visages | ★★★★★ | Référence industrie — meilleure fidélité face cloud |
| Format 9:16 | ★★★★★ | Natif — prévu pour Shorts et Reels |
| Contrôle artistique | ★★★★☆ | Prompt text + image reference. Gen-4 : "Consistent character" entre clips |
| Coût à l'échelle | ★★☆☆☆ | ~0.25-0.50€/clip (5s) · Teaser : ~5€ · EP01 : ~30-40€ · Saison 1 : ~400-600€ |
| Dépendance fournisseur | ★★☆☆☆ | **Élevée** — startup, tarifs variables, accès API conditionnel |
| Risque dérive visuelle | ★★★☆☆ | Runway a ses propres tendances esthétiques (hyper-lissé, parfois trop propre) |
| Capacité teaser 9 plans | ★★★★★ | Idéal — API simple, résultats immédiats |
| Difficulté installation | ★★★★★ | Très simple — clé API + 3 lignes Python |
| Qualité motion | ★★★★★ | Meilleure qualité cloud actuelle |

**Génération typique :** < 60 secondes par clip  
**Gen-4 spécifiquement :** fonctionnalité "Character Consistency" — même image de référence pour un personnage, cohérence maintenue entre plusieurs générations. Critique pour Luna sur 80 clips d'un épisode.  
**Risque principal :** dépendance à une startup (leçon Simli vs Tavus dans le projet YAWatch app)

---

### 4.2 Luma Dream Machine (Luma AI)

**API :** `pip install lumaai` — endpoint REST

| Critère | Note | Détail |
|---|---|---|
| Stabilité visages | ★★★★☆ | Bonne — légèrement inférieure à Runway pour les portraits serré |
| Format 9:16 | ★★★★☆ | Supporté |
| Contrôle artistique | ★★★☆☆ | Prompt + image. Moins de contrôle fin que Runway |
| Coût à l'échelle | ★★★☆☆ | Plans d'abonnement ($29-500/mois) + crédits · Difficile à prévoir à l'unité |
| Dépendance fournisseur | ★★☆☆☆ | Élevée |
| Risque dérive visuelle | ★★★☆☆ | Esthétique Luma reconnaissable (lumineux, légèrement éthéré) |
| Capacité teaser 9 plans | ★★★★☆ | Bon |
| Difficulté installation | ★★★★★ | Très simple |
| Qualité motion | ★★★★☆ | Bonne — caméra fluide |

**Usage potentiel :** bonne alternative à Runway, tarification plus lisible avec abonnement.  
**Risque principal :** esthétique propre peut tirer les scènes vers le "trop beau" au détriment du thriller.

---

### 4.3 Hailuo / MiniMax

**API :** MiniMax API (minimax.io)

| Critère | Note | Détail |
|---|---|---|
| Stabilité visages | ★★★★☆ | Reconnue pour la fidélité sur visages notamment asiatiques (pertinent pour Luna) |
| Format 9:16 | ★★★★☆ | Supporté |
| Contrôle artistique | ★★★☆☆ | Prompt + image. Contrôle moyen |
| Coût à l'échelle | ★★★☆☆ | Crédits — tarification moins documentée en Europe |
| Dépendance fournisseur | ★★☆☆☆ | Société chinoise — risque réglementaire possible |
| Risque dérive visuelle | ★★★☆☆ | Esthétique Hailuo reconnaissable, tendance hyper-réaliste |
| Capacité teaser 9 plans | ★★★★☆ | Bon |
| Difficulté installation | ★★★★☆ | Simple |
| Qualité motion | ★★★★☆ | Bonne |

**Usage potentiel :** alternative crédible, notamment pour la stabilité des visages.  
**Risque principal :** dépendance à une entreprise chinoise — incertitude réglementaire pour un contenu européen distribué sur YouTube.

---

### 4.4 Pika 2.2 (Pika Labs)

| Critère | Note | Détail |
|---|---|---|
| Stabilité visages | ★★★☆☆ | Correcte |
| Format 9:16 | ★★★★☆ | Supporté |
| Contrôle artistique | ★★★☆☆ | Bon pour effets spéciaux (Pikaffects), moins pour cinéma naturaliste |
| Coût à l'échelle | ★★★☆☆ | Crédits, tarification par plan |
| Dépendance fournisseur | ★★★☆☆ | Startup |
| Risque dérive visuelle | ★★☆☆☆ | **Pika tend à "styliser" les images — risque de dérive vers un esthétique pop** |
| Capacité teaser 9 plans | ★★★☆☆ | Acceptable |
| API | ★★★☆☆ | Beta — moins stable que Runway ou Luma |

**Verdict YAWatch-LUNA :** non recommandé en priorité. L'esthétique Pika (pop, stylisée, effets)
est incompatible avec le thriller psychologique parisien réaliste de la série.

---

## 5. Matrice comparative globale

Échelle : ★ = 1 (mauvais) → ★★★★★ = 5 (excellent) · **↑** = avantageux · **↓** = contrainte

| Critère (poids) | Wan2.1 14B | CogVideoX-5B | Runway Gen-3/4 | Luma | Hailuo |
|---|---|---|---|---|---|
| **Stabilité visages** (★★★★★) | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★☆ |
| **Format 9:16 natif** (★★★★★) | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★☆ |
| **Contrôle artistique** (★★★★☆) | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ |
| **Coût à l'échelle** (★★★★☆) | ★★★★★ | ★★★★★ | ★★☆☆☆ | ★★★☆☆ | ★★★☆☆ |
| **Dépendance fournisseur** (★★★☆☆) | ★★★★★ | ★★★★★ | ★★☆☆☆ | ★★☆☆☆ | ★★☆☆☆ |
| **Risque dérive visuelle** (★★★☆☆) | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ |
| **Capacité teaser 9 plans** (★★★☆☆) | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★☆ |
| **Difficulté installation** (★★☆☆☆) | ★☆☆☆☆ | ★★★☆☆ | ★★★★★ | ★★★★★ | ★★★★☆ |
| **Qualité motion générale** (★★☆☆☆) | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★☆ | ★★★★☆ |
| **Score pondéré (indicatif)** | **39/45** | **36/45** | **34/45** | **30/45** | **29/45** |

*Le score pondéré tient compte du poids de chaque critère — pas une simple moyenne.*

---

## 6. Analyse des critères les plus discriminants

### 6.1 Stabilité des visages — Le critère décisif

Luna Doll, Luna adulte, Aby, Malik, Père sont des **personnages récurrents sur 20+ épisodes**.
Chaque clip I2V prend l'image de référence du personnage et doit en respecter :
- la morphologie du visage
- la carnation
- les traits distinctifs
- les expressions attendues

**Ce que les outils font mal :**
- Certains "embellissent" les visages (lissage excessif, symmétrisation)
- D'autres "inventent" des détails non présents dans l'image source
- Certains dérivent progressivement entre clips (clip 1 de Luna ≠ clip 47)

**Gagnants sur ce critère :** Wan2.1 14B et Runway Gen-3/4 (avec Character Consistency Gen-4)

**Avantage structurel des outils locaux :** la possibilité d'entraîner un LoRA personnage
(5-20 images de Luna → modèle fine-tuné sur Luna spécifiquement) est une garantie de cohérence
qui n'existe pas dans les APIs cloud.

### 6.2 Format 9:16 — La contrainte de base

La majorité des modèles I2V sont entraînés en 16:9. Le format 9:16 (Shorts YouTube) est secondaire.

**Ce que ça implique concrètement :**
- Un modèle 16:9 forcé en 9:16 produit des distorsions, des corps coupés, des cadrages incohérents
- Les modèles qui "supportent" le 9:16 le font souvent à résolution réduite, nécessitant un upscaling
- Runway Gen-3/4 est conçu pour les réseaux sociaux — le 9:16 est un format nativement supporté

**Gagnants sur ce critère :** Runway Gen-3/4, puis Wan2.1 (avec upscaling), puis CogVideoX-5B

### 6.3 Coût à l'échelle — La question saisonnière

Pour un teaser (9 clips), le coût cloud est négligeable (5-15€). Le coût devient structurant à l'échelle de la série.

**Projection à 1 600 clips (Saison 1 complète) :**

| Outil | Coût/clip (5s) | Coût teaser (9) | Coût EP01 (70) | Coût Saison 1 (1 600) |
|---|---|---|---|---|
| Wan2.1 / CogVideoX local | ~0€ + GPU | 0€ | 0€ | 0€ (hardware) |
| Runway Gen-3 Alpha | ~0.25€ | ~2.25€ | ~17.50€ | **~400€** |
| Runway Gen-4 | ~0.50€ | ~4.50€ | ~35€ | **~800€** |
| Luma Dream Machine | ~0.15-0.30€ | ~2€ | ~17€ | **~350€** |
| Hailuo | ~0.10-0.20€ | ~1.50€ | ~12€ | **~250€** |

*Les coûts cloud sont cumulatifs et augmentent avec les regénérations (clips rejetés par le quality gate).*

**À 1 600 clips produits + 20% de rejet quality gate = ~1 920 générations effectives.**

### 6.4 Dépendance fournisseur — La leçon Simli

Le projet YAWatch app a déjà vécu un changement d'outil I2V forcé (Simli → Tavus).
La même situation peut se reproduire avec un fournisseur cloud I2V :
- Changement de tarification
- Fermeture d'API
- Dégradation de qualité après mise à jour du modèle
- Conditions d'utilisation restreintes (droits sur les contenus générés)

**Les outils locaux (Wan2.1, CogVideoX) sont immunisés contre ce risque** — le modèle est
téléchargé une fois et reste disponible.

**Point de vigilance Runway :** les CGU de Runway autorisent l'utilisation commerciale des clips
générés, mais Runway se réserve des droits de monitoring. À vérifier selon le modèle de distribution YAWatch.

### 6.5 Risque de dérive visuelle/sonore

Ce critère mesure la propension d'un outil à imposer son esthétique sur le contenu.

**Signes de dérive identifiés sur les outils cloud :**
- *Runway* : tendance au rendu "cinema premium" — très lisse, très cinématique, parfois trop propre
  pour l'ambiance thriller cru voulu par YAWatch
- *Luma* : esthétique éthérée, lumineuse — peut tirer les scènes sombres vers le beau plutôt que l'anxiogène
- *Pika* : stylisation pop — incompatible avec le réalisme parisien

**Les outils locaux n'imposent pas d'esthétique** — ils suivent fidèlement le prompt et l'image source.
Le risque de dérive existe mais vient du prompt, pas de l'outil. Il est contrôlable.

---

## 7. Question bloquante non résolue

**La décision dépend d'une information que cette matrice ne peut pas déterminer :**

> **Quelle est la VRAM disponible sur la machine de production vidéo ?**

| VRAM disponible | Recommandation |
|---|---|
| ≥ 16 GB | Wan2.1 I2V 14B — meilleur rapport qualité/contrôle/coût |
| 8-10 GB | CogVideoX-5B I2V — bon équilibre, déjà documenté dans le repo |
| 4-8 GB | CogVideoX-2B + cloud pour les plans complexes (hybride) |
| Pas de GPU dédié | Runway Gen-3 Alpha pour démarrer, migration locale possible plus tard |
| Cloud GPU loué | RunPod/Vast.ai + Wan2.1 — même résultat que GPU local, coût prévisible |

---

## 8. Deux stratégies opposées — Analyse honnête

### Stratégie A — Cloud first (Runway Gen-3 Alpha)

**Pour :** démarrage immédiat, qualité validée, aucun setup technique  
**Contre :** coût récurrent, dépendance fournisseur, esthétique légèrement contrainte, ~400-800€ pour la Saison 1

**Quand c'est cohérent avec l'usine :**
- Si aucun GPU dédié n'est disponible à court terme
- Si la priorité est de valider la grammaire visuelle rapidement sur le teaser
- Si le budget saison 1 absorbe ~500€ d'infrastructure I2V

### Stratégie B — Local first (Wan2.1 ou CogVideoX-5B)

**Pour :** coût nul à l'échelle, contrôle total, cohérence maximale, LoRA personnage possible  
**Contre :** setup complexe, VRAM requise, itérations plus lentes

**Quand c'est cohérent avec l'usine :**
- Si une machine GPU est disponible ou louable (RunPod ~0.50$/h pour A100 = ~30€ pour produire un épisode complet)
- Si l'objectif est l'indépendance totale à long terme
- Si la qualité d'un modèle local suffit après test de validation

### Stratégie C — Hybride (recommandée si VRAM inconnue)

**Phase 1 — Teaser (9 clips) :** Runway Gen-3 Alpha → coût minimal, qualité immédiate, validation de la grammaire visuelle  
**Phase 2 — EP01 :** décision locale vs cloud basée sur les leçons du teaser

**Avantage :** ne ferme aucune porte. Fournit une baseline de qualité avant de choisir l'outil permanent.

---

## 9. Référence historique rejetée — Kling AI

**Statut :** exclu définitivement de la stratégie YAWatch-LUNA (décision 2026-06-20)

**Pourquoi il est mentionné ici :** les futures IA ou futures discussions pourraient proposer
de revenir à Kling. Ce paragraphe verrouille le contexte de la décision.

**Kling avait :** bonne qualité, API disponible, résultats corrects sur les 5 plans testés.  
**La décision d'exclusion n'est pas liée à la qualité de l'outil** mais à la décision
stratégique de construire une architecture I2V_ENGINE agnostique, non couplée à un fournisseur.

Kling est compatible avec le slot I2V_ENGINE — il pourrait techniquement y être réintégré
si Ludovic le décide explicitement. Cette décision ne peut pas venir d'un agent IA.

---

## 10. Recommandation finale argumentée

### Recommandation principale

> **Pour l'usine YAWatch-LUNA à long terme : option locale (Wan2.1 14B ou CogVideoX-5B) sur GPU dédié.**

**Argumentation :**

1. **Cohérence à l'échelle.** 1 600 clips sur la Saison 1 avec des personnages récurrents nécessitent une fidélité garantie. Un LoRA Luna entraîné sur 20 images canoniques donne une cohérence inatteignable avec un outil cloud générique.

2. **Coût.** Zéro à l'échelle (hardware amorti). Runway à 400-800€ pour la Saison 1 est tolérable mais devient un coût structurel permanent pour chaque saison.

3. **Indépendance.** La série YAWatch-LUNA a déjà changé d'outil I2V une fois (Simli → Tavus dans l'app). Construire l'usine sur un outil local élimine ce risque pour la production vidéo.

4. **Contrôle artistique.** Le pipeline local permet des ajustements fins (seed, steps, CFG, IPAdapter) qui restent hors portée des APIs cloud.

### Recommandation pour démarrer maintenant (sans GPU dédié)

> **Runway Gen-3 Alpha pour le teaser S01E00 (9 clips, ~5-10€).**

**Argumentaire :**
- Pas de setup requis — productif immédiatement
- Qualité suffisante pour valider la grammaire visuelle du teaser
- 5-10€ pour 9 clips : investissement de validation, pas d'engagement long terme
- Résultat : premier teaser candidat qui permet de décider de la stratégie locale ensuite

### Ce que cette recommandation ne décide pas

- Elle ne choisit pas l'outil permanent de l'usine — c'est la décision de Ludovic
- Elle ne préjuge pas de la qualité de Runway vs local — seul un test sur les 9 plans du teaser réel peut trancher
- Elle ne ferme pas la porte à Wan2.1 ou CogVideoX-5B si une machine GPU est disponible

---

## 11. Prochaine étape recommandée

Avant de coder l'intégration I2V_ENGINE, effectuer le test de validation sur **3 plans représentatifs** :

| Plan | Représente | Challenge principal |
|---|---|---|
| Plan 2 — Luna adulte portrait | Push-in visage humain | Stabilité visage |
| Plan 6 — Luna enfant + poupée | Visage enfant + texture tissu | Double stabilité |
| Plan 9 — Aby enfant + jeton noir | Main + objet + visage enfant | Mains (difficulté I2V connue) |

**Score minimum requis (grille `IMAGE_TO_VIDEO_TEST_MATRIX.md`) :** 25/35 sur ces 3 plans.
Si l'outil passe 25/35 sur ces 3 plans, il est validé pour le teaser complet.

L'outil qui passera ce test sur ces 3 plans deviendra automatiquement le premier occupant du slot I2V_ENGINE.

---

*I2V Engine Decision Matrix v1.0 — 2026-06-20*  
*Référence : `YAWATCH_LUNA_FACTORY_MASTER_PLAN.md` Partie 7*
