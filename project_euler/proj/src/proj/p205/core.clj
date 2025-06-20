
(ns proj.p205.core
  (:require [clojure.math :as math]
            [proj.shared :as shared])
  (:gen-class))

;; Problem 205: Dice Game
;; Created on 2025-06-15

(def single-roll-peter {1 1, 2 1, 3 1, 4 1}) ; score -> freq
(def single-roll-colin {-1 1, -2 1, -3 1, -4 1, -5 1, -6 1}) ; score -> freq

(defn assoc-or-compute [m f k v]
  (if (nil? (m k)) (assoc m k v) (assoc m k (f v (m k)))))

(defn seq-assoc-or-compute [m f kk vv] 
  (let [k (first kk)
        v (first vv)]
    (if (and (not (nil? k)) (not (nil? v)))
      (seq-assoc-or-compute (assoc-or-compute m f k v) f (rest kk) (rest vv))
      m)))

(defn combine-rolls [r1 r2]
  (let [two-tups (for [[k1 v1] r1
                       [k2 v2] r2]
                   [(+ k1 k2) (* v1 v2)])
        keys (map #(% 0) two-tups)
        vals (map #(% 1) two-tups)]
    (seq-assoc-or-compute {} + keys vals)))

(defn problem-combo []
  (let [p-2 (combine-rolls single-roll-peter single-roll-peter)
        p-4 (combine-rolls p-2 p-2)
        p-8 (combine-rolls p-4 p-4)
        p-9 (combine-rolls p-8 single-roll-peter)
        c-2 (combine-rolls single-roll-colin single-roll-colin)
        c-4 (combine-rolls c-2 c-2)
        c-6 (combine-rolls c-2 c-4)]
    (combine-rolls p-9 c-6)))

(defn solve [] (let[pc (problem-combo)
                    total-possibilities (reduce + (vals pc))
                    peter-wins (reduce + (map #(% 1) (filter #(< 0 (% 0)) pc)))]
                (float (/ peter-wins total-possibilities))))

(defn -main []
  (println "Solution to Problem 205:")
  (println (solve)))
