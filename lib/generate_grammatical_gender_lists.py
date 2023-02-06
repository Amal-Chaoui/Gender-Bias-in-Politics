def masc_fem_gram_gender_set(conllu_file, rmv_masc=None, rmv_fem=None):
    """ create a list of grammatically masculine and feminine words from a conllu file. 
    Parameters:
    -----------
    conllu_file: string
        conllu file. Example: 'data/fr_gsd-ud-dev.conllu'
    rmv_masc: list
        list of further masculine words to remove from the generated list
    rmv_fem: list
        list of further feminine words to remove from the generated list
    """
    data_file = open(conllu_file, "r", encoding="utf-8")
    masculine = set()
    feminine = set()
    all_data = [tokenlist for tokenlist in data_file]
    for i, tokenlist in enumerate(all_data):
        tt = tokenlist.split('\t')
        if tt[0].isdigit() and tt[3] == "NOUN":
            tmp = tt[5].split('|')
            for feat in tmp:
                if 'Gender' in feat and feat.split('=')[1] == 'Masc':
                    if rmv_masc == None or (rmv_masc != None and tt[2] not in rmv_masc):
                        masculine.add(tt[2])

                elif 'Gender' in feat and feat.split('=')[1] == 'Fem':
                    if rmv_fem == None or (rmv_fem != None and tt[2] not in rmv_fem):
                        feminine.add(tt[2])

    return masculine, feminine


def masc_fem_animate_words(tsv_file):
    """ return a list of semantically feminine and masculine animate words """
    data_file = open(tsv_file, "r", encoding="utf-8")
    masculine = set()
    feminine = set()
    for i, row in enumerate(data_file):
        tt = row.split('\t')
        masculine.add(tt[2][:-1])  # -1: to remove '\n'
        feminine.add(tt[1])
    return masculine, feminine
            








if __name__ == '__main__':
  
    # list of masculine and feminine animate (person) words
    masc_animate, fem_animate = masc_fem_animate_words("../data/zmigrod_animate_words.tsv")

    # other animate words (manually spotted)
    other_masc = {'homme', 'député', 'auteur', 'dirigeant', 'client', 'joueur', 'héros', 'animateur', 'jeune-homme', 'grand-père', 'Maître', 'psychologue', 'hôte', 'coursier', 'psychologue', 'gouverneur', 'orateur', 'rappeur', 'émigré', 'trésorier', 'intervenant', 'journaliste', 'empereur', 'malade', 'responsable', 'auteur-compositeur-interprète', 'vétérant', 'beau-frère', 'seigneur', 'kurde', 'militant', 'professeur', 'fils', 'romancier', 'colonel', 'père', 'entraîneur', 'commandant', 'carrossier', 'chevalier', 'indien', 'vénézuélien', 'développeur', 'spécialiste', 'tirailleur', 'réalisateur', 'secrétaire', 'architecte', 'commentateur', 'ministre', 'lanceur', 'imitateur', 'libre-penseur', 'frère', 'organisateur', 'clergé', 'artisan', 'ingénieur', 'médecin', 'acheteur', 'investisseur', 'représentant', 'recruteur', 'grand-maître', 'pèlerin', 'ambassadeur', 'italien', 'statisticien', 'passager', 'éditeur-en-chef'}
    other_fem = {'femme', 'héroïne', 'dame', 'grand-mère', 'reine', 'joueuse','sœur', 'petite-fille', 'nounou', 'enfant', 'surveillante', 'mère', 'serveuse', 'journaliste', 'ministre', 'vice-présidente'}

    # list of masculine and feminine grammatical gender words (before removing the animate words)
    masc_gram, fem_gram = masc_fem_gram_gender_set("../data/fr_gsd-ud-dev.conllu")
    print(f'(before) nb of masc_gram: {len(masc_gram)}   |  nb of fem_gram: {len(fem_gram)}')

    # list of masculine and feminine grammatical gender words (after removing the animate words)
    masc_gram, fem_gram = masc_fem_gram_gender_set("../data/fr_gsd-ud-dev.conllu", masc_animate|other_masc, fem_animate|other_fem)
    print(f'(after)  nb of masc_gram: {len(masc_gram)}   |  nb of fem_gram: {len(fem_gram)}')

    with open("../data/grammatical_masculine.txt", "w") as output:
        for row in masc_gram:
            output.write(str(row) + '\n')
        output.close()

    with open("../data/grammatical_feminine.txt", "w") as output:
        for row in fem_gram:
            output.write(str(row) + '\n')
        #output.write(str(fem_gram))
        output.close()