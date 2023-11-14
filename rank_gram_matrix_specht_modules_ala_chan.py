#define action of S_n on Young tableaux T
def act(sigma,T):
    return Tableau([[sigma(l[i]) for i in range(len(l))] for l in T])

#define action on rows of tablueax
#g is an element of the subgroup \prod_i S_{n_i} where \sum_i n_i = n
#T is a tableau corresponding to some partition T.shape()
def act_rows(g,T):
    return [g[i](T[i]) for i in range(len(T))]

#determine when two tableaux are row-equivalent
def row_equiv(T_0,T_1):
    assert T_0.shape() == T_1.shape()
    row_group = cartesian_product([SymmetricGroup(size) for size in T_0.shape()])
    for g in row_group:
        if act_rows(g,T_0) == T_1:
            return True
    return False

#get columns of tableau
#there is a MUCH smarter way to do this
def cols(T):
    cols=[]
    for j in range(max(T.shape())):
        col=[]
        for i in range(len(T)):
            try:
                col.append(T[i][j])
            except:
                IndexError
        cols.append(col)
    return cols

#compute the column stabilizer of a tableau T
def col_stab(T):
    n=sum(T.shape())
    col_1 = cols(T)
    col_stabilizer = []
    for g in SymmetricGroup(n):
        col_2 = cols(act(g,T))
        assert len(col_1) == len(col_2)
        cols_preserved = True
        for i in range(len(col_1)):
            if set(col_1[i]) != set(col_2[i]):
                cols_preserved = False
        if cols_preserved:
            col_stabilizer.append(g)
    return col_stabilizer

#compute polytabloid e_T associated to a standard young tableau T
#e_T = \sum_{\sigma \in C_T} sgn(\sigma) { \sigma T}
#where {} is the row-equivalence class, i.e. a tabloid
#C_T is the column stabilizer, the subgroup of the symmetric group preserving the columns of tableau T setwise
#sgn is the sign of the permutation \sigma
#the sum takes place in the module generated by tabloids {T}
#represent lienar combination of tabloids as a dict={Tableau:Integer}
#if T_1 is equivalent to T_2, just increase the sum by sgn(\sigma)
#if T_1 is not equivalent to T_2, create a new entry
def polytabloid(T):
    e_T = {}
    C_T = col_stab(T)
    for pi in C_T:
        T_1 = act(pi,T)
        sum_contains_equiv = False
        for T_2 in e_T.keys():
            if row_equiv(T_1,T_2):
                sum_contains_equiv = True
                e_T[T_2] += sgn(pi)
        if not sum_contains_equiv:
            e_T[T_1] = sgn(pi)
    return e_T

#compute bilinear form <.,.> associated to span of tabloids
#<{s},{t}> = \delta_{{s},{t}}
#takes in two dicts representing polytabloids e_{T_1} and e_{T_2}
#iterates through both keys only increasing the sum by the product of entries when {s}=={t}, i.e. s ~ t
def bilinear_form(poly_1,poly_2):
    sum = 0
    for s in poly_1.keys():
        for t in poly_2.keys():
            if row_equiv(s,t):
                sum += poly_1[s]*poly_2[t]
    return sum

#use the bilinear form to compute the rank of the Gram matrix (<e_i,e_j>)_{i,j=1,...,n}
#note that polytabloids e_T form a basis for S^\lambda for *standard* tableau T
T = Tableau([[1,2,3],[4,5]])
def gram_matrix(T):
    std_tableaux=[act(g,T) for g in SymmetricGroup(sum(T.shape())) if act(g,T).is_standard()]
    gram_matrix=[[bilinear_form(polytabloid(T_1),polytabloid(T_2)) for T_1 in std_tableaux] for T_2 in std_tableaux]
    return gram_matrix

#compute the rank of the Gram matrix in characteristic 0
import numpy as np
A=gram_matrix(T)
np.linalg.matrix_rank(A)

#A modulo 3
np.mod(A,3)

#compue the rank of the Gram matrix modulo 3
np.linalg.matrix_rank(np.mod(A,3),3)