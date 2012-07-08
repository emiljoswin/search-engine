% This is the octave program for calculating the eigenvector of the 'big matrix'.
% here M is the transpose of big_matrix

function [v] = pagerank1(M, d, v_quadratic_error)
	l = length(M(:,1));
	for i = 1:l,
		s = sum(M(:,i));
		if s == 0,
			%disp(i);
			M(:,i) = ones(l,1);
			M(:,i) = M(:,i) ./ l;
			continue;
		end;
		M(:,i) = M(:,i) ./ s;
	end;
	disp(M);
	N = size(M, 2);  
	v = rand(N, 1);
	v = v ./ norm(v, 2);
	last_v = ones(N, 1) * inf;
	M_hat = (d .* M) + (((1 - d) / N) .* ones(N, N));
	while(norm(v - last_v, 2) > v_quadratic_error)
        	last_v = v;
	        v = M_hat * v;
        	v = v ./ norm(v, 2);
	end;
end;

