
(ns proj.p203.core
  (:require [clojure.math :as math]
            [proj.shared :as shared])
  (:gen-class))

;; Problem 203: Squarefree Binomial Coefficients
;; Created on 2025-06-22

(defn next-pascal-row [p-row-prev]
  (cons 1 (conj (into [] (map #(+ %1 %2) p-row-prev (rest p-row-prev))) 1)))

(def pascal-seq ; turns out I probably did not need to do this
  (map #((% 1) (% 0))
       (iterate
        #(let [idx (% 0)
               nbrs (% 1)
               nxt (mod (+ idx 1) (count nbrs))]
           (if (= nxt 0)
             [0 (into [] (next-pascal-row nbrs))]
             [nxt nbrs]))
        [0 [1]])))

(defn take-rows [rows]
  (let [el-count (quot (+ (* rows rows) rows) 2)]
    (take el-count pascal-seq)))

(defn has-square-factor 
  ([n] (has-square-factor n 2))
  ([n test] (let [test-sq (* test test)]
              (cond (> test-sq n) false
                    (= (mod n test-sq) 0) true
                    :else (recur n (+ test 1))))))

(defn solve-1 [rows]
    (reduce + (filter #(not (has-square-factor %)) (distinct (take-rows rows)))))

(defn solve []
  ;; TODO: Implement solution
  (solve-1 50))

(defn -main []
  (println "Solution to Problem 203:")
  (println (solve)))
