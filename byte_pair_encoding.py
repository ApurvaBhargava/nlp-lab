from collections import Counter, defaultdict

def get_stats(vocab):
    """Count frequency of all adjacent pairs in the vocabulary."""
    pairs = defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[(symbols[i], symbols[i + 1])] += freq
    return pairs

def merge_vocab(pair, vocab):
    """Merge all occurrences of the most frequent pair."""
    bigram = ' '.join(pair)
    replacement = ''.join(pair)
    new_vocab = {}
    for word in vocab:
        # Replace the pair with merged token
        new_word = word.replace(bigram, replacement)
        new_vocab[new_word] = vocab[word]
    return new_vocab

def bpe_tokenizer(text, num_merges=10):
    # Initialize vocabulary with whitespace separated characters and their frequency
    vocab = Counter()
    for word in text.strip().split():
        tokenized_word = ' '.join(list(word)) + ' </w>'
        vocab[tokenized_word] += 1

    print("Initial Vocabulary:")
    for k, v in vocab.items():
        print(f"{k}: {v}")
    print()

    merges = []

    for i in range(num_merges):
        pairs = get_stats(vocab)
        if not pairs:
            break
        best = max(pairs, key=pairs.get)
        merges.append(best)
        print(f"Step {i + 1}: most frequent pair: {best} with frequency {pairs[best]}")
        vocab = merge_vocab(best, vocab)

        print("Vocabulary after merging:")
        for k, v in vocab.items():
            print(f"{k}: {v}")
        print()

    print("Final Merge Table (Lookup Table):")
    for idx, merge in enumerate(merges, 1):
        print(f"{idx}: {merge}")

    return vocab, merges

# Test an example
text = "believe unbelievable unable"
final_vocab, merge_table = bpe_tokenizer(text, num_merges=10)
