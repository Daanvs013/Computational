function [matrix] = KTH_AUCTION(names, bids, copies)
sizes = size(bids);
A = cell(3,3);
for k = 1:length(names)
    A(k,1) = {names(k)};
    A(k,3) = {0};
end
j = 1;
while j < sizes(1) + 1
    itemprize = bids(j,:);
    copy = copies(j)
    [indexes, prize] = KTH_PRIZE(itemprize, copy);

    i = 1;
    len = size(indexes);
    while i < len(2) + 1
        position = indexes(i);
        B = A{position ,2}
        B(end+1) = j
        A{position ,2} = B
        oldprize = A(position, 3);
        newprize = oldprize{1} + prize;
        A(position, 3) = {newprize};
        i = i + 1
    end
    j = j + 1;
end
matrix = A
end

