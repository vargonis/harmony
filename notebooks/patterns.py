from microtonal.patterns import Note, Pattern, S, T, W

n = Note(0, 0, 1)
S(1) * n
S(1) * T(1) * n
W(2) * n

Pattern(16, [T(4*i) for i in range(4)])
p = Pattern(4, n)
p * p
p**4
p**2**2

(S(0) + S(1)) * n
(S(0) + S(1)) * p
(S(0) + T(1)) * p
(S(0) + T(6)) * p

S(1) * p**4
q = (S(0) + S(1) + S(2) + S(3)) * p

(S(0) + S(1) + S(2) + S(3)) * n

p = Pattern(4, S(0,0,1) + S(1,1,1) + S(2,2,1) + S(3,3,1))
p * p