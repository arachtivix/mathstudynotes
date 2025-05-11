
(ns proj.p26.core
  (:require [clojure.math :as math]
            [proj.shared :as shared])
  (:gen-class))

;; Problem 26: Reciprocal Cycles
;; Created on 2025-05-10

(defn find-cycle-length
  "Finds the length of the recurring cycle in the decimal expansion of 1/n.
   Returns [n, cycle-length] where cycle-length is the length of the recurring cycle."
  [n]
  (let [remainders (loop [r 1
                          seen {}
                          pos 0]
                     (cond
                       (zero? r) [n 0]  ; Terminates with no cycle
                       (contains? seen r) [n (- pos (seen r))]  ; Found cycle
                       :else (recur (mod (* r 10) n)
                                   (assoc seen r pos)
                                   (inc pos))))]
    remainders))

(defn solve []
  "Find the value of d < 1000 for which 1/d contains the longest recurring cycle in its decimal fraction part."
  (->> (range 2 1000)
       (map find-cycle-length)
       (apply max-key second)
       (first)))

(defn -main []
  (println "Solution to Problem 26:")
  (println (solve)))

