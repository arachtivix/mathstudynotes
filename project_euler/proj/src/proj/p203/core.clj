
(ns proj.p203.core
  (:require [clojure.math :as math]
            [proj.shared :as shared])
  (:gen-class))

;; Problem 203: Squarefree Binomial Coefficients
;; Created on 2025-06-22

(defn next-pascal-row [p-row-prev]
  (cons 1 (conj (into [] (map #(+ %1 %2) p-row-prev (rest p-row-prev))) 1)))

(defn solve []
  ;; TODO: Implement solution
  nil)

(defn -main []
  (println "Solution to Problem 203:")
  (println (solve)))
