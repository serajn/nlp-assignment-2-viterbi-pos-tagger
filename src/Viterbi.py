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

def viterbi(sentence, sentence_count, word_tag_counts, tag_counts, transition_counts):
    words = []
    ground_truth_tags = []

    for token in sentence.split():
        if token.strip():
            word, tag = token.strip().rsplit('/', 1) # Strip the tag from the word/tag pair
            words.append(word)
            ground_truth_tags.append(tag)

    # Initialization Step
    scores = {}
    backpointers = {0: {}}

    for tag in tag_counts:
        emission_probability = word_tag_counts.get((words[0], tag), 0) / tag_counts[tag]
        start_probability = transition_counts.get(("<START>", tag), 0) / sentence_count

        scores[tag] = emission_probability * start_probability
        backpointers[0][tag] = None  # No backpointer for the first word

    # Iteration Step
    for i in range(1, len(words)):
        new_scores = {}
        new_backpointers = {}
        
        for tag in tag_counts:
            emission_probability = word_tag_counts.get((words[i], tag), 0) / tag_counts[tag]

            best_score = 0
            best_prev_tag = None

            for prev_tag in tag_counts:
                transition_probability = transition_counts.get((prev_tag, tag), 0) / tag_counts[prev_tag]
                potential_score = scores[prev_tag] * transition_probability * emission_probability

                if potential_score > best_score:
                    best_score = potential_score
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

def main():
    train_file = "../data/train/POS.train"

    word_tag_counts = count_word_tag_pairs(train_file)
    tag_counts = count_tag_counts(train_file)
    transition_counts = count_transition_counts(train_file)
    sentence_count = count_sentences(train_file)

    return 0

if __name__ == "__main__":
    main()
