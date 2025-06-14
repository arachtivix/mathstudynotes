
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

(defn solve []
  ;; TODO: Implement solution
  nil)

(defn -main []
  (println "Solution to Problem 51:")
  (println (solve)))
