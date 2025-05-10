(ns proj.p7.core
  (:gen-class))

(defn calc-next-range
  [p]
  (range (+ p 2) (+ 2 (* p p)) 2))

(defn seq-contains-no-divisor
  [[:as ls] n]
  (not (some #(= 0 (mod n %)) ls)))

(defn primes
  [prev-primes]
  (let [rng (calc-next-range (apply max prev-primes))]
    (filter #(seq-contains-no-divisor prev-primes %) rng)))

; five layers of recursion will yield a mind bogglingly large
; sequence, so the lazy unrolling here should be able to treat
; this as effectively infinite
(def long-seq-o-primes
  (let [p1 [2 3 5]
        p2 (concat p1 (primes p1))
        p3 (concat p2 (primes p2))
        p4 (concat p3 (primes p3))]
    p4))

(defn solve []
  (last (take 10001 long-seq-o-primes)))

(defn -main []
  (println "Solution to Problem 7:")
  (println (solve)))
