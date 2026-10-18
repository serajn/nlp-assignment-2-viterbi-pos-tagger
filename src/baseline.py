import sys

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
    
    # For debugging purposes (ignore)
    '''
    with open('word_tag_counts.txt', 'w') as f:
        f.write(f" {word_tag_counts}\n")
    '''
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

    # For debugging purposes (ignore)
    '''
    with open('tag_counts.txt', 'w') as f:
        f.write(f" {tag_counts}\n")
    '''

    return tag_counts

def build_baseline(word_tag_counts):
    most_frequent_tags = {}

    for (word, tag), count in word_tag_counts.items():
        if (
            word not in most_frequent_tags
            or count > most_frequent_tags[word][1]
        ):
            most_frequent_tags[word] = (tag, count)

    return {
        word: tag
        for word, (tag, count) in most_frequent_tags.items()
    }

def evaluate_baseline(test_file, most_frequent_tags, tag_counts):
    fallback_tag = max(tag_counts, key=tag_counts.get)

    total_tags = 0
    correct_tags = 0

    with open(test_file, "r") as file:
        for line in file:
            for token in line.strip().split():
                word, gold_tag = token.rsplit("/", 1)

                predicted_tag = most_frequent_tags.get(
                    word, fallback_tag
                )

                total_tags += 1
                if predicted_tag == gold_tag:
                    correct_tags += 1

    accuracy = correct_tags / total_tags if total_tags else 0
    print(f"Baseline accuracy: {accuracy:.2%}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python baseline.py <train_file> <test_file>")
        sys.exit(1)

    train_file = sys.argv[1]
    test_file = sys.argv[2]

    word_tag_counts = count_word_tag_pairs(train_file)
    tag_counts = count_tag_counts(train_file)

    most_frequent_tags = build_baseline(word_tag_counts)

    evaluate_baseline(
        test_file,
        most_frequent_tags,
        tag_counts
    )

if __name__ == "__main__":
    sys.exit(main())