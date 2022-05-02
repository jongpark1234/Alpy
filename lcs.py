def lcs(s1, s2):
    result = []
    M, N = len(s1), len(s2)
    dp = [[0 for _ in range(N + 1)] for _ in range(M + 1)]
    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i][j - 1], dp[i - 1][j])
    i, j = M, N
    while True:
        if dp[i - 1][j] != dp[i][j] and dp[i][j - 1] != dp[i][j]:
            result.append(s2[j - 1])
            i -= 1
            j -= 1
        else:
            if dp[i - 1][j] == dp[i][j]:
                i -= 1
            elif dp[i][j - 1] == dp[i][j]:
                j -= 1
        if i == 0 or j == 0:
            break
    if dp[M][N] == 0:
        return ''
    else:
        return ''.join(map(str, result[::-1]))
