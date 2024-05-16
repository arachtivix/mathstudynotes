(ns p4.core
  (:gen-class))

(defn is-pdrome
  [n]
  (let [s (str n)
        r (reverse s)
        q (seq s)]
    (= r q)))

(def all-pdrome-cands
  (filter is-pdrome (range 10000 998001)))

(def all-three-digit-divisors
  (range 100 999))

(defn is-three-digits
  [n]
  (and (> n 99) (< n 1000)))

(defn check-divisor
  [[pdrome divisor]]
  (and (= 0 (mod pdrome divisor)) (is-three-digits (/ pdrome divisor))))

(defn iter-two-combos
  [[curr & remaining] inner-coll]
  (if (not= curr nil)
    (concat
     (map #(list curr %) inner-coll)
     (iter-two-combos remaining inner-coll))
    (list)))

(defn result-coll
  []
  #(first %)
  (filter
   check-divisor
   (iter-two-combos all-pdrome-cands all-three-digit-divisors)))



