(ns p15.core)

(defn factorial
  ([n]
  (if (= n 0) 1
      (factorial (- n 1) n)))
  ([n c]
  (if (= n 0) c
      (recur (- n 1) (* n c)))))

; this problem is a classic -- it's just 40 choose 20
; the problem can be re-imagined as a sequence of chars D and R
; (D=down R=right) where you need to end up with 20 Ds and 20 Rs
; in any order, i.e. choosing 20 places of 40
(def answ
  (/
   (factorial (bigint 40))
   (* (bigint (factorial 20)) (bigint (factorial 20)))))
