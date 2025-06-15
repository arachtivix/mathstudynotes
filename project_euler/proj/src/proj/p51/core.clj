
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
   (cond (= nil (first n)) true
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

(defn get-valid-masked-values [n masks-to-try]
  (map #(num-to-masked n %)
       (filter #(numbers-under-mask-all-same? n %) masks-to-try)))

(defn multi-assoc [values m n]
  (if (= nil (first values)) m
      (let [curr (first values)
            existing (m curr)
            sub (multi-assoc (rest values) m n)]
        (if (= nil existing)
          (assoc sub curr (list n))
          (assoc sub curr (cons n existing))))))

(defn get-map-for-all
  ([num-digits] (get-map-for-all
                 (all-n-digit-primes num-digits)
                 (all-n-digit-masks num-digits)
                 {}))
  ([primes masks sofar]
   (if (= nil (first primes)) sofar
       (let [curr (first primes)
             valid-masked-values (get-valid-masked-values curr masks)]
         (recur (rest primes)
                masks
                (multi-assoc valid-masked-values sofar curr))))))

(defn get-earliest-conforming-group [mfa threshold]
  (let [count-matching (filter #(>= (count %) threshold) (vals mfa))]
    (if (= (count count-matching) 0)
      '()
      (reduce
       #(if (< (first %2) (first %1)) %2 %1)
       count-matching))))

(defn get-answer-for-num-digits [num-digits, threshold]
  (get-earliest-conforming-group
   (get-map-for-all num-digits)
   threshold))

(defn solve []
  ;; not the most performant, but it gets there in a few min
  ;; procedure to work through the args to this function could be automated but
  ;; maybe later
  (last (get-answer-for-num-digits 6, 8)))

(defn -main []
  (println "Solution to Problem 51:")
  (println (solve)))
