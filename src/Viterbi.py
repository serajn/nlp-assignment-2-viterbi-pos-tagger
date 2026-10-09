def count_word_tag_pairs(file):
    word_tag_counts = {}
    with open(file, 'r') as f:
        for line in f:
            if line.strip():
                word, tag = line.strip().split()
                if (word, tag) in word_tag_counts:
                    word_tag_counts[(word, tag)] += 1
                else:
                    word_tag_counts[(word, tag)] = 1
    return word_tag_counts

def count_tag_counts(file):
    tag_counts = {}
    with open(file, 'r') as f:
        for line in f:
            if line.strip():
                _, tag = line.strip().split()
                if tag in tag_counts:
                    tag_counts[tag] += 1
                else:
                    tag_counts[tag] = 1
    return tag_counts

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
    return transition_counts

def main():
    train_file = "../data/train/POS.train"

    word_tag_counts = count_word_tag_pairs(train_file)
    tag_counts = count_tag_counts(train_file)
    transition_counts = count_transition_counts(train_file)
