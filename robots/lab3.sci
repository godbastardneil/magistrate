kw = 0.00211:0.00211*2:0.02743
A = [32.237,7.931,3.13,1.478,0.793,0.468,0.296]
w = [-0.4476555; -1.2300646; -1.6243413; -2.1111647; -2.3673124; -2.4788976; -2.69911]

t = 0:0.1:1489
t_len = length(t)

y0 = 26.5

y = y0 + (A * sin(kw '* t + repmat(w, 1, t_len)))

show_window(1);
plot(t, y);
xgrid()
