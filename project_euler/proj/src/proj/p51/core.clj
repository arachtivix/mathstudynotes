
(ns proj.p51.core
  (:require [clojure.math.numeric-tower :as nt]
            [proj.shared :refer [prime-seq]])
  (:gen-class))

;; Problem 51: Prime Digit Replacements
;; Created on 2025-06-09

(defn all-n-digit-primes [n]
  (let [gt (nt/expt 10 n)
        lt (nt/expt 10 (- n 1))]
    (filter #(> % lt) (take-while #(< % gt) prime-seq))))


(defn solve []
  ;; TODO: Implement solution
  nil)

(defn -main []
  (println "Solution to Problem 51:")
  (println (solve)))
