
(ns proj.p204.core
  (:require [clojure.math :as math]
            [proj.shared :as shared])
  (:gen-class))

;; Problem 204: Generalised Hamming Numbers
;; Created on 2025-06-20

(defn remove-factors [n factors-asc]
  (let [curr-factor (first factors-asc)]
    (cond (= n 1) 1
          (nil? curr-factor) n
          (= curr-factor n) 1
          (> curr-factor n) n
          (= 0 (rem n curr-factor))
          (recur (quot n curr-factor) factors-asc)
          :else (recur n (rest factors-asc)))))

;; a simple implementation of hamming numbers first:
(defn simple-generalized-hamming-numbers-impl-seq [n]
  (filter #(= 1 (remove-factors % n)) (iterate inc 1)))

(defn solve []
  ;; TODO: Implement solution
  nil)

(defn -main []
  (println "Solution to Problem 204:")
  (println (solve)))
