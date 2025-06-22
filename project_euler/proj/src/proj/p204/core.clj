
(ns proj.p204.core
  (:require [clojure.math :as math]
            [proj.shared :as shared]
            [clojure.math.numeric-tower :as nt :refer [expt]])
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
  (let [factors (take-while #(>= n %) shared/prime-seq)]
    (filter #(= 1 (remove-factors % factors)) (iterate inc 1))))

;; so we can bootstrap some testing scenarios, let's implement a
;; brute force solution to the problem at low numbers
(defn brute-force-count [n leq]
  (count (take-while #(<= % leq) (simple-generalized-hamming-numbers-impl-seq n))))

(defn apply-factors [known-hamming-numbers prime-factors max]
  (let [to-add (for [f prime-factors hn known-hamming-numbers] (* f hn))
        updated-known (apply conj known-hamming-numbers (filter #(<= % max) to-add))
        stop (= (count updated-known) (count known-hamming-numbers))]
    (if stop known-hamming-numbers (apply-factors updated-known prime-factors max))))

(defn solve-1 [n thresh]
  (let [factors (take-while #(>= n %) shared/prime-seq)]
    (apply-factors (sorted-set 1) factors thresh)))

(defn solve []
  ;; TODO: Faster solution -- this one takes ten minutes
  (solve-1 100 1000000000))

(defn -main []
  (println "Solution to Problem 204:")
  (println (solve)))
