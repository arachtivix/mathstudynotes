
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

(defn all-n-digit-masks [n]
  (if (= n 1) ["X" "O"]
      (let [subs (all-n-digit-masks (- n 1))]
        (concat
         (map #(str "X" %) subs)
         (map #(str "O" %) subs)))))

(defn combine-int-with-mask [n mask]
  (apply str (map #(if (= %1 \X) \X %2) mask (str n))))

(defn numbers-under-mask-all-same?
  ([n mask] (numbers-under-mask-all-same? (str n) mask #{}))
  ([n mask seen]
   (cond (= 0 (count n)) true
         (= \O (first mask)) (recur (rest n) (rest mask) seen)
         (= 0 (count seen)) (recur (rest n) (rest mask) #{(first n)})
         (contains? seen (first n)) (recur (rest n) (rest mask) seen)
         :else false)))

(defn num-to-masked
  ([n mask] (apply str (num-to-masked n mask [])))
  ([n mask sofar]
   (cond (not (seq? n)) (num-to-masked (seq (str n)) mask)
         (= 0 (count n)) sofar
         (= \X (first mask)) (recur (rest n) (rest mask) (conj sofar \X))
         :else (recur (rest n) (rest mask) (conj sofar (first n))))))

(defn solve []
  ;; TODO: Implement solution
  nil)

(defn -main []
  (println "Solution to Problem 51:")
  (println (solve)))
