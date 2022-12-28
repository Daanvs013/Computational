function evalue = expected(probobj, k, n)
total = 0;
for i = 1:length(k)
    fun = DISTRIBUTION(probobj{i}, k(i), n);
    p = k(i);
    subtotal = 0;
    for j = 1:20
        subtotal = subtotal + fun(j)* j;    
    end
    total = total + subtotal * p;
end
evalue = total;
end