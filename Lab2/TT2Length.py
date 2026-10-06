import multiprocessing as mp
import os

# Input: দুই লাইনের document (প্রতি লাইন = ১টি map task)
DOCUMENTS = [
    "SUST software engineering students build distributed systems every day",
    "distributed systems help SUST software engineering students every day",
]

NUM_REDUCERS = 3


# ---------- MAP ----------
def map_task(doc_id, text):
    print(f"[MAP worker pid={os.getpid()}] mapping doc {doc_id}")
    pairs = []
    for word in text.split():
        pairs.append((len(word), 1))   # key = শব্দের দৈর্ঘ্য, value = 1
    return pairs


# ---------- SHUFFLE (sort + group + partition) ----------
def shuffle(all_mapped_pairs, num_reducers):
    groups = {}
    for pairs in all_mapped_pairs:
        for length, count in pairs:
            groups.setdefault(length, []).append(count)   # GROUP

    buckets = [{} for _ in range(num_reducers)]
    for length, counts in groups.items():
        bucket_id = hash(length) % num_reducers            # PARTITION
        buckets[bucket_id][length] = counts
    return buckets


# ---------- REDUCE ----------
def reduce_task(bucket_id, bucket):
    print(f"[REDUCE worker pid={os.getpid()}] bucket {bucket_id}: "
          f"lengths {sorted(bucket.keys())}")
    result = {}
    for length, counts in bucket.items():
        result[length] = sum(counts)
    return result


# ---------- MASTER ----------
def main():
    print("[MASTER] Splitting input into", len(DOCUMENTS), "map tasks")

    # Map phase
    with mp.Pool(processes=len(DOCUMENTS)) as pool:
        map_results = pool.starmap(
            map_task, [(i, doc) for i, doc in enumerate(DOCUMENTS)]
        )
    print("\n[MASTER] Map output:")
    for i, pairs in enumerate(map_results):
        print(f"  doc {i}: {pairs}")

    # Shuffle phase
    buckets = shuffle(map_results, NUM_REDUCERS)
    print("\n[MASTER] After shuffle (grouped):")
    for i, b in enumerate(buckets):
        print(f"  bucket {i}: {b}")

    # Reduce phase
    with mp.Pool(processes=NUM_REDUCERS) as pool:
        reduce_results = pool.starmap(reduce_task, list(enumerate(buckets)))

    # Combine
    final_counts = {}
    for partial in reduce_results:
        final_counts.update(partial)

    print("\n[MASTER] FINAL OUTPUT (word length -> occurrences):")
    for length, count in sorted(final_counts.items()):    # দৈর্ঘ্য অনুযায়ী সাজানো
        print(f"  length {length:2d} -> {count}")


if __name__ == "__main__":
    main()