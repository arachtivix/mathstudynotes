
(ns proj.p26.core
  (:require [clojure.math :as math]
            [proj.shared :as shared])
  (:gen-class))

;; Problem 26: Reciprocal Cycles
;; Created on 2025-05-10

;; lazy sequence simulating a grade schooler who never learned when to stop long dividing
(defn dec-exp [n m]
  (lazy-seq (let [q (quot n m) r (rem n m)] (cons q (dec-exp (* 10 r) m)))))

(defn gen-pairs-to-n [n] (map #(shared/find-cyc-len %) (range 2 n)))

(defn solve-1 [n] (nth (reduce #(let [[c1] %1 [c2] %2] (if (> c1 c2) %1 %2)) (gen-pairs-to-n n)) 1))

(defn solve []
  "Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part."
  (println (solve-1 1000)))

(defn -main []
  (println "Solution to Problem 26:")
  (println (solve-1 1000)))

