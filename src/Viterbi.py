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

def main():
    train_file = "../data/train/POS.train"

    word_tag_counts = count_word_tag_pairs(train_file)
