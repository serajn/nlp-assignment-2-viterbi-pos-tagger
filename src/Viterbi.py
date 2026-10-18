import math

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

def count_transition_counts(file):
    transition_counts = {}

    with open(file, 'r') as file:
        previous_tag = "<START>"

        for line in file:
            for token in line.split():
                if token.strip():
                    _, tag = token.strip().rsplit('/', 1)

                    if (previous_tag, tag) in transition_counts:
                        transition_counts[(previous_tag, tag)] += 1
                    else:
                        transition_counts[(previous_tag, tag)] = 1
                    previous_tag = tag
                
            previous_tag = "<START>"  # Reset at the end of a sentence

    with open('transition_counts.txt', 'w') as f:
        f.write(f" {transition_counts}\n")

    return transition_counts

def count_sentences(file):
    sentence_count = 0

    with open(file, 'r') as file:
        for line in file:
            if line.strip():
                sentence_count += 1

    return sentence_count


def viterbi(sentence, sentence_count, word_tag_counts, tag_counts, transition_counts, alpha=1.0):
    words = []
    ground_truth_tags = []

    for token in sentence.split():
        word, gold_tag = token.rsplit('/', 1)
        words.append(word)
        ground_truth_tags.append(gold_tag)

    if not words:
        return [], []

    tags = list(tag_counts)
    num_tags = len(tags)

    # Laplace smoothing

    # Training vocabulary size. Reserve one additional slot for unknown words.
    vocabulary = {word for word, tag in word_tag_counts}
    vocab_size = len(vocabulary) + 1

    # Count observed outgoing transitions from each tag.
    outgoing_counts = {tag: 0 for tag in tags}

    for (prev_tag, curr_tag), count in transition_counts.items():
        if prev_tag in outgoing_counts and curr_tag in tag_counts:
            outgoing_counts[prev_tag] += count

    # Initialization Step
    scores = {}
    backpointers = {0: {}}

    for tag in tags:
        emission_probability = (
            word_tag_counts.get((words[0], tag), 0) + alpha
        ) / (
            tag_counts[tag] + alpha * vocab_size
        )

        start_probability = (
            transition_counts.get(("<START>", tag), 0) + alpha
        ) / (
            sentence_count + alpha * num_tags
        )

        scores[tag] = math.log(emission_probability) + math.log(start_probability)
        backpointers[0][tag] = None

    # Iteration Step
    for i in range(1, len(words)):
        new_scores = {}
        new_backpointers = {}

        for tag in tags:
            emission_probability = (
                word_tag_counts.get((words[i], tag), 0) + alpha
            ) / (
                tag_counts[tag] + alpha * vocab_size
            )

            best_score = float('-inf')
            best_prev_tag = None

            for prev_tag in tags:
                transition_probability = (
                    transition_counts.get((prev_tag, tag), 0) + alpha
                ) / (
                    outgoing_counts[prev_tag] + alpha * num_tags
                )

                candidate_score = (
                    scores[prev_tag]
                    + math.log(transition_probability)
                    + math.log(emission_probability)
                )

                if candidate_score > best_score:
                    best_score = candidate_score
                    best_prev_tag = prev_tag

            new_scores[tag] = best_score
            new_backpointers[tag] = best_prev_tag

        scores = new_scores
        backpointers[i] = new_backpointers

    # Sequence Identification Step
    best_tag = max(scores, key=scores.get)

    predicted_tags = [None] * len(words)
    predicted_tags[-1] = best_tag

    for i in range(len(words) - 1, 0, -1):
        predicted_tags[i - 1] = backpointers[i][predicted_tags[i]]

    return predicted_tags, ground_truth_tags


def predict_tags(word_tag_counts, tag_counts, transition_counts, sentence_count, file):
    predicted_tags_list = []

    with open(file, 'r') as file:
        for line in file:
            sentence = line.strip()
            predicted_tags, ground_truth_tags = viterbi(sentence, sentence_count, word_tag_counts, tag_counts, transition_counts)
            predicted_tags_list.append((predicted_tags, ground_truth_tags))

    return predicted_tags_list

def evaluate(predicted_tags_list):
    total_tags = 0
    correct_tags = 0

    for predicted_tags, ground_truth_tags in predicted_tags_list:
        total_tags += len(ground_truth_tags)
        correct_tags += sum(p == g for p, g in zip(predicted_tags, ground_truth_tags))

    accuracy = correct_tags / total_tags if total_tags > 0 else 0

    with open("POS.test.out", "w") as file:
        for predicted_tags, ground_truth_tags in predicted_tags_list:
            file.write(f"Predicted: {' '.join(predicted_tags)}\n")
            file.write(f"Ground Truth: {' '.join(ground_truth_tags)}\n\n")

    print(f"Accuracy: {accuracy:.2%}")

def main():
    train_file = "../data/train/POS.train"
    test_file = "../data/test/POS.test"

    word_tag_counts = count_word_tag_pairs(train_file)
    tag_counts = count_tag_counts(train_file)
    transition_counts = count_transition_counts(train_file)
    sentence_count = count_sentences(train_file)

    predicted_tags_list = predict_tags(word_tag_counts, tag_counts, transition_counts, sentence_count, test_file)
    evaluate(predicted_tags_list)

    '''
    print("Empty string exists:", "" in tag_counts)
    print("Quotation tag exists:", "''" in tag_counts)
    print("Tags:", [repr(tag) for tag in tag_counts if not tag or tag == "''"])
    '''

    return 0

if __name__ == "__main__":
    main()
