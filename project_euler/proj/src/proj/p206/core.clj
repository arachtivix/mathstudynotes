
(ns proj.p206.core
  (:require [clojure.math :as math]
            [proj.shared :as shared])
  (:gen-class))

;; Problem 206: Concealed Square
;; Created on 2025-05-23

(defn dec-exp-int "decimal expansion for an integer"
  ([n] (dec-exp-int n '()))
  ([n prv] (let [q (quot n 10) r (rem n 10) cur (cons r prv)]
             (if (= r 0) prv (recur q cur)))))

(defn matches-pattern [p s]
  (let [pair-compare #(if (= %1 :_) true (= %1 %2))
        pairwise (into '() (map pair-compare p s))
        counts-match (= (count p) (count s))
        pairwise-all-good (reduce #(and %1 %2) pairwise)]
    (if counts-match pairwise-all-good false)))

(defn solve []
  ;; TODO: Implement solution
  nil)

(defn -main []
  (println "Solution to Problem 206:")
  (println (solve)))
