documents = [
        ("docB", "Python python and Git"),
        ("docA", "git Linux"),
        ("docC", "python linux linux")
]

stop_words = {"and"}



def build_index(
        documents: list[tuple[str, str]],
        stop_words: set[str]
) -> tuple[dict[str, list[str]], dict[str, int]]:
    index = {}
    freq = {}

    for row in documents:
        title = row[0]
        body = row[1].lower()

        words = body.split()
        
        for word in words:
            if word in stop_words:
                continue

            elif word not in index.keys():
                index[word] = [title]
                freq[word] = 1

            else:
                if title not in index[word]:
                    index[word].append(title)
                freq[word] = freq.get(word, 0) + 1


    results = (index, freq)

    return results



print(build_index(documents, stop_words))

# 辞書に対するinはkeyの存在を調べる
# freq[word] += 1出も追加可能
