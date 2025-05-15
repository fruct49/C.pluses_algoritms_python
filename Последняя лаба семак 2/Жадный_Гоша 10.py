def cafe(prices):
    n = len(prices)
    max_coupons = n + 1  # Максимум n купонов

    # Инициализация DP
    dp = [[float('inf')] * (max_coupons) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(1, n + 1):
        price = prices[i - 1]
        for j in range(max_coupons):
            if dp[i - 1][j] == float('inf'):
                continue

            #Покупаем обед, получаем купон (если price > 500)
            new_j = j
            cost = dp[i - 1][j] + price
            if price > 500:
                new_j += 1
            if new_j < max_coupons:
                dp[i][new_j] = min(dp[i][new_j], cost)

            #Используем купон (не платим)
            if j > 0:
                dp[i][j - 1] = min(dp[i][j - 1], dp[i - 1][j])

    # Находим минимальную стоимость и оптимальное j
    min_cost = min(dp[n])
    best_j = min(j for j in range(max_coupons) if dp[n][j] == min_cost)

    # Восстанавливаем дни использования купонов
    used = []
    j = best_j
    for i in range(n, 0, -1):
        # Проверяем, был ли использован купон в день i
        if j + 1 < max_coupons and dp[i][j] == dp[i - 1][j + 1]:
            used.append(i)
            j += 1
        # Если не использован, проверяем, был ли получен купон
        else:
            price = prices[i - 1]
            if price > 500 and j > 0:
                j -= 1  # Откатываем получение купона

    print(min_cost, len(used))
    print(' '.join(map(str, sorted(used))))


cafe([500, 501, 300])
cafe([502, 501, 503, 504])