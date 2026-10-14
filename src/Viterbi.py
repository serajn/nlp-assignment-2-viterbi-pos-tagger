def count_word_tag_pairs(file):
    word_tag_counts = {}

    with open(file, 'r') as file:
        for line in file:
            for token in line.split():
                if token.strip():
                    word, tag = token.strip().rsplit('/', 1)

                    if (word, tag) in word_tag_counts:
                        word_tag_counts[(word, tag)] += 1
                    else:
                        word_tag_counts[(word, tag)] = 1

    with open('word_tag_counts.txt', 'w') as f:
        f.write(f" {word_tag_counts}\n")
    
    return word_tag_counts

def count_tag_counts(file):
    tag_counts = {}

    with open(file, 'r') as file:
        for line in file:
            for token in line.split():
                if token.strip():
                    _, tag = token.strip().rsplit('/', 1)

                    if tag in tag_counts:
                        tag_counts[tag] += 1
                    else:
                        tag_counts[tag] = 1

    with open('tag_counts.txt', 'w') as f:
        f.write(f" {tag_counts}\n")

    return tag_counts

'''
def count_transition_counts(file):
    transition_counts = {}
    with open(file, 'r') as f:
        previous_tag = "<START>"
        for line in f:
            if line.strip():
                _, tag = line.strip().split() 
                if (previous_tag, tag) in transition_counts:
                    transition_counts[(previous_tag, tag)] += 1
                else:
                    transition_counts[(previous_tag, tag)] = 1
                previous_tag = tag
            else:
                previous_tag = "<START>"  # Reset at the end of a sentence
    with open('transition_counts.txt', 'w') as f:
        for (prev_tag, curr_tag), count in transition_counts.items():
            f.write(f"{prev_tag} {curr_tag} {count}\n")
    return transition_counts

    '''
def main():
    train_file = "../data/train/POS.train"

    word_tag_counts = count_word_tag_pairs(train_file)
    tag_counts = count_tag_counts(train_file)
    #transition_counts = count_transition_counts(train_file)

    return 0

if __name__ == "__main__":
    main()
