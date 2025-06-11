
(ns proj.p26.core
  (:require [proj.shared :as shared])
  (:gen-class))

;; Problem 26: Reciprocal Cycles
;; Created on 2025-05-10

;; lazy sequence simulating a grade schooler who never learned when to stop long dividing
(defn dec-exp [n m]
  (lazy-seq (let [q (quot n m) r (rem n m)] (cons q (dec-exp (* 10 r) m)))))

;For a number n, finds the length of the repeating decimal in 1/n.
; Returns [cycle-length n]
(defn find-cyc-len [n]
  (let [[e s] (shared/find-repeat (shared/dec-exp-components [1 n]) {} 0)]
    [(- e s) n]))

(defn gen-pairs-to-n [n] (map #(find-cyc-len %) (range 2 n)))

(defn solve-1 [n] (nth (reduce #(let [[c1] %1 [c2] %2] (if (> c1 c2) %1 %2)) (gen-pairs-to-n n)) 1))

; Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part.
#_{:clojure-lsp/ignore [:clojure-lsp/unused-public-var]}
(defn solve []
  (println (solve-1 1000)))

(defn -main []
  (println "Solution to Problem 26:")
  (println (solve-1 1000)))

