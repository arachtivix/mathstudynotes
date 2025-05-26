
(ns proj.p206.core
  (:require [clojure.math :as math]
            [proj.shared :as shared])
  (:gen-class))

;; Problem 206: Concealed Square
;; Created on 2025-05-23

(defn dec-exp-int "decimal expansion for an integer"
  ([n] (dec-exp-int n '()))
  ([n prv] (let [q (quot n 10) r (rem n 10) cur (cons r prv)]
             (if (= q 0) cur (recur q cur)))))

(defn matches-pattern? [p s]
  (let [pair-compare #(if (= %1 :_) true (= %1 %2))
        pairwise (into '() (map pair-compare p s))
        counts-match (= (count p) (count s))
        pairwise-all-good (reduce #(and %1 %2) pairwise)]
    (if counts-match pairwise-all-good false)))

(defn is-root-of-hidden-sq? [n]
  (matches-pattern?
   '(1 :_ 2 :_ 3 :_ 4 :_ 5 :_
       6 :_ 7 :_ 8 :_ 9 :_ 0)
   (dec-exp-int (* n n))))

(def max-possible-hidden-square 19293949596979899909N)
(def max-n (bigint (math/sqrt max-possible-hidden-square)))
(def min-possible-hidden-square 10203040506070809000N)
(def min-n (bigint (math/sqrt min-possible-hidden-square)))
(def num-brute-force (+ 1 (- max-n min-n)))

;; naive solution will take its sweet time
(defn sol1 [] (take 1 (filter is-root-of-hidden-sq? (range min-n max-n))))

(def max-m-possible-hidden-square 192939495969798999N)
(def max-m (bigint (math/sqrt max-m-possible-hidden-square)))
(def min-m-possible-hidden-square 102030405060708090N)
(def min-m (bigint (math/sqrt min-m-possible-hidden-square)))
(def num-m-brute-force (+ 1 (- max-m min-m)))

(defn is-m-sq? "Using the intermidiate step from the writeup"
  [m]
  (matches-pattern?
   '(1 :_ 2 :_ 3 :_ 4 :_ 5 :_
       6 :_ 7 :_ 8 :_ 9)
   (dec-exp-int (* m m))))

;; technically better, but also takes its sweet time
(defn sol2 [] (take 1 (filter is-m-sq? (range min-m max-m))))

;; let's generalize the brute force approach so we can actually test
;; that it works at a smaller scale
(defn max-dec-exp-from-pattern [p] (map #(if (= %1 :_) 9 %1) p))
(defn min-dec-exp-from-pattern [p] (map #(if (= %1 :_) 0 %1) p))
(defn dec-exp-to-bigint
  ([d] (if (= d '()) 0N (dec-exp-to-bigint d 0N)))
  ([[f & d] c] (let [cc (+ f (* 10 c))] (if (< 0 (count d)) (recur d cc) cc))))
(defn patt-max [p] (dec-exp-to-bigint (map #(if (= %1 :_) 9 %1) p)))
(defn patt-min [p] (dec-exp-to-bigint (map #(if (= %1 :_) 0 %1) p)))
(defn brute-force-generalized [p]
  (take 1 (filter #(matches-pattern? p (dec-exp-int (* %1 %1))) (range (bigint (math/sqrt (patt-min p))) (+ 1 (bigint (math/sqrt (patt-max p))))))))

(defn solve []
  ;; TODO: Implement solution
  nil)

(defn -main []
  (println "Solution to Problem 206:")
  (println (solve)))
