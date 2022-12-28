function output = DISTRIBUTIONS(pdo, k, n)
output = @(y) factorial(n)*pdf(pdo,y)*(cdf(pdo,y))^(n-k-1)*(1-cdf(pdo,y))^k/(factorial(k)*factorial(n-k-1));
end


