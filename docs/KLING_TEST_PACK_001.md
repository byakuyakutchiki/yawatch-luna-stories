# KLING TEST PACK 001 - YAWatch-LUNA

Statut : **pack de test officiel**.

Objectif : valider la faisabilite visuelle avec Kling avant de produire 30 a 50 clips pour EP01.

Decision : ne generer aucune nouvelle image. Ce test utilise uniquement les assets canon deja valides.

## Objectifs De Validation

1. Cohérence visuelle : visages, tenues, decors et objets doivent rester stables.
2. Cohérence émotionnelle : les mouvements doivent renforcer la tension sans surjouer.
3. Cohérence narrative : chaque plan doit raconter le mystere Luna / Aby / YAWatch sans l'expliquer.

## Reglages Generaux Kling

- Generer des clips courts de 5 secondes.
- Preferer les mouvements tres lents : push-in, travelling doux, legere respiration.
- Eviter les gestes complexes, les changements de tenue, les rotations brusques et les mouvements de bouche.
- Ne pas demander de dialogue lipsync dans ce test.
- Ne pas modifier les logos, textes, visages, mains, cadre photo ou interface.
- Si Kling propose plusieurs modes, privilegier le mode le plus stable / cinematic / image-to-video, pas le mode le plus creatif.

## Plan 1 - Luna Seule Dans Son Bureau

Image source :

`assets/luna_stories_assets/08_visuels_cles/ep01_luna_seule_bureau_nuit_cadre_en_main_01.png`

Durée recommandée : 5 secondes.

Mouvement recommandé : slow push-in très léger vers Luna et le cadre.

Prompt Kling :

```text
Cinematic 5-second image-to-video shot. Luna sits alone in her YAWatch office at night, holding a turned photo frame. Very slow push-in, subtle breathing, tiny movement in her eyes and shoulders, soft screen glow and warm desk lamp, La Defense skyline outside the window. Emotional psychological thriller mood, quiet tension, realistic film look. Keep her face, hair, black blazer, hands, frame and office exactly consistent. No speaking, no smile, no tears, no dramatic gesture.
```

Risques de dérive visuelle :

- Luna change de visage ou vieillit.
- Les doigts fusionnent autour du cadre.
- Le contenu du cadre devient visible.
- La lumiere devient trop cyberpunk ou trop violette.

Conseils de génération :

- Si les mains se déforment, refaire avec un prompt plus court : "hands stay still".
- Si le cadre révèle une photo, ajouter : "the frame stays turned away, no image visible".
- Garder le mouvement minimal.

## Plan 2 - La Photo Retournée

Image source :

`assets/luna_stories_assets/08_visuels_cles/ep01_insert_cadre_presque_retourne_contenu_cache_01.jpg`

Durée recommandée : 5 secondes.

Mouvement recommandé : léger travelling ou macro push-in.

Prompt Kling :

```text
Cinematic 5-second macro close-up. Slow delicate push-in toward Luna's hands holding a turned photo frame. The frame remains almost turned but its content stays hidden. Soft office light, shallow depth of field, quiet emotional mystery, premium thriller mood. Keep the hands natural and still, keep the frame stable, no faces appearing inside the photo, no text, no reveal.
```

Risques de dérive visuelle :

- Kling révèle une photo ou invente des visages.
- Les mains bougent trop ou se déforment.
- Le cadre fond ou change de forme.

Conseils de génération :

- C'est le plan le plus fragile : ne demander aucun mouvement de main.
- Utiliser seulement un mouvement caméra, pas une action.
- Si Kling invente une photo, refaire avec "back of frame only".

## Plan 3 - Malik Adulte

Image source :

`assets/luna_stories_assets/06_personnage_masculin_noir/malik_adulte_neutral_canon_realiste_01.png`

Durée recommandée : 5 secondes.

Mouvement recommandé : respiration naturelle, micro-mouvement du regard, push-in imperceptible.

Prompt Kling :

```text
Cinematic 5-second portrait shot. Malik sits in his Paris apartment in daylight, quiet and tired, holding his emotions inside. Subtle natural breathing, very small eye movement, slight shift of light from the window, almost imperceptible camera push-in. Human emotional silence, realistic premium drama. Keep Malik's face, hair, beard, grey sweater and apartment exactly consistent. No speaking, no smile, no dramatic motion.
```

Risques de dérive visuelle :

- Malik devient trop expressif ou sourit.
- Le visage change et devient un autre homme.
- L'appartement devient trop luxueux ou generique.

Conseils de génération :

- Tester ce plan tôt : il mesure bien la stabilité visage.
- Si Kling anime trop le visage, demander "still portrait, only breathing".

## Plan 4 - Aby En Salle De Réunion

Image source :

`assets/luna_stories_assets/03_aby/aby_adulte_reunion_publique_collaborateurs_01.png`

Durée recommandée : 5 secondes.

Mouvement recommandé : léger regard hors champ, micro-respiration, aucun geste dominateur.

Prompt Kling :

```text
Cinematic 5-second corporate thriller shot. Aby sits in a glass meeting room at YAWatch Industries, La Defense in daylight, surrounded by adult collaborators. She stays calm, professional and controlled. Very subtle eye movement toward someone off-screen, tiny breathing, slow lateral camera drift. She must look competent and normal, not villainous. Keep her blonde hair bun, black suit, collaborators, table, glasses and La Defense background stable. No smile, no aggressive gesture, no speaking.
```

Risques de dérive visuelle :

- Aby devient trop méchante ou trop glamour.
- Les collaborateurs changent de visage ou bougent trop.
- L'arrière-plan La Défense se transforme en ville générique.

Conseils de génération :

- Ne pas demander de mouvement de mains.
- Le meilleur test ici est la stabilité du groupe et du décor.
- Si Aby sourit trop, ajouter "neutral controlled expression".

## Plan 5 - Tour YAWatch Industries

Image source :

`assets/luna_stories_assets/09_decors_paris_la_defense/pack_01_yawatch_industries/yawatch_tour_la_defense_exterieur_jour_logo_01.png`

Durée recommandée : 5 secondes.

Mouvement recommandé : drone lent vertical ou travelling aérien doux.

Prompt Kling :

```text
Cinematic 5-second establishing shot. Slow elegant aerial drift toward the YAWatch Industries tower at La Defense, Paris, in daylight. Silent corporate power, glass reflections, modern Paris business district, premium thriller atmosphere. Keep the building architecture and YAWatch logo stable and readable, no distortion, no cyberpunk, no New York skyline, no sudden camera movement.
```

Risques de dérive visuelle :

- Le logo se déforme.
- La Défense devient New York ou une ville générique.
- Le mouvement drone devient trop spectaculaire.

Conseils de génération :

- Si le logo bouge ou se déforme, refaire sans logo ou utiliser la version sans logo.
- Un travelling vertical lent est plus sûr qu'un vrai drone complexe.

## Ordre De Test Recommandé

1. Malik adulte : test stabilité visage.
2. Luna bureau : test visage + mains + cadre.
3. Photo retournée : test mains / objet.
4. Aby réunion : test groupe / décor / identité.
5. Tour YAWatch : test architecture / logo.

Si Kling échoue sur 3 plans ou plus, ne pas lancer EP01 complet. Tester un autre outil ou réduire les mouvements.

## Narration Teaser - Version Test 30 à 45 Secondes

```text
Luna disait qu'elle avait construit YAWatch pour protéger les autres.

Mais certaines nuits, le système lui répondait avec des phrases que personne n'avait prononcées.

Dans son bureau, il y avait une photo qu'elle ne retournait jamais.

Un visage qu'elle refusait de revoir.

Et une question qu'elle évitait depuis l'enfance.

Si Luna protège tout le monde...

qui la protège d'elle-même ?
```

Direction :

- Thriller psychologique.
- Mystère humain.
- Peu explicatif.
- Laisser respirer les silences entre les phrases.
- La dernière phrase doit tomber presque à voix basse.

## Direction Voix

### Voix Narratrice

Ton : grave, calme, intime, légèrement fatigué, pas bande-annonce hollywoodienne.

Intention : raconter un secret de famille, pas vendre une application.

Rythme : lent, avec silences. Une phrase peut durer plus longtemps que prévu si l'image respire.

### Voix Luna

Ton : bas, contenu, intelligent, protecteur, émotion retenue.

Intention : Luna ne dramatise pas. Elle se contrôle même quand elle vacille.

Couleur : chaleur discrète, fatigue nocturne, culpabilité non dite.

### Voix Aby

Ton : posé, précis, presque doux, jamais ouvertement méchant.

Intention : elle dit peu, mais chaque mot semble choisi.

Couleur : maîtrise, secret, calme stratégique.

### Voix Malik

Ton : naturel, bas, humain, fatigué, pas spectaculaire.

Intention : un homme qui a appris à dire "ça va" même quand ce n'est pas vrai.

Couleur : retenue, dignité, silence intérieur.

## Ce Que Ce Pack Doit Décider

Après génération des 5 clips, noter chaque plan de 1 à 5 :

| Critère | Note |
|---|---:|
| Respect de l'image source | /5 |
| Stabilité visage | /5 |
| Stabilité mains / objets | /5 |
| Tenues cohérentes | /5 |
| Décor cohérent | /5 |
| Mouvement cinéma | /5 |
| Absence d'artefacts | /5 |

Validation :

- 30/35 ou plus : Kling est validé pour teaser + début EP01.
- 25 à 29/35 : Kling utilisable avec mouvements très simples.
- Moins de 25/35 : ne pas produire EP01 complet avec Kling sans autre test.
