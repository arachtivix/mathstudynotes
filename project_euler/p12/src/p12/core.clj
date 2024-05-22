(ns p12.core)

; it seems these may have little to do with the solution, but I
; made a slightly handier way of getting a specific number of primes
; tonight
(defn next-prime
  [start prev-primes]
  (first
   (filter
    #(not (some (fn [x] (= 0 (mod % x))) prev-primes))
    (iterate #(+ 2 %) start))))

(defn n-primes
  [n]
  (cond (< n 1) '(2)
        (= n 2) '(3 2)
        :else (let [[gt :as prev-primes] (n-primes (- n 1))]
                (cons (next-prime (+ 2 gt) prev-primes) prev-primes))))


