---
titre: "I am sitting in a room : une boucle de retard qui révèle les résonances d'une salle"
date: 2026-11-10
cours: e-music-ma, e-music-ba
patch: 26-11-10_I_am_sitting_in_a_room_v01.maxpat
notions: Boucle de rétroaction, Ligne de retard, Réverbération, Filtre passe-haut, Entrée micro, Lecture de fichier son, Routage audio, Alvin Lucier
---

# I am sitting in a room : une boucle de retard qui révèle les résonances d'une salle

On reprend le principe de « I am sitting in a room » d'Alvin Lucier : un son est rejoué dans une salle, réenregistré, rejoué encore, jusqu'à ce que la salle elle-même se fasse entendre. Le patch propose deux versions : une salle simulée (réverbération + filtre), à partir d'un fichier son, et la vraie salle, avec un micro et des haut-parleurs.


## Le patch, étape par étape

### 1. Choisir la source
Le menu `umenu` propose trois choix : `off`, `soundfile + room simulation`, `microphone`. Il envoie leur numéro (0, 1 ou 2) à la fois à `selector~ 2` (quelle entrée on laisse passer) et à `gate~ 2` (vers quelle sortie on envoie le son). 0 ferme tout.

### 2. Le fichier son
Premier temps (1) : le message `open` choisit un fichier dans `sfplay~`. Deuxième temps (2) : le toggle lance la lecture (1) ou l'arrête (0). Le son part vers l'entrée 1 du `selector~ 2` et, en direct, vers le `ezdac~` pour entendre l'original.

### 3. Le micro
`ezadc~` est l'entrée audio (le micro). Ses deux canaux arrivent dans `live.gain~` « live input », puis dans l'entrée 2 du `selector~ 2`. Le `loadmess` -6 règle ce niveau à −6 dB à l'ouverture du patch.

### 4. Le retard de 10 secondes
`tapin~ 10000` mémorise jusqu'à 10 secondes de son, `tapout~ 10000` le relit 10 secondes plus tard. C'est l'équivalent des deux magnétophones de Lucier : ce qu'on entend maintenant revient 10 secondes après. Dans la pièce de Lucier, le retard est d'environ 1 min 25 s, soit la durée de lecture de son texte.

### 5. La salle simulée
Sortie 1 du `gate~ 2` : le son retardé passe dans `abl.device.reverb~` (la « salle »), réglée par les `attrui` damping, predelay, decay et mix. Puis `live.gain~` « feedback loop » et `biquad~`, un filtre passe-haut dessiné dans `filtergraph~`. La sortie va au `ezdac~` et revient dans l'entrée 1 du `selector~ 2` : c'est la boucle de rétroaction (feedback loop). À chaque tour, la réverbération s'ajoute à la précédente.

### 6. La vraie salle
Sortie 2 du `gate~ 2` : le son retardé passe par `live.gain~` « live output » puis par le `ezdac~`, donc par les haut-parleurs. La salle résonne, le micro réenregistre, et le son revient 10 secondes plus tard. Ici la boucle passe par l'air : c'est la version de Lucier.


## Avant de commencer

> **Utiliser un fichier personnel de voix parlée.** Comme chez Lucier, une phrase lue fonctionne très bien : on reconnaît longtemps le rythme de la parole, puis seules les résonances restent. Le plus simple : s'enregistrer soi-même en train de lire une phrase. `sfplay~` sans argument lit un fichier mono : prévoir un fichier mono, ou n'utiliser que le canal gauche.

> **Attention : la boucle peut exploser.** À chaque tour, le son s'ajoute à lui-même. Si le gain total de la boucle dépasse 1 (0 dB), le niveau monte à chaque passage jusqu'à saturer. Ce gain dépend du patch, mais surtout de l'amplification extérieure : volume de la carte son, des haut-parleurs, gain du micro. Commencer avec ce volume bas, garder les `live.gain~` sous 0 dB, et passer le menu sur `off` pour tout couper.

> **Attention : en mode micro, protéger ses oreilles.** Pas de casque : la boucle doit passer par l'air, donc par des haut-parleurs. Le micro et les haut-parleurs intégrés de l'ordinateur suffisent pour comprendre l'interaction acoustique. Choisir le micro dans **Options › Audio Status** (Input Device), et commencer avec « live input » et « live output » bas. Un larsen (feedback acoustique) peut apparaître si le micro est trop près des haut-parleurs.

> **Max 9.** `abl.device.reverb~` fait partie des objets ABL (des effets issus d'Ableton Live) apparus avec Max 9 : le patch ne s'ouvre pas correctement dans Max 8.


## Les objets à connaître

### `umenu`
- **Rôle :** Menu déroulant. Il envoie le numéro de l'élément choisi (à gauche) et son texte (au milieu).
- **Dans ce patch :** `off` = 0, `soundfile + room simulation` = 1, `microphone` = 2. Le même numéro règle `selector~ 2` et `gate~ 2`.
- **Le piège :** La numérotation commence à 0 : le premier élément du menu vaut 0, pas 1.
- **Voisins :** `live.menu`, `radiogroup`, `tab`

### `selector~ 2`
- **Rôle :** Aiguillage d'entrées : laisse passer une seule des entrées audio. L'argument est le nombre d'entrées audio.
- **Entrées / sorties :** Gauche : le numéro de l'entrée à ouvrir (0 = aucune). Puis les entrées audio 1 et 2. Une sortie audio.
- **Le piège :** L'entrée audio 1 est la deuxième entrée en partant de la gauche. Et plusieurs câbles dans la même entrée s'additionnent : ici, `sfplay~` et le retour de la boucle arrivent ensemble dans l'entrée 1.
- **Voisins :** `gate~`, `matrix~`, `mc.selector~`

### `gate~ 2`
- **Rôle :** L'inverse de `selector~` : une entrée audio, envoyée vers une seule des sorties. L'argument est le nombre de sorties.
- **Entrées / sorties :** Gauche : le numéro de la sortie (0 = fermé). Droite : le signal.
- **Le piège :** Le signal entre par la droite et le numéro par la gauche : l'inverse d'un réflexe courant.
- **Voisins :** `selector~`, `matrix~`

### `sfplay~`
- **Rôle :** Lecteur de fichier son depuis le disque.
- **Entrées / sorties :** Gauche : `open` (choisir un fichier), 1 (lire depuis le début), 0 (arrêter). Sorties : le signal, puis un bang à la fin du fichier.
- **Le piège :** Sans argument, il est mono. Pour un fichier stéréo : `sfplay~ 2`. Et l'audio doit être allumé pour entendre quelque chose.
- **Voisins :** `playlist~`, `buffer~` + `groove~`, `sfrecord~`

### `ezadc~`
- **Rôle :** Entrée audio (analog-to-digital converter) : le micro ou l'entrée de la carte son. Un clic allume ou éteint l'audio.
- **Entrées / sorties :** Deux sorties, canal 1 et canal 2.
- **Le piège :** L'entrée utilisée se choisit dans **Options › Audio Status** (Input Device). Ici, les deux canaux arrivent dans la même entrée de `live.gain~` : ils s'additionnent.
- **Voisins :** `adc~`, `mc.adc~`, `ezdac~` (la sortie)

### `live.gain~`
- **Rôle :** Réglage de niveau en dB avec vumètre, stéréo.
- **Dans ce patch :** Trois réglages : « live input » (le micro), « live output » (vers la salle réelle) et « feedback loop », qui suit la réverbération dans la boucle simulée.
- **Le piège :** 0 dB veut dire « sans atténuation », pas « silence ». Dans une boucle, rester sous 0 dB.
- **Voisins :** `gain~`, `*~` avec `dbtoa`, `meter~`

### `loadmess -6`
- **Rôle :** Envoie un message (ici un niveau en dB) à l'ouverture du patch.
- **Dans ce patch :** trois `loadmess -6` règlent « live input », « live output » et « feedback loop » à −6 dB. Ouvrir un patch de feedback avec des niveaux bas, c'est une sécurité.
- **Le piège :** Il n'agit qu'à l'ouverture : un réglage changé pendant le cours reste tel quel jusqu'à la prochaine ouverture.
- **Voisins :** `loadbang`, `closebang`

### `tapin~ 10000` · `tapout~ 10000`
- **Rôle :** Ligne de retard. `tapin~` mémorise le son (l'argument est la mémoire maximale en ms), `tapout~` le relit avec un retard (l'argument est le retard en ms).
- **Entrées / sorties :** `tapin~` se branche directement sur `tapout~` (un câble spécial, pas un signal). Un nombre envoyé à `tapout~` change le retard.
- **Le piège :** Le retard ne peut pas dépasser la mémoire de `tapin~`. Et MSP ne permet pas de reboucler un câble audio directement sur lui-même : une boucle doit passer par `tapin~` / `tapout~` (ou `send~` / `receive~`).
- **Voisins :** `delay~` (en échantillons), `comb~`, `send~` / `receive~`

### `abl.device.reverb~` · `attrui`
- **Rôle :** `abl.device.reverb~` est la réverbération d'Ableton Live, disponible comme objet dans Max 9 : c'est la « salle » simulée. `attrui` affiche et modifie un attribut d'un objet.
- **Dans ce patch :** Quatre `attrui` : damping (amortissement des aigus), predelay (temps avant la réverbération), decay (longueur de la réverbération), mix (0.5 = moitié son direct, moitié son réverbéré).
- **Le piège :** Dans une boucle, la réverbération s'ajoute à chaque tour : un decay ou un mix élevé noie très vite le son. Objet de Max 9 uniquement.
- **Voisins :** les autres objets `abl.device.*` de Max 9, `attrui` pour n'importe quel attribut

### `filtergraph~` · `biquad~`
- **Rôle :** `filtergraph~` dessine un filtre à la souris et calcule ses cinq coefficients ; `biquad~` applique ce filtre au signal.
- **Dans ce patch :** Un passe-haut vers 98 Hz : il retire les graves sourds qui s'accumuleraient à chaque tour.
- **Le piège :** `filtergraph~` envoie une liste de coefficients, pas un signal : son câble va dans l'entrée de gauche de `biquad~`, avec le signal. Des coefficients tapés à la main peuvent rendre le filtre instable.
- **Voisins :** `lores~`, `svf~`, `reson~`, `cascade~`

### `ezdac~`
- **Rôle :** Sortie audio vers la carte son (digital-to-analog converter), et bouton pour allumer ou éteindre l'audio.
- **Dans ce patch :** Deux `ezdac~` : l'un pour le fichier et la salle simulée, l'autre pour la salle réelle. Ils sortent tous les deux sur les canaux 1 et 2.
- **Le piège :** Allumer l'un allume l'audio de tout Max : les deux boutons font la même chose.
- **Voisins :** `dac~`, `mc.dac~`, `ezadc~` (l'entrée)


## À essayer

1. Mode `soundfile + room simulation`, avec une phrase parlée : compter les retours toutes les 10 secondes. À partir de combien de tours la voix devient-elle incompréhensible ?
2. Monter decay, puis mix : la boucle s'emballe-t-elle plus vite ? Que reste-t-il du rythme de la parole ?
3. Déplacer le passe-haut dans `filtergraph~` vers 500 Hz, puis vers 30 Hz. Qu'est-ce qui s'accumule dans les graves quand le filtre est trop bas ?
4. Volume de l'ordinateur bas : monter le `live.gain~` « feedback loop » au-dessus de 0 dB. Que se passe-t-il au bout de quelques tours ? Revenir sur `off` pour tout couper.
5. Mode `microphone`, avec le micro et les haut-parleurs de l'ordinateur : lire une phrase, se taire, écouter les tours suivants. Recommencer avec l'ordinateur au milieu de la table, puis contre un mur, puis dans un coin : les résonances changent-elles ?


## Ce que fait la pièce d'Alvin Lucier

Dans « I am sitting in a room » (1969), Alvin Lucier enregistre sa voix lisant un court texte, le rejoue dans la pièce et le réenregistre, encore et encore. Sa partition demande un micro, deux magnétophones, un amplificateur et un haut-parleur.

Chaque salle résonne sur certaines fréquences, selon sa taille et sa forme : à chaque passage, ces fréquences sont renforcées et les autres atténuées. Au bout de nombreuses générations, les mots deviennent incompréhensibles : il ne reste que les résonances de la salle, avec le rythme de la parole.

Le patch remplace les deux magnétophones par une ligne de retard de 10 secondes, et les générations se superposent au lieu de se succéder. En mode simulé, la réverbération et le filtre jouent le rôle de la salle ; en mode micro, c'est la salle réelle.


## Aller plus loin

> **À rendre.** Au moins deux exercices au choix parmi les suivants (ou plus 🙂). Déposer les patchs sur Discord, dans le canal rendus.

> **Lire les mini-patchs.** Les exemples ci-dessous sont écrits en notation pseudo-Max : à reconstruire soi-même dans Max.
> - `[metro 500]` entre crochets = un **objet** (touche **N** dans un patch déverrouillé)
> - `[open(` crochet + parenthèse = une **boîte message** (touche **M**)
> - `|` = un **câble**, de la sortie de l'objet du dessus vers l'entrée de l'objet du dessous
> - `→ tapout~ 10000` = envoyer vers cet objet, déjà présent dans le patch

### Compter les générations · facile
Afficher le numéro du tour en cours : un `metro` au rythme du retard fait avancer un compteur.
```
[toggle]
   |
[metro 10000]
   |
[counter]
   |
[number]
```
Lancer le toggle en même temps que la lecture du fichier.

### Changer la durée du retard · facile
Envoyer une nouvelle durée à `tapout~` : une phrase courte avec un retard court, une phrase longue avec un retard long.
```
[2000(   [5000(   [10000(
   |        |         |
   →  tapout~ 10000
```
Ne pas dépasser 10000 : c'est la mémoire de `tapin~ 10000`.

### Enregistrer la pièce · intermédiaire
Garder une trace des générations dans un fichier : brancher la sortie de `biquad~` dans les deux entrées audio de `sfrecord~ 2`.
```
[open(   [1(   [0(
   |      |     |
[sfrecord~ 2]
```
`open` choisit le nom du fichier, 1 lance l'enregistrement, 0 l'arrête.

### Une salle très résonante · intermédiaire
Remplacer la réverbération par trois filtres résonants en parallèle : une « salle » inventée, qui ne résonne que sur trois fréquences. Brancher la sortie 1 du `gate~ 2` dans les trois, et leurs sorties ensemble dans `live.gain~`.
```
[reson~ 1. 220 20]   [reson~ 1. 330 20]   [reson~ 1. 550 20]
```
Arguments : gain, fréquence centrale, Q (plus Q est grand, plus la résonance est étroite).

### Plusieurs retards · avancé
Un seul `tapout~` peut relire la mémoire à plusieurs moments : un argument par retard, une sortie par retard.
```
[tapin~ 10000]
   |
[tapout~ 3000 7000 10000]
```
Mélanger les trois sorties avant le `gate~ 2`. Les générations se croisent-elles en rythme ?

### Spatialiser les générations · avancé
Reprendre la séance Simple spat : envoyer la sortie de `biquad~` dans `spat5.spat~` plutôt que dans `ezdac~`, et déplacer la source à chaque tour.
```
[metro 10000]
   |
[random 360]
   |
[- 180]
   |
[/source/1/az $1(  →  spat5.oper
```


## Ressources

Dans Max : clic droit (ou Alt-clic, patch déverrouillé) sur un objet › **Open Help**. Les fichiers d'aide de `tapin~`, `filtergraph~` et `abl.device.reverb~` sont particulièrement utiles ici.

- [I Am Sitting in a Room (Wikipédia, en anglais)](https://en.wikipedia.org/wiki/I_Am_Sitting_in_a_Room)
- [Alvin Lucier (Wikipédia, en anglais)](https://en.wikipedia.org/wiki/Alvin_Lucier)
- [Documentation Max (Cycling '74)](https://docs.cycling74.com)
