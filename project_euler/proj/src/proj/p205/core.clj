
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

(defn solve [] 1234)

(defn -main []
  (println "Solution to Problem 205:")
  (println (solve)))
