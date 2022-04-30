import bisect
def lis(seq):
    seqLen = len(seq)
    record = [1] + [0 for _ in range(seqLen - 1)]
    dp = [seq[0]]
    result = []
    for i in range(1, seqLen):
        if dp[-1] < seq[i]:
            dp.append(seq[i])
            record[i] = len(dp)
        else:
            idx = bisect.bisect_left(dp, seq[i])
            dp[idx] = seq[i]
            record[i] = idx + 1
    Len = len(dp)
    for i in range(len(record) - 1, -1, -1):
        if record[i] == Len:
            result.append(seq[i])
            Len -= 1
        if Len < 1:
            break
    return result[::-1]
