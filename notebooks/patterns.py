from microtonal.patterns import Note, Pattern, S, T, S_, W, Shift

n = Note(0, 1, 0)
S(1) * n
S(1) * T(1) * n
W(1) * n

p = Pattern(16, [T(4*i) * n for i in range(4)])
p = Pattern(4, n)
p * p
p**4
p**2**2

p + S(1)*p

S(1) * p**4
q = p + S(1) * p + S(2) * p + S(3) * p

n + S(1) * n + S(2) * n + S(3) * n

S_(1) * q

p = Pattern(4, n + Shift(1,1) * n + Shift(2,2) * n + Shift(3,3) * n)
p * p