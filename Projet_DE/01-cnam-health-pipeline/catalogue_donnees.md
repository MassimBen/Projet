# Catalogue des jeux de données

Ce document décrit les colonnes utilisées par les trois assets du pipeline. Les colonnes/type correspondent aux sources et aux types matérialisés par le code ; lorsque la documentation officielle ne donne pas une définition détaillée, la description est indicative et doit être confirmée à l'aide du dictionnaire fourni avec le fichier source.

## Dépenses de santé — `cnam.depenses_2025`

**Sources :**

- [Catalogue officiel des données open data de l'Assurance Maladie](https://www.assurance-maladie.ameli.fr/etudes-et-donnees/donnees/liste-donnees-open-data) — téléchargement des fichiers CSV.
- [Rubrique « Dépenses d'assurance maladie »](https://www.assurance-maladie.ameli.fr/etudes-et-donnees/par-theme/depenses-assurance-maladie) — contexte général des dépenses publiées.
- En-tête des fichiers CSV mensuels utilisés par le pipeline — noms des variables.

**Limite de provenance :** le dictionnaire CNAM qui définit précisément toutes les variables `NTOT` n'a pas été retrouvé dans les fichiers du projet ni dans les pages citées. Les descriptions du tableau ci-dessous sont donc des interprétations indicatives des noms et libellés, et non des définitions officielles garanties. Pour les unités, codes et règles de calcul, consulter le dictionnaire fourni avec la série téléchargée.

**Périmètre utilisé :** janvier à avril 2025, selon les fichiers locaux sélectionnés. Les lignes sont des agrégats statistiques, et non des enregistrements individuels de patients.

| Colonnes | Signification / lecture |
|---|---|
| `PRS_FAC_TOP`, `l_fac_top` | Code et libellé du regroupement de prestation facturée (`TOP`). |
| `SERIE`, `l_serie` | Code et libellé de série de la prestation. |
| `prs_nat`, `l_prs_nat` | Code et libellé de la nature de la prestation. |
| `rem_date`, `sns_date` | Périodes de remboursement et de soins, généralement au format `AAAAMM`. |
| `asu_nat`, `l_asu_nat` | Code et libellé de la nature d'assurance ou du risque pris en charge. |
| `cpl_cod`, `l_cpl_cod` | Code et libellé du complément associé à la prestation. |
| `REM_TAU` | Taux de remboursement ; unité et modalités à vérifier dans le dictionnaire source. |
| `pre_spe`, `l_pre_spe`, `pre_spe1`, `l_pre_spe1` | Codes et libellés de spécialité du professionnel prescripteur, selon les niveaux fournis par la source. |
| `pre_stj1`, `l_pre_stj1` | Code et libellé du statut juridique du prescripteur. |
| `exe_spe`, `l_exe_spe`, `exe_spe1`, `l_exe_spe1` | Codes et libellés de spécialité du professionnel exécutant, selon les niveaux fournis par la source. |
| `exe_stj1`, `l_exe_stj1` | Code et libellé du statut juridique de l'exécutant. |
| `rem_mon`, `rec_mon`, `dep_mon` | Mesures monétaires liées au remboursement, aux montants reconnus et aux dépenses. Les définitions, unités et règles de calcul exactes sont à confirmer dans la documentation du fichier. |
| `act_dnb` | Nombre ou dénombrement d'actes associé à l'agrégat. |
| `act_coe` | Coefficient d'activité associé à l'agrégat. |

Les colonnes préfixées par `l_` sont des libellés associés à des codes. Ne pas additionner ou comparer les montants et indicateurs d'activité sans vérifier leurs unités et leur niveau d'agrégation.

## Comorbidités — `cnam.comorbidites`

**Sources officielles :**

- [Fiche du jeu de données](https://data.ameli.fr/explore/dataset/comorbidites/information/) — description générale et définitions.
- [Métadonnées de l'API](https://data.ameli.fr/api/explore/v2.1/catalog/datasets/comorbidites) — noms de champs, types et descriptions exposées par le catalogue.
- [Export CSV utilisé par le pipeline](https://data.ameli.fr/api/explore/v2.1/catalog/datasets/comorbidites/exports/csv?use_labels=false&delimiter=%3B) — valeurs effectivement récupérées ; séparateur `;`.

Les descriptions ci-dessous proviennent principalement des descriptions de champs du catalogue et de la fiche du jeu.

| Colonne | Type matérialisé | Signification |
|---|---|---|
| `annee` | Entier | Année de référence. |
| `patho_niv1` | Texte | Groupe de pathologies, traitements chroniques ou épisodes de soins. |
| `patho_niv2` | Texte | Sous-groupe de pathologies ou de prises en charge. |
| `patho_niv3` | Texte | Sous-groupe détaillé de pathologies ou de prises en charge. |
| `top` | Texte | Libellé technique de la pathologie, du traitement chronique ou de l'épisode de soins étudié. |
| `comorbidite` | Texte | Libellé technique de la comorbidité associée. |
| `libelle_comorbidite` | Texte | Libellé descriptif de la comorbidité associée. |
| `region` | Entier | Code de région ; `99` désigne le niveau national selon la fiche source. |
| `dept` | Entier | Code de département ; `999` désigne le niveau national selon la fiche source. |
| `ncomorb` | Entier | Effectif pris en charge pour la comorbidité associée. |
| `ntop` | Entier | Effectif pris en charge pour la pathologie ou prise en charge étudiée. |
| `proportion_comorb` | Nombre décimal | Rapport entre `ncomorb` et `ntop`. |
| `patho_niv1_comorb` | Texte | Groupe de pathologies associé à la comorbidité. |
| `patho_niv2_comorb` | Texte | Sous-groupe associé à la comorbidité. |
| `patho_niv3_comorb` | Texte | Sous-groupe détaillé associé à la comorbidité. |
| `niveau_prioritaire` | Texte | Niveau prioritaire associé, selon la nomenclature de la source. |

## Patientèle des médecins traitants — `cnam.professionelle`

**Sources officielles :**

- [Fiche du jeu de données](https://data.ameli.fr/explore/dataset/patientele-medecintraitant-generalistes-annuelle/information/) — champ, contexte, secret statistique et fréquence de mise à jour.
- [Méthode « Accès aux soins »](https://data.ameli.fr/pages/methode-acces-aux-soins/) — méthode et définitions complémentaires.
- [Métadonnées de l'API](https://data.ameli.fr/api/explore/v2.1/catalog/datasets/patientele-medecintraitant-generalistes-annuelle) — noms de champs, types et annotations (dont l'unité des taux).
- [Export CSV utilisé par le pipeline](https://data.ameli.fr/api/explore/v2.1/catalog/datasets/patientele-medecintraitant-generalistes-annuelle/exports/csv?use_labels=false&delimiter=%3B) — valeurs effectivement récupérées ; séparateur `;`.

La source décrit la patientèle moyenne « médecin traitant » des médecins généralistes actifs répondant aux critères de champ du jeu de données, aux niveaux national, régional et départemental. Les descriptions des colonnes reprennent la fiche et les métadonnées officielles.

| Colonne | Type matérialisé | Signification |
|---|---|---|
| `annee` | Entier | Année de référence. |
| `profession_sante` | Texte | Profession de santé concernée. |
| `region` | Texte | Code ou identifiant de région. |
| `libelle_region` | Texte | Libellé de la région. |
| `departement` | Texte | Code ou identifiant de département. |
| `libelle_departement` | Texte | Libellé du département. |
| `nombre_patients_medecin_traitant` | Entier | Nombre moyen de patients ayant déclaré le médecin comme médecin traitant. |
| `taux_evolution_annuel` | Texte | Taux d'évolution annuel publié ; le texte peut conserver des modalités telles que `NS` ou `NC`. |
| `taux_evolution_annuel_integer` | Nombre décimal | Valeur numérique du taux d'évolution annuel, lorsqu'elle est disponible. |

Pour les conditions de champ, le secret statistique et les mises à jour, se référer à la [documentation officielle du jeu de données](https://data.ameli.fr/explore/dataset/patientele-medecintraitant-generalistes-annuelle/information/).
